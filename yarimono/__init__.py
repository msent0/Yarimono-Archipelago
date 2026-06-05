"""Yarimono Archipelago world"""

from __future__ import annotations

from BaseClasses import Tutorial
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, Type, components

from .Items import (
    ITEMS, ITEM_BY_NAME, ItemCategory, ItemDef, YarimonoItem, make_item,
)
from .Locations import (
    ALL_LOCATIONS, LOCATION_BY_NAME, LocCategory, YarimonoLocation, GOLD_REWARDS,
    extra_shop_locations,
)
from .Options import YarimonoOptions
from .Regions import create_regions as _build_region_graph
from .Rules import set_completion_condition, set_rules


# Game patcher
# Registers a "Yarimono Patcher" entry to patch the game with the Archipelago plugin.
# Edition exe names — Steam / 072project have the romaji exe, DLsite uses the kana one.
_GAME_EXE_NAMES = ("YARISUTEMESUBUTA.exe", "ヤリステメスブター.exe")
_CLEAN_PLUGINS_JS_SHA256 = (
    "7c60427f7919aeb24c3b2808ece7092257a890595c247392d0ce8f10b3d7050a"
)
_PLUGIN_ENTRY = (
    '{"name":"YarimonoAP","status":true,'
    '"description":"Archipelago randomizer","parameters":{}}'
)


def _launch_patcher() -> None:
    import hashlib
    import pkgutil
    import re
    import tkinter as tk
    from pathlib import Path
    from tkinter import filedialog, messagebox

    root = tk.Tk()
    root.withdraw()

    picked = filedialog.askdirectory(title="Select your Yarimono game folder")
    if not picked:
        return
    game_dir = Path(picked)

    # Sanity check: must contain at least one of the known game exes.
    if not any((game_dir / n).is_file() for n in _GAME_EXE_NAMES):
        messagebox.showerror(
            "Wrong folder",
            f"None of {list(_GAME_EXE_NAMES)} were found in:\n  {game_dir}\n\n"
            "Pick the folder that contains the game's exe.",
        )
        return

    plugins_js  = game_dir / "data" / "www" / "js" / "plugins.js"
    plugin_dir  = game_dir / "data" / "www" / "js" / "plugins"
    icon_dir    = (game_dir / "data" / "www" / "img" / "pictures" /
                   "H_Scene" / "_DataBase" / "DouguIcon")
    if not plugins_js.is_file():
        messagebox.showerror(
            "Wrong folder",
            f"plugins.js not found at:\n  {plugins_js}\n\n"
            "The selected folder doesn't look like a Yarimono install.",
        )
        return

    plugin_bytes = pkgutil.get_data(__package__, "data/YarimonoAP.js")
    icon_bytes   = pkgutil.get_data(__package__, "data/archipelago.rpgmvp")
    if plugin_bytes is None or icon_bytes is None:
        messagebox.showerror(
            "Bundle error",
            "YarimonoAP.js or archipelago.rpgmvp is missing from this apworld.",
        )
        return

    current = plugins_js.read_bytes()
    current_hash = hashlib.sha256(current).hexdigest()
    already_patched = b'"YarimonoAP"' in current

    if not already_patched and current_hash != _CLEAN_PLUGINS_JS_SHA256:
        messagebox.showerror(
            "Unexpected plugins.js",
            "plugins.js sha256 is\n"
            f"  {current_hash}\n"
            "which doesn't match the known-clean hash\n"
            f"  {_CLEAN_PLUGINS_JS_SHA256}\n\n"
            "If you've modified it, restore the original first.",
        )
        return

    if not already_patched:
        text = current.decode("utf-8")
        close = re.search(r"\n\s*\]\s*;\s*\Z", text)
        if not close:
            messagebox.showerror(
                "Patch failed",
                "Couldn't locate the closing `];` of the $plugins array. "
                "Aborting without changes.",
            )
            return
        head = text[:close.start()].rstrip()
        tail = text[close.start():]  # includes "\n];"
        # Inspect what comes before the close: `}` (no trailing comma) or
        # `},` (already comma-terminated).
        sep = "," if head.endswith("}") else ""
        patched = head + sep + "\n" + _PLUGIN_ENTRY + tail
        plugins_js.with_suffix(".js.bak").write_bytes(current)
        plugins_js.write_bytes(patched.encode("utf-8"))

    # Copy the plugin and the AP icon.
    plugin_dir.mkdir(parents=True, exist_ok=True)
    icon_dir.mkdir(parents=True, exist_ok=True)
    (plugin_dir / "YarimonoAP.js").write_bytes(plugin_bytes)
    (icon_dir / "archipelago.rpgmvp").write_bytes(icon_bytes)

    note = ("plugins.js was already patched; plugin and icon refreshed."
            if already_patched
            else "plugins.js patched (backup: plugins.js.bak), plugin and icon installed.")
    messagebox.showinfo("Yarimono Installer", "Done.\n\n" + note)


components.append(Component(
    "Yarimono Patcher",
    description="Patch a Yarimono game installation with the Archipelago plugin.",
    func=_launch_patcher,
    component_type=Type.TOOL,
))

