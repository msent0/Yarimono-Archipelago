"""Region graph for Yarimono."""

from __future__ import annotations

from dataclasses import dataclass, field

from BaseClasses import Region

from rule_builder.rules import (
    And, CanReachLocation, CanReachRegion, Has, Rule, True_,
)
from .Conditions import OnScenes, OnRoadPasses

REGIONS: list[str] = [
    "Menu",

    # --- Hajime Village & surrounding area ---
    "Hajime Village",
    "Protagonists House",
    "Protagonists House Basement",
    "Hikari's House",
    "Laboratory",
    "Laboratory Left",
    "Hajime Road",
    "Lava Hideout",
    "Hajime Forest Path",
    "Old Road",
    "Old Road Ruins",
    "Ruins",
    "Ruins (Cleared)",

    # --- Big City ---
    "Big City Entrance",
    "Big City",
    "Yarimon Center (Big City)",
    "Yarimon Center 2F (Big City)",
    "Laboratory (Big City)",
    "Typeless Gym",
    "Event Venue 1F",
    "Members-Only Bar",
    "Ryugasaki Gym",
    "Ryugasaki Gym Rest Area",
    "Ero Doujin Building",

    # --- Routes out of Big City ---
    "Cave Road",
    "City Road",
    "Beach Road",

    # --- Harbor Town & surrounding area ---
    "Tea House",
    "Tea House Fitness Room",
    "Tea House Special Room",
    "Holy Road",
    "Lake",
    "Central Church",
    "Central Church 2F",
    "Forest Hideout",
    "Harbor Town",
    "Inlet Hideout",
    "Yarimon Center (Harbor Town)",
    "Yarimon Center 2F (Harbor Town)",
    "Harbor Gym",
    "Candy Perorin",
    "Lucky Besuke Reception",
    "Pool",
    "Changing Rooms",

    # --- Wano Village & surrounding area ---
    "Wano Road",
    "Wano Village",
    "Yarimon Center (Wano Village)",
    "Yarimon Center 2F (Wano Village)",
    "Wano Mountain Cave 1F",
    "Wano Mountain Cave B1F",
    "Wano Mountain Cave Rest Area",
    "Wano Village School",
    "Wano Village Hut",
    "Keidai Road A",
    "Keidai Road B",
    "Shrine",
    "Dojo",
    "Old Road North",
    "Secret Shop",
    "Bath House",
    "Mens Bath",

    # --- Central ---
    "Makina Ranch",
    "Central Road",
    "Central",
    "Forest of Trials Entrance",
    "Forest of Trials",
    "Last Dungeon",
    "Crystal Room",
    "Post-ED",
    "Construction Site Office",

    # --- DLC2 ---
    "Resort",
    "Sand Area",
    "Coastline Area",
    "Deep Forest Area",
    "Hotel Lobby",
    "Hotel Room",
    "Villa Area",
    "Villa Room",
    "Monthly 1F",
    "Monthly 3F",
    "DLC2 Endgame",
]


@dataclass(frozen=True)
class Transition:
    src: str
    dst: str
    rule: Rule | None = None
    # Whether this transition is one-way (no implicit reverse Entrance).
    one_way: bool = False