class YarimonoWorld(World):
    """Yarimono Archipelago world"""

    game = "Yarimono"
    options_dataclass = YarimonoOptions
    options: YarimonoOptions
    topology_present = True

    item_name_to_id = {it.name: it.code for it in ITEMS}
    location_name_to_id = {loc.name: loc.code for loc in ALL_LOCATIONS}
    explicit_indirect_conditions = False

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)
        self._extra_shop_locations: list = []

    def create_regions(self) -> None:
        _build_region_graph(self)
        self._place_locations()

    def _place_locations(self) -> None:
        """Attach each LocationDef to its declared region."""
        # Include extra-shop locations into the location pool.
        self._extra_shop_locations = extra_shop_locations(int(self.options.extra_levels))
        used_extra_codes = {loc.code for loc in self._extra_shop_locations}

        # Filter scenes based on the encyclopedia option.
        include_scenes = bool(self.options.randomize_yariman_encyclopedia)
        
        # Filter gold reward locations based on randomized trainer gold reward option.
        gold_rewards = bool(self.options.randomize_trainer_gold_reward)
  
        for loc_def in LOCATION_BY_NAME.values():
            if loc_def.category == LocCategory.SCENE_UNLOCK and not include_scenes:
                continue
            if loc_def.category == LocCategory.EXTRA_SHOP and loc_def.code not in used_extra_codes:
                continue
            if loc_def.category == LocCategory.GOLD_REWARD and not gold_rewards:
                continue
            self._attach_location(loc_def)

    def _attach_location(self, loc_def) -> None:
        region = self.multiworld.get_region(loc_def.region, self.player)
        loc = YarimonoLocation(self.player, loc_def.name, loc_def.code, region)
        region.locations.append(loc)

    def create_item(self, item: str) -> YarimonoItem:
        item_def: ItemDef = ITEM_BY_NAME[item]
        return make_item(item_def.name, self.player, scenes_randomized=bool(self.options.randomize_yariman_encyclopedia))

    def create_items(self) -> None:
        pool: list = []

        # When scenes are randomized, EVENT_ITEMs (non-filler) become
        # progression.
        scenes = bool(self.options.randomize_yariman_encyclopedia)

        # Road Passes are only added when the option is on.
        road_passes = bool(self.options.road_passes_required)
        
        # Gold rewards are only added when the option is on.
        gold_rewards = bool(self.options.randomize_trainer_gold_reward)

        # Trainer Levels
        level_loc_count = self._count_level_slots()
        for _ in range(level_loc_count):
            pool.append(make_item("Trainer Level", self.player, scenes_randomized=scenes))

        # One of each event item, ultimate move unlock, story checkpoint,
        # and, when randomized, scene.
        for it in ITEMS:
            if it.category == ItemCategory.TRAINER_LEVEL:
                continue
            if it.category == ItemCategory.SCENE_UNLOCK and not scenes:
                continue
            if it.category == ItemCategory.JUNK:
                continue
            if it.category == ItemCategory.GOLD:
                continue
            if it.category == ItemCategory.ROAD_PASS and not road_passes:
                continue
            pool.append(make_item(it.name, self.player, scenes_randomized=scenes))

        # Add gold reward items if the option is on.
        if gold_rewards:
            # Add one trainer gold reward item for len(GOLD_REWARDS) locations
            for _ in range(len(GOLD_REWARDS)):
                pool.append(make_item("Trainer Yen Reward", self.player, scenes_randomized=scenes))

        # Fill with random junk to make item and location sizes match.
        junk_names = [it.name for it in ITEMS if it.category == ItemCategory.JUNK]
        # Junk also includes all gold items except Trainer Yen Reward
        gold_items = [it.name for it in ITEMS if it.category == ItemCategory.GOLD and it.name != "Trainer Yen Reward"]
        junk_names.extend(gold_items)
        unfilled = self._unfilled_count() - len(pool)
        for _ in range(max(0, unfilled)):
            name = self.multiworld.random.choice(junk_names)
            pool.append(make_item(name, self.player, scenes_randomized=scenes))

        self.multiworld.itempool += pool

    def _count_level_slots(self) -> int:
        return sum(
            1 for loc in LOCATION_BY_NAME.values()
            if loc.category in (LocCategory.TRAINER_FIGHT, LocCategory.LEVEL_GRANT)
        ) + len(self._extra_shop_locations)

    def _unfilled_count(self) -> int:
        return sum(1 for _ in self.multiworld.get_unfilled_locations(self.player))

    def set_rules(self) -> None:
        set_rules(self)
        set_completion_condition(self)

    # Slot data sent to the client
    def fill_slot_data(self) -> dict:
        data = {
            "goal": int(self.options.goal),
            "randomize_yariman_encyclopedia": bool(self.options.randomize_yariman_encyclopedia),
            "limited_cheat_tackle": int(self.options.limited_cheat_tackle),
            "extra_levels": int(self.options.extra_levels),
            "encyclopedia_ct_bonus": int(self.options.encyclopedia_ct_bonus),
            "opponent_level_adjustment": int(self.options.opponent_level_adjustment),
            "fixed_trainer_levels": bool(self.options.fixed_trainer_levels),
            "randomize_trainer_yarimon": int(self.options.randomize_trainer_yarimon),
            "randomize_wild_yarimon": int(self.options.randomize_wild_yarimon),
            "randomize_yarimon_abilities": int(self.options.randomize_yarimon_abilities),
            "randomize_yarimon_moves": int(self.options.randomize_yarimon_moves),
            "road_passes_required": bool(self.options.road_passes_required),
            "road_pass_hints": bool(self.options.road_pass_hints),
            "randomize_trainer_gold_reward": bool(self.options.randomize_trainer_gold_reward),
            "trainer_reward_money_amount": int(self.options.trainer_reward_money_amount),
        }
        if data["road_passes_required"]:
            pass_locations: dict[str, dict] = {}
            for short, full in (("central", "Central Road Pass"),
                                ("beach",   "Beach Road Pass"),
                                ("cave",    "Cave Road Pass")):
                locations = self.multiworld.find_item_locations(full, self.player)
                if locations:
                    pass_locations[short] = {
                        "address": locations[0].address,
                        "player":  locations[0].player,
                    }
            data["pass_locations"] = pass_locations
        return data