TRANSITIONS: list[Transition] = [
    # Hajime Village & surrounding area
    Transition("Menu", "Hajime Village"),
    Transition("Hajime Village", "Protagonists House"),
    Transition("Protagonists House", "Protagonists House Basement"),
    Transition("Hajime Village", "Hikari's House",
               rule=CanReachLocation("Defeat Athena")),
    Transition("Hajime Village", "Laboratory"),
    Transition("Laboratory", "Laboratory Left"),
    Transition("Hajime Village", "Hajime Road"),
    Transition("Hajime Village", "Hajime Forest Path"),
    Transition("Hajime Road", "Big City Entrance"),
    Transition("Hajime Road", "Old Road"),
    Transition("Hajime Road", "Lava Hideout",
               rule=CanReachLocation("Dream 2 Complete")),
    Transition("Old Road", "Old Road Ruins"),
    Transition("Old Road Ruins", "Ruins",
               rule=CanReachLocation("Defeat Totoro")),
    Transition("Old Road Ruins", "Ruins (Cleared)",
               rule=CanReachLocation("Defeat Aya")),

    # Big City
    Transition("Big City Entrance", "Big City",
               rule=CanReachLocation("Defeat Leo")),
    Transition("Big City Entrance", "Yarimon Center (Big City)"),
    Transition("Yarimon Center (Big City)", "Yarimon Center 2F (Big City)"),
    Transition("Big City", "Laboratory (Big City)"),
    Transition("Big City", "Typeless Gym"),
    Transition("Big City", "Members-Only Bar"),
    Transition("Big City", "Ryugasaki Gym",
               rule=CanReachLocation("Defeat Aya")),
    Transition("Ryugasaki Gym", "Ryugasaki Gym Rest Area"),
    Transition("Big City", "Event Venue 1F",
               rule=CanReachLocation("Dream 2 Complete")),
    Transition("Big City", "Ero Doujin Building",
               rule=CanReachLocation("Defeat Athena")),

    # Routes out of Big City
    Transition("Big City", "Cave Road",
               rule=CanReachLocation("Dream 1 Complete") & OnRoadPasses(Has("Cave Road Pass"))),
    Transition("Big City", "City Road",
               rule=CanReachLocation("Dream 1 Complete") & OnRoadPasses(Has("Central Road Pass"))),
    Transition("Big City", "Beach Road",
               rule=CanReachLocation("Dream 1 Complete") & OnRoadPasses(Has("Beach Road Pass"))),

    # Harbor Town & surrounding area
    Transition("Beach Road", "Holy Road"),
    Transition("Holy Road", "Lake"),
    Transition("Holy Road", "Central Church"),
    Transition("Central Church", "Central Church 2F"),
    Transition("Holy Road", "Forest Hideout"),
    Transition("Beach Road", "Tea House"),
    Transition("Tea House", "Tea House Fitness Room",
               rule=Has("VIP Card")),
    Transition("Tea House Fitness Room", "Tea House Special Room"),
    Transition("Beach Road", "Harbor Town"),
    Transition("Harbor Town", "Yarimon Center (Harbor Town)"),
    Transition("Yarimon Center (Harbor Town)", "Yarimon Center 2F (Harbor Town)"),
    Transition("Harbor Town", "Harbor Gym"),
    Transition("Harbor Town", "Candy Perorin"),
    Transition("Harbor Town", "Lucky Besuke Reception"),
    Transition("Lucky Besuke Reception", "Pool"),
    Transition("Pool", "Changing Rooms"),
    Transition("Harbor Town", "Inlet Hideout"),

    # Wano Village & surrounding area
    Transition("Wano Mountain Cave 1F", "Keidai Road A"),
    Transition("Cave Road", "Wano Mountain Cave 1F", rule=CanReachLocation("Dream 2 Complete")),
    Transition("Wano Mountain Cave 1F", "Wano Mountain Cave B1F"),
    Transition("Wano Mountain Cave 1F", "Wano Mountain Cave Rest Area"),
    Transition("Keidai Road A", "Wano Village"),
    Transition("Wano Village", "Yarimon Center (Wano Village)"),
    Transition("Yarimon Center (Wano Village)", "Yarimon Center 2F (Wano Village)"),
    Transition("Wano Village", "Wano Village School"),
    Transition("Wano Village", "Wano Village Hut"),
    Transition("Wano Village", "Keidai Road B"),
    Transition("Keidai Road B", "Shrine"),
    Transition("Wano Village", "Dojo"),
    Transition("Wano Village", "Bath House"),
    Transition("Bath House", "Mens Bath"),
    Transition("Shrine", "Old Road North"),
    Transition("Old Road North", "Secret Shop",
               rule=CanReachLocation("Defeat White God")),
    Transition("Wano Village", "Wano Road"),

    # Central & endgame
    Transition("City Road", "Central Road"),
    Transition("Central Road", "Central"),
    Transition("Central Road", "Forest of Trials Entrance"),
    Transition("Forest of Trials Entrance", "Forest of Trials",
               rule=CanReachLocation("Defeat Patra")),
    Transition("City Road", "Makina Ranch"),
    Transition("City Road", "Construction Site Office"),
    Transition("Central", "Last Dungeon",
               rule=CanReachLocation("Defeat Hikari (Tournament)")),
    Transition("Last Dungeon", "Crystal Room"),
    Transition("Crystal Room", "Post-ED",
               rule=CanReachLocation("Defeat White God"),
               one_way=True),

    # DLC2
    Transition("Harbor Town", "Resort",
               rule=CanReachLocation("Defeat Athena")),
    Transition("Resort", "Sand Area"),
    Transition("Resort", "Coastline Area"),
    Transition("Sand Area", "Deep Forest Area"),
    Transition("Coastline Area", "Deep Forest Area"),
    Transition("Resort", "Hotel Lobby"),
    Transition("Hotel Lobby", "Hotel Room"),
    Transition("Resort", "Villa Area"),
    Transition("Villa Area", "Villa Room"),

    Transition("Resort", "Monthly 1F"),
    Transition("Monthly 1F", "Monthly 3F",
               rule=(CanReachLocation("Defeat Akira (DLC2)") & CanReachLocation("Defeat Taiga (DLC2)") & CanReachLocation("Defeat Yoru and Neru") & CanReachLocation("Defeat Ero-doujin Sensei"))),

    Transition("Deep Forest Area", "DLC2 Endgame"),
]


# ---------------------------------------------------------------------------
# Graph builder
# ---------------------------------------------------------------------------

def create_regions(world) -> None:
    """Build the Region graph."""
    region_objs: dict[str, Region] = {}
    for name in REGIONS:
        r = Region(name, world.player, world.multiworld)
        region_objs[name] = r
        world.multiworld.regions.append(r)

    for t in TRANSITIONS:
        src = region_objs[t.src]
        dst = region_objs[t.dst]
        src.connect(dst, name=f"{t.src} -> {t.dst}")

    world.regions = region_objs  # stash for the world's later phases
