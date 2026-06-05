"""Yarimono Archipelago locations.

Location Categories:

- TRAINER_FIGHT: Trainer fights that grant a level up when defeated.
- LEVEL_GRANT: Non-battle level ups.
- EXTRA_SHOP: AP-purchasable slots added to shops and vending machines.
- PICKUP: Chests and hidden items.
- SCENE: When `randomize_yariman_encyclopedia` is on. Adds each scene as a
    location.
- EVENT_PURCHASE: Event items in the secret shop and Lucky Besuke.
- EVENT_PICKUP: VIP Card.
- STORY_CHECKPOINT: Synthetic checks for beating chapters 1-4, White God, and Tama.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum, auto

from BaseClasses import Location

from rule_builder.rules import (
    And, CanReachLocation, CanReachRegion, Has, Rule, True_,
)

from .Conditions import OnScenes

BASE_ID = 1082_000
TRAINER_FIGHT_BASE_ID = BASE_ID
LEVEL_GRANT_BASE_ID = BASE_ID + 1000
EXTRA_SHOP_BASE_ID = BASE_ID + 2000
PICKUP_BASE_ID = BASE_ID + 3000
SCENE_UNLOCK_BASE_ID = BASE_ID + 4000
EVENT_PURCHASE_BASE_ID = BASE_ID + 5000
EVENT_PICKUP_BASE_ID = BASE_ID + 6000
STORY_CHECKPOINT_BASE_ID = BASE_ID + 7000
ULTIMATE_MOVE_BASE_ID = BASE_ID + 8000
TRAINER_GOLD_REWARD_BASE_ID = BASE_ID + 9000

AP_PURCHASE_SLOTS: list[tuple[str, int, str]] = [
        # Main shops
        ("Laboratory", 3, "Lab Shop"),
        ("Yarimon Center (Big City)", 1, "YC Big City"),
        ("Yarimon Center (Harbor Town)", 1, "YC Harbor"),
        ("Big City", 2, "DS Food A"),  # Department Store 2F
        ("Big City", 1, "DS Food B"),

        # Vending — Hajime Road
        ("Hajime Road", 4, "VM Hajime Road A"),
        ("Hajime Road", 3, "VM Hajime Road B"),

        # Vending — Cave Road
        ("Cave Road", 3, "VM Cave Road A"),
        ("Cave Road", 4, "VM Cave Road B"),

        # Vending — Old Road
        ("Old Road North", 3, "VM Old Road"),

        # Vending — Big City (street-level)
        ("Big City", 3, "VM Big City A"),
        ("Big City", 3, "VM Big City B"),
        ("Big City", 3, "VM Big City C"),
        ("Big City", 4, "VM Big City D"),
        ("Big City", 4, "VM Big City E"),
        ("Big City", 3, "VM Big City F"),
        ("Big City", 3, "VM Big City G"),
        ("Big City", 4, "VM Big City H"),
        ("Big City", 3, "VM Big City I"),

        # Vending — Department Store 2F (Big City)
        ("Big City", 4, "VM Dept Store A"),
        ("Big City", 3, "VM Dept Store B"),
        ("Big City", 3, "VM Dept Store C"),

        # Vending — Central Church 2F
        ("Central Church 2F", 4, "VM Church A"),
        ("Central Church 2F", 3, "VM Church B"),
        ("Central Church 2F", 3, "VM Church C"),

        # Vending — Beach Road
        ("Beach Road", 4, "VM Beach Road"),

        # Vending — Harbor Town
        ("Harbor Town", 3, "VM Harbor A"),
        ("Harbor Town", 3, "VM Harbor B"),
        ("Harbor Town", 3, "VM Harbor C"),
        ("Harbor Town", 3, "VM Harbor D"),
        ("Harbor Town", 4, "VM Harbor E"),

        # Vending — Resort
        ("Resort", 4, "VM Resort A"),
        ("Resort", 4, "VM Resort B"),
        ("Resort", 3, "VM Resort C"),
        ("Resort", 3, "VM Resort D"),
    ]


class LocCategory(IntEnum):
    TRAINER_FIGHT = auto()
    LEVEL_GRANT = auto()
    EXTRA_SHOP = auto()
    PICKUP = auto()
    SCENE_UNLOCK = auto()
    EVENT_PURCHASE = auto()
    EVENT_PICKUP = auto()
    STORY_CHECKPOINT = auto()
    ULTIMATE_MOVE_BASE_ID = auto()
    GOLD_REWARD = auto()


@dataclass(frozen=True)
class LocationDef:
    code: int  # Location id
    name: str  # Display name
    category: LocCategory
    required_level: int = 0  # `TrainerLv >= required_level`
    region: str = "Yarimono"  # Region name in the access graph
    rule: Rule | None = None  # Additional rules

# In most cases required_level is the games recommended level - 5 (Player starts at level 5).
TRAINER_FIGHTS: list[LocationDef] = [
    # Hajime Village
    LocationDef(TRAINER_FIGHT_BASE_ID + 2, "Defeat Hikari",
                LocCategory.TRAINER_FIGHT, required_level=0, region="Hajime Village"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 34, "Defeat Sanae",
                LocCategory.TRAINER_FIGHT, required_level=90, region="Hajime Village"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 63, "Defeat Luna",
                LocCategory.TRAINER_FIGHT, required_level=49, region="Laboratory",
                rule=(CanReachLocation("Dream 2 Complete"))),
    LocationDef(TRAINER_FIGHT_BASE_ID + 86, "Defeat Maho",
                LocCategory.TRAINER_FIGHT, required_level=20, region="Hajime Village",
                rule=(CanReachLocation("Dream 2 Complete"))),
    LocationDef(TRAINER_FIGHT_BASE_ID + 90, "Defeat Kuina",
                LocCategory.TRAINER_FIGHT, required_level=35, region="Hajime Village",
                rule=(CanReachLocation("Dream 2 Complete"))),

    # Hajime Road
    LocationDef(TRAINER_FIGHT_BASE_ID + 3, "Defeat Kantaro",
                LocCategory.TRAINER_FIGHT, required_level=0, region="Hajime Road"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 13, "Defeat Yuna",
                LocCategory.TRAINER_FIGHT, required_level=0, region="Hajime Road"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 4, "Defeat Hotaru",
                LocCategory.TRAINER_FIGHT, required_level=0, region="Hajime Road"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 36, "Defeat Honoka",
                LocCategory.TRAINER_FIGHT, required_level=1, region="Hajime Road"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 5, "Defeat Takezou",
                LocCategory.TRAINER_FIGHT, required_level=4, region="Hajime Road"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 35, "Defeat Sumire",
                LocCategory.TRAINER_FIGHT, required_level=23, region="Hajime Road"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 41, "Defeat Jill",
                LocCategory.TRAINER_FIGHT, required_level=27, region="Hajime Road",
                rule=(CanReachLocation("Dream 2 Complete"))),
    LocationDef(TRAINER_FIGHT_BASE_ID + 56, "Defeat Smith",
                LocCategory.TRAINER_FIGHT, required_level=22, region="Old Road"),

    # Big City
    # This Leo fight can actually be progressed by losing, so the required level is 0.
    LocationDef(TRAINER_FIGHT_BASE_ID + 12, "Defeat Leo",
                LocCategory.TRAINER_FIGHT, required_level=0, region="Big City Entrance"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 47, "Defeat Natsumi",
                LocCategory.TRAINER_FIGHT, required_level=30, region="Big City"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 6, "Defeat Shota",
                LocCategory.TRAINER_FIGHT, required_level=5, region="Big City"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 7, "Defeat Rokurou",
                LocCategory.TRAINER_FIGHT, required_level=11, region="Big City"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 8, "Defeat Jinbei",
                LocCategory.TRAINER_FIGHT, required_level=10, region="Big City"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 9, "Defeat Yoshimitsu",
                LocCategory.TRAINER_FIGHT, required_level=20, region="Big City"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 57, "Defeat Watson",
                LocCategory.TRAINER_FIGHT, required_level=10, region="Big City"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 67, "Defeat Melon",
                LocCategory.TRAINER_FIGHT, required_level=28, region="Laboratory (Big City)"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 27, "Defeat Riona",
                LocCategory.TRAINER_FIGHT, required_level=20, region="Typeless Gym"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 26, "Defeat Shingo",
                LocCategory.TRAINER_FIGHT, required_level=5, region="Typeless Gym"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 28, "Defeat Taiboku",
                LocCategory.TRAINER_FIGHT, required_level=30, region="Typeless Gym",
                rule=(CanReachLocation("Defeat Riona") & CanReachLocation("Defeat Shingo"))),
    LocationDef(TRAINER_FIGHT_BASE_ID + 20, "Defeat Corn",
                LocCategory.TRAINER_FIGHT, required_level=37, region="Ryugasaki Gym"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 22, "Defeat Iori",
                LocCategory.TRAINER_FIGHT, required_level=43, region="Ryugasaki Gym"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 72, "Defeat Neru",
                LocCategory.TRAINER_FIGHT, required_level=41, region="Ryugasaki Gym"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 71, "Defeat Yoru",
                LocCategory.TRAINER_FIGHT, required_level=40, region="Big City",
                rule=CanReachLocation("Defeat Aya")),
    LocationDef(TRAINER_FIGHT_BASE_ID + 109, "Defeat Quem",
                LocCategory.TRAINER_FIGHT, required_level=48, region="Event Venue 1F"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 39, "Defeat Maki",
                LocCategory.TRAINER_FIGHT, required_level=50, region="Big City"),

    # Beach Road
    LocationDef(TRAINER_FIGHT_BASE_ID + 14, "Defeat Yamato",
                LocCategory.TRAINER_FIGHT, required_level=19, region="Beach Road"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 122, "Defeat Manpuku",
                LocCategory.TRAINER_FIGHT, required_level=23, region="Beach Road"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 10, "Defeat Murasaki",
                LocCategory.TRAINER_FIGHT, required_level=19, region="Beach Road"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 11, "Defeat Fran",
                LocCategory.TRAINER_FIGHT, required_level=23, region="Beach Road"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 15, "Defeat Gyan",
                LocCategory.TRAINER_FIGHT, required_level=22, region="Beach Road"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 65, "Defeat Haruka",
                LocCategory.TRAINER_FIGHT, required_level=10, region="Tea House"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 106, "Defeat Kana",
                LocCategory.TRAINER_FIGHT, required_level=40, region="Tea House",
                rule=CanReachLocation("Defeat Haruka")),
    LocationDef(TRAINER_FIGHT_BASE_ID + 127, "Defeat Hina",
                LocCategory.TRAINER_FIGHT, required_level=40, region="Tea House",
                rule=CanReachLocation("Defeat Haruka")),

    # Holy Road
    LocationDef(TRAINER_FIGHT_BASE_ID + 16, "Defeat Nene",
                LocCategory.TRAINER_FIGHT, required_level=16, region="Holy Road"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 18, "Defeat Armin",
                LocCategory.TRAINER_FIGHT, required_level=17, region="Central Church"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 30, "Defeat Matsunoki",
                LocCategory.TRAINER_FIGHT, required_level=15, region="Holy Road"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 19, "Defeat Vitalis",
                LocCategory.TRAINER_FIGHT, required_level=33, region="Central Church"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 50, "Defeat Marisa",
                LocCategory.TRAINER_FIGHT, required_level=40, region="Central Church 2F"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 62, "Defeat Vritra",
                LocCategory.TRAINER_FIGHT, required_level=54, region="Central Church 2F"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 112, "Defeat Rumi",
                LocCategory.TRAINER_FIGHT, required_level=33, region="Harbor Town", rule=CanReachRegion("Dojo")),

    # Harbor Town
    LocationDef(TRAINER_FIGHT_BASE_ID + 58, "Defeat Akari",
                LocCategory.TRAINER_FIGHT, required_level=22, region="Harbor Town"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 59, "Defeat Marin",
                LocCategory.TRAINER_FIGHT, required_level=23, region="Harbor Town"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 85, "Defeat Shouta",
                LocCategory.TRAINER_FIGHT, required_level=23, region="Harbor Town"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 60, "Defeat Mei",
                LocCategory.TRAINER_FIGHT, required_level=25, region="Harbor Gym"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 113, "Defeat Hibana",
                LocCategory.TRAINER_FIGHT, required_level=27, region="Harbor Gym"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 120, "Defeat Ryusen",
                LocCategory.TRAINER_FIGHT, required_level=31, region="Harbor Gym",
                rule=(CanReachLocation("Defeat Mei") & CanReachLocation("Defeat Hibana"))),
    LocationDef(TRAINER_FIGHT_BASE_ID + 37, "Defeat Leo (Harbor)",
                LocCategory.TRAINER_FIGHT, required_level=30, region="Harbor Town"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 44, "Defeat Mizuki",
                LocCategory.TRAINER_FIGHT, required_level=53, region="Harbor Town"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 70, "Defeat Taiga",
                LocCategory.TRAINER_FIGHT, required_level=63, region="Harbor Town"),

    # Pool
    LocationDef(TRAINER_FIGHT_BASE_ID + 74, "Defeat Minako",
                LocCategory.TRAINER_FIGHT, required_level=25, region="Pool"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 75, "Defeat Tina",
                LocCategory.TRAINER_FIGHT, required_level=25, region="Pool"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 76, "Defeat Tamaki",
                LocCategory.TRAINER_FIGHT, required_level=27, region="Pool"),

    # City Road
    LocationDef(TRAINER_FIGHT_BASE_ID + 49, "Defeat Meena",
                LocCategory.TRAINER_FIGHT, required_level=20, region="Makina Ranch"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 29, "Defeat Emily",
                LocCategory.TRAINER_FIGHT, required_level=21, region="Makina Ranch"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 31, "Defeat Dengaku",
                LocCategory.TRAINER_FIGHT, required_level=10, region="City Road"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 32, "Defeat Kurumi",
                LocCategory.TRAINER_FIGHT, required_level=10, region="City Road"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 78, "Defeat Patra",
                LocCategory.TRAINER_FIGHT, required_level=45, region="Forest of Trials Entrance"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 87, "Defeat Opera",
                LocCategory.TRAINER_FIGHT, required_level=40, region="Forest of Trials", rule=CanReachLocation("Defeat Patra")),
    LocationDef(TRAINER_FIGHT_BASE_ID + 61, "Defeat Akira",
                LocCategory.TRAINER_FIGHT, required_level=51, region="Makina Ranch"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 73, "Defeat Leo (Forest of Trials)",
                LocCategory.TRAINER_FIGHT, required_level=68, region="Forest of Trials",
                rule=(CanReachLocation("Defeat Patra") & CanReachLocation("Defeat Luna") & CanReachLocation("Defeat Quem") & CanReachLocation("Defeat Maki") & CanReachLocation("Defeat Vritra") & CanReachLocation("Defeat Mizuki") & CanReachLocation("Defeat Taiga") & CanReachLocation("Defeat Akira") & CanReachLocation("Defeat Momohime") & CanReachLocation("Defeat Kurohime") & CanReachLocation("Defeat Aoi") & CanReachLocation("Defeat Aya"))),

    # Cave Road
    LocationDef(TRAINER_FIGHT_BASE_ID + 21, "Defeat Fence",
                LocCategory.TRAINER_FIGHT, required_level=30, region="Cave Road"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 48, "Defeat Kanako",
                LocCategory.TRAINER_FIGHT, required_level=33, region="Cave Road"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 24, "Defeat Battou",
                LocCategory.TRAINER_FIGHT, required_level=30, region="Wano Mountain Cave 1F"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 23, "Defeat Akage",
                LocCategory.TRAINER_FIGHT, required_level=32, region="Wano Mountain Cave 1F"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 25, "Defeat Totoro",
                LocCategory.TRAINER_FIGHT, required_level=33, region="Keidai Road A"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 110, "Defeat Vice",
                LocCategory.TRAINER_FIGHT, required_level=64, region="Wano Mountain Cave 1F", rule=CanReachLocation("Defeat Athena")),
    LocationDef(TRAINER_FIGHT_BASE_ID + 108, "Defeat Quem (Cave)",
                LocCategory.TRAINER_FIGHT, required_level=85, region="Wano Mountain Cave 1F", rule=CanReachLocation("Defeat Athena")),

    # Wano Road
    LocationDef(TRAINER_FIGHT_BASE_ID + 123, "Defeat Masayuki",
                LocCategory.TRAINER_FIGHT, required_level=35, region="Wano Road"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 88, "Defeat Shiryu",
                LocCategory.TRAINER_FIGHT, required_level=43, region="Bath House"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 128, "Defeat Mitsukuni",
                LocCategory.TRAINER_FIGHT, required_level=40, region="Wano Road"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 84, "Defeat Rinrin",
                LocCategory.TRAINER_FIGHT, required_level=21, region="Wano Road"),

    # Wano Village
    LocationDef(TRAINER_FIGHT_BASE_ID + 38, "Defeat Hikari (Wano)",
                LocCategory.TRAINER_FIGHT, required_level=38, region="Wano Village"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 51, "Defeat Shishio",
                LocCategory.TRAINER_FIGHT, required_level=32, region="Wano Village"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 52, "Defeat Little Ta-ke",
                LocCategory.TRAINER_FIGHT, required_level=30, region="Wano Village"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 53, "Defeat Anderson",
                LocCategory.TRAINER_FIGHT, required_level=33, region="Wano Village"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 124, "Defeat Bunta",
                LocCategory.TRAINER_FIGHT, required_level=33, region="Wano Village"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 54, "Defeat Phineh",
                LocCategory.TRAINER_FIGHT, required_level=43, region="Wano Village School"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 68, "Defeat Chie",
                LocCategory.TRAINER_FIGHT, required_level=30, region="Wano Village"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 69, "Defeat Anna",
                LocCategory.TRAINER_FIGHT, required_level=35, region="Wano Village"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 105, "Defeat Nanase",
                LocCategory.TRAINER_FIGHT, required_level=46, region="Dojo"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 40, "Defeat Momohime",
                LocCategory.TRAINER_FIGHT, required_level=52, region="Wano Village"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 42, "Defeat Kurohime",
                LocCategory.TRAINER_FIGHT, required_level=52, region="Wano Village"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 126, "Defeat Marble",
                LocCategory.TRAINER_FIGHT, required_level=28, region="Yarimon Center (Wano Village)"),

    # Shrine
    LocationDef(TRAINER_FIGHT_BASE_ID + 55, "Defeat Umenoki",
                LocCategory.TRAINER_FIGHT, required_level=36, region="Shrine"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 17, "Defeat Sophia",
                LocCategory.TRAINER_FIGHT, required_level=39, region="Shrine"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 89, "Defeat Sara",
                LocCategory.TRAINER_FIGHT, required_level=42, region="Shrine"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 43, "Defeat Aoi",
                LocCategory.TRAINER_FIGHT, required_level=59, region="Shrine"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 104, "Defeat Murei",
                LocCategory.TRAINER_FIGHT, required_level=37, region="Shrine"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 125, "Defeat Charlie",
                LocCategory.TRAINER_FIGHT, required_level=39, region="Old Road North"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 132, "Defeat Orochi",
                LocCategory.TRAINER_FIGHT, required_level=42, region="Old Road North"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 64, "Defeat Aya",
                LocCategory.TRAINER_FIGHT, required_level=43, region="Ruins"),

    # Central
    LocationDef(TRAINER_FIGHT_BASE_ID + 45, "Defeat Maki (Tournament)",
                LocCategory.TRAINER_FIGHT, required_level=72, region="Central", 
                rule=CanReachLocation("Dream 4 Complete")),
    LocationDef(TRAINER_FIGHT_BASE_ID + 46, "Defeat Hikari (Tournament)",
                LocCategory.TRAINER_FIGHT, required_level=71, region="Central", 
                rule=CanReachLocation("Dream 4 Complete")),
    LocationDef(TRAINER_FIGHT_BASE_ID + 77, "Defeat Athena",
                LocCategory.TRAINER_FIGHT, required_level=90, region="Central",
                rule=CanReachLocation("Defeat White God")),

    # DLC Fights
    LocationDef(TRAINER_FIGHT_BASE_ID + 140, "Defeat Hotaru (DLC1)",
                LocCategory.TRAINER_FIGHT, required_level=95, region="Hajime Road", rule=CanReachLocation("Defeat Athena")),
    LocationDef(TRAINER_FIGHT_BASE_ID + 142, "Defeat Sanae (DLC1)",
                LocCategory.TRAINER_FIGHT, required_level=95, region="Hajime Village", rule=CanReachLocation("Defeat Athena")),
    LocationDef(TRAINER_FIGHT_BASE_ID + 144, "Defeat Maho (DLC1)",
                LocCategory.TRAINER_FIGHT, required_level=95, region="Hajime Village", rule=CanReachLocation("Defeat Athena")),
    LocationDef(TRAINER_FIGHT_BASE_ID + 145, "Defeat Kuina (DLC1)",
                LocCategory.TRAINER_FIGHT, required_level=95, region="Hajime Village", rule=CanReachLocation("Defeat Athena")),
    LocationDef(TRAINER_FIGHT_BASE_ID + 147, "Defeat Honoka (DLC1)",
                LocCategory.TRAINER_FIGHT, required_level=95, region="Big City", rule=CanReachLocation("Defeat Athena")),
    LocationDef(TRAINER_FIGHT_BASE_ID + 151, "Defeat Melon (DLC1)",
                LocCategory.TRAINER_FIGHT, required_level=95, region="Laboratory (Big City)", rule=CanReachLocation("Defeat Athena")),
    LocationDef(TRAINER_FIGHT_BASE_ID + 152, "Defeat Riona (DLC1)",
                LocCategory.TRAINER_FIGHT, required_level=95, region="Typeless Gym"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 155, "Defeat Yoru and Neru",
                LocCategory.TRAINER_FIGHT, required_level=115, region="Sand Area"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 156, "Defeat Maki (DLC1)",
                LocCategory.TRAINER_FIGHT, required_level=105, region="Big City",
                rule=(CanReachLocation("Defeat Athena") & OnScenes(CanReachLocation("Maki Scene 2 (Hot Spring XXX)")))),
    LocationDef(TRAINER_FIGHT_BASE_ID + 157, "Defeat Murasaki (DLC1)",
                LocCategory.TRAINER_FIGHT, required_level=95, region="Beach Road", rule=CanReachLocation("Defeat Athena")),
    LocationDef(TRAINER_FIGHT_BASE_ID + 163, "Defeat Nene (DLC2)",
                LocCategory.TRAINER_FIGHT, required_level=115, region="Resort", rule=CanReachLocation("Defeat Tama")),
    LocationDef(TRAINER_FIGHT_BASE_ID + 165, "Defeat Marisa (DLC1)",
                LocCategory.TRAINER_FIGHT, required_level=100, region="Central Church 2F", rule=CanReachLocation("Defeat Athena")),
    LocationDef(TRAINER_FIGHT_BASE_ID + 167, "Defeat Rumi (DLC1)",
                LocCategory.TRAINER_FIGHT, required_level=95, region="Harbor Town",
                rule=(CanReachLocation("Defeat Athena") & CanReachRegion("Dojo"))),
    LocationDef(TRAINER_FIGHT_BASE_ID + 173, "Defeat Taiga (DLC2)",
                LocCategory.TRAINER_FIGHT, required_level=115, region="Coastline Area",
                rule=CanReachLocation("Defeat Tama")),
    LocationDef(TRAINER_FIGHT_BASE_ID + 174, "Defeat Minako (DLC1)",
                LocCategory.TRAINER_FIGHT, required_level=95, region="Pool", rule=CanReachLocation("Defeat Athena")),
    LocationDef(TRAINER_FIGHT_BASE_ID + 182, "Defeat Akira (DLC2)",
                LocCategory.TRAINER_FIGHT, required_level=115, region="Deep Forest Area",
                rule=CanReachLocation("Defeat Tama")),
    LocationDef(TRAINER_FIGHT_BASE_ID + 183, "Defeat Kanako (DLC1)",
                LocCategory.TRAINER_FIGHT, required_level=95, region="Cave Road", rule=CanReachLocation("Defeat Athena")),
    LocationDef(TRAINER_FIGHT_BASE_ID + 193, "Defeat Nanase (DLC1)",
                LocCategory.TRAINER_FIGHT, required_level=95, region="Dojo", rule=CanReachLocation("Defeat Athena")),
    LocationDef(TRAINER_FIGHT_BASE_ID + 200, "Defeat Murei (DLC1)",
                LocCategory.TRAINER_FIGHT, required_level=95, region="Shrine", rule=CanReachLocation("Defeat Athena")),
    LocationDef(TRAINER_FIGHT_BASE_ID + 201, "Defeat Aya (DLC2)",
                LocCategory.TRAINER_FIGHT, required_level=95, region="Lake", rule=CanReachLocation("Defeat Tama")),
    LocationDef(TRAINER_FIGHT_BASE_ID + 204, "Defeat Hikari (DLC1)",
                LocCategory.TRAINER_FIGHT, required_level=110, region="Wano Village",
                rule=(CanReachLocation("Defeat Athena") & OnScenes(CanReachLocation("Luna Scene 4 (Mother and Daughter 3some)")) & Has("Matsutake"))),
    LocationDef(TRAINER_FIGHT_BASE_ID + 205, "Defeat Leo (DLC1)",
                LocCategory.TRAINER_FIGHT, required_level=110, region="Forest of Trials",
                rule=(CanReachLocation("Defeat Athena") & OnScenes(CanReachLocation("Leo Scene 3 (Pool XXX)")) & Has("5000 Yen Swimsuit Voucher 1"))),
    LocationDef(TRAINER_FIGHT_BASE_ID + 207, "Defeat Lisa",
                LocCategory.TRAINER_FIGHT, required_level=105, region="Resort"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 208, "Defeat Sophia (DLC2)",
                LocCategory.TRAINER_FIGHT, required_level=105, region="Resort"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 209, "Defeat Hiroko",
                LocCategory.TRAINER_FIGHT, required_level=105, region="Hotel Lobby"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 210, "Defeat Hibana (DLC2)",
                LocCategory.TRAINER_FIGHT, required_level=105, region="Harbor Gym", rule=CanReachLocation("Defeat Athena")),
    LocationDef(TRAINER_FIGHT_BASE_ID + 211, "Defeat Ero-doujin Sensei",
                LocCategory.TRAINER_FIGHT, required_level=115, region="Ero Doujin Building"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 212, "Defeat Meena (DLC2)",
                LocCategory.TRAINER_FIGHT, required_level=105, region="Makina Ranch", rule=CanReachLocation("Defeat Athena")),
    LocationDef(TRAINER_FIGHT_BASE_ID + 213, "Defeat Shishio (DLC2)",
                LocCategory.TRAINER_FIGHT, required_level=105, region="Wano Village", rule=CanReachLocation("Defeat Athena")),
    LocationDef(TRAINER_FIGHT_BASE_ID + 214, "Defeat Anna (DLC2)",
                LocCategory.TRAINER_FIGHT, required_level=105, region="Resort"),
    LocationDef(TRAINER_FIGHT_BASE_ID + 221, "Defeat Nupuryu",
                LocCategory.TRAINER_FIGHT, required_level=135, region="Monthly 3F"),
]

LEVEL_GRANTS: list[LocationDef] = [
    # --- Sunglasses Mushrooms ---
    LocationDef(LEVEL_GRANT_BASE_ID + 0, "Level Mushroom - Hajime Road",
                LocCategory.LEVEL_GRANT, region="Hajime Road"),
    LocationDef(LEVEL_GRANT_BASE_ID + 1, "Level Mushroom - City Road",
                LocCategory.LEVEL_GRANT, region="City Road"),
    LocationDef(LEVEL_GRANT_BASE_ID + 2, "Level Mushroom - Wano Village",
                LocCategory.LEVEL_GRANT, region="Wano Village"),
    LocationDef(LEVEL_GRANT_BASE_ID + 3, "Level Mushroom - Harbor Town",
                LocCategory.LEVEL_GRANT, region="Harbor Town"),
    LocationDef(LEVEL_GRANT_BASE_ID + 4, "Level Mushroom - Central Road",
                LocCategory.LEVEL_GRANT, region="Central Road"),
    LocationDef(LEVEL_GRANT_BASE_ID + 5, "Level Mushroom - Lava Hideout",
                LocCategory.LEVEL_GRANT, region="Lava Hideout"),
    LocationDef(LEVEL_GRANT_BASE_ID + 6, "Level Mushroom - Inlet Hideout",
                LocCategory.LEVEL_GRANT, region="Inlet Hideout"),
    LocationDef(LEVEL_GRANT_BASE_ID + 7, "Level Mushroom - Forest Hideout",
                LocCategory.LEVEL_GRANT, region="Forest Hideout"),

    # --- Secret Shop Mushrooms ---
    LocationDef(LEVEL_GRANT_BASE_ID + 10, "Secret Shop Mushroom (10K)",
                LocCategory.LEVEL_GRANT, region="Secret Shop",
                rule=CanReachLocation("Defeat White God")),
    LocationDef(LEVEL_GRANT_BASE_ID + 11, "Secret Shop Mushroom (50K)",
                LocCategory.LEVEL_GRANT, region="Secret Shop",
                rule=(CanReachLocation("Defeat Athena") & CanReachLocation("Secret Shop Mushroom (10K)"))),

    # --- Men's Bath reward (Map 165) ---
    LocationDef(LEVEL_GRANT_BASE_ID + 20, "Men's Bath Reward",
                LocCategory.LEVEL_GRANT, region="Mens Bath"),

    # --- Jizo Set Complete ---
    # Level granted on speaking to all 10 Jizo. Last accessible one is in Forest of Trials.
    LocationDef(LEVEL_GRANT_BASE_ID + 30, "Jizo Set Complete",
                LocCategory.LEVEL_GRANT, region="Forest of Trials", rule=CanReachRegion("Wano Village") & CanReachRegion("Harbor Town")),

    # --- After White God three levels are granted. ---
    LocationDef(LEVEL_GRANT_BASE_ID + 40, "ED Setup Level 1",
                LocCategory.LEVEL_GRANT, region="Post-ED"),
    LocationDef(LEVEL_GRANT_BASE_ID + 41, "ED Setup Level 2",
                LocCategory.LEVEL_GRANT, region="Post-ED"),
    LocationDef(LEVEL_GRANT_BASE_ID + 42, "ED Setup Level 3",
                LocCategory.LEVEL_GRANT, region="Post-ED"),
]


def extra_shop_locations(count: int) -> list[LocationDef]:
    """Distribute `count` AP slots across shops.
    Phase 1: Round-robin while respecting each shop's preferred `cap`. This
    keeps all additions visible in the UI.
    Phase 2: Once every shop has hit its cap but `count` is still
    > 0, keep distributing one per shop per pass. Shops will exceed their
    ability to display items, but they will still be accessible.
    """
    if count <= 0:
        return []

    out: list[LocationDef] = []
    filled = [0] * len(AP_PURCHASE_SLOTS)
    next_id = 0

    def _place(i: int) -> None:
        nonlocal next_id
        region, _cap, label = AP_PURCHASE_SLOTS[i]
        filled[i] += 1
        out.append(LocationDef(
            EXTRA_SHOP_BASE_ID + next_id,
            f"{label} — AP Slot {filled[i]}",
            LocCategory.EXTRA_SHOP,
            region=region,
        ))
        next_id += 1

    # Phase 1: Respect slot limits.
    while count > 0:
        progress = False
        for i, (_region, cap, _label) in enumerate(AP_PURCHASE_SLOTS):
            if count <= 0:
                break
            if filled[i] >= cap:
                continue
            _place(i)
            count -= 1
            progress = True
        if not progress:
            break

    # Phase 2: Slots exhausted, keep distributing evenly.
    while count > 0:
        for i in range(len(AP_PURCHASE_SLOTS)):
            if count <= 0:
                break
            _place(i)
            count -= 1

    return out


PICKUPS: list[LocationDef] = [
    # --- Big City (gated by Defeat Leo) ---
    LocationDef(PICKUP_BASE_ID + 0, "Chest - Big City (Star Disk)",
                LocCategory.PICKUP, region="Big City"),
    LocationDef(PICKUP_BASE_ID + 1, "Chest - Big City (Rec. Castella)",
                LocCategory.PICKUP, region="Big City"),
    LocationDef(PICKUP_BASE_ID + 2, "Hidden 5000 Yen - Big City",
                LocCategory.PICKUP, region="Big City"),

    # --- Hajime Road ---
    LocationDef(PICKUP_BASE_ID + 3, "Chest - Hajime Road (Recovery Beans)",
                LocCategory.PICKUP, region="Hajime Road"),

    # --- Cave Road ---
    LocationDef(PICKUP_BASE_ID + 4, "Chest - Cave Road (Energy Mushroom)",
                LocCategory.PICKUP, region="Cave Road"),

    # --- Wano Mountain Cave 1F ---
    LocationDef(PICKUP_BASE_ID + 5, "Chest - Wano Mountain Cave 1F (Attack-ola)",
                LocCategory.PICKUP, region="Wano Mountain Cave 1F"),
    LocationDef(PICKUP_BASE_ID + 6, "Chest - Wano Mountain Cave 1F (Full Tank Soup)",
                LocCategory.PICKUP, region="Wano Mountain Cave 1F"),
    LocationDef(PICKUP_BASE_ID + 7, "Chest - Wano Mountain Cave 1F (Rec. Castella)",
                LocCategory.PICKUP, region="Wano Mountain Cave 1F"),

    # --- Wano Mountain Cave B1F ---
    LocationDef(PICKUP_BASE_ID + 8, "Chest - Wano Mountain Cave B1F (Full Tank Soup)",
                LocCategory.PICKUP, region="Wano Mountain Cave B1F"),

    # --- Harbor Town ---
    LocationDef(PICKUP_BASE_ID + 9, "Hidden 5000 Yen - Harbor Town",
                LocCategory.PICKUP, region="Harbor Town"),
    LocationDef(PICKUP_BASE_ID + 10, "Chest - Harbor Town (Energy Mushroom)",
                LocCategory.PICKUP, region="Harbor Town"),
    LocationDef(PICKUP_BASE_ID + 11, "Chest - Harbor Town (Full Tank Soup)",
                LocCategory.PICKUP, region="Harbor Town"),

    # --- Central Road ---
    LocationDef(PICKUP_BASE_ID + 12, "Chest - Central Road (Full Tank Soup)",
                LocCategory.PICKUP, region="City Road"),

    # --- Protagonist's House Basement ---
    LocationDef(PICKUP_BASE_ID + 13, "Hidden Item - Basement (Repel Incense)",
                LocCategory.PICKUP, region="Protagonists House Basement"),
    LocationDef(PICKUP_BASE_ID + 14, "Hidden Item - Basement (Foamy Detergent)",
                LocCategory.PICKUP, region="Protagonists House Basement"),

    # --- Holy Road ---
    LocationDef(PICKUP_BASE_ID + 15, "Chest - Holy Road (Energy Mushroom)",
                LocCategory.PICKUP, region="Holy Road"),

    # --- Construction Site Office ---
    LocationDef(PICKUP_BASE_ID + 16, "Chest - Construction Site Office (Repel Incense)",
                LocCategory.PICKUP, region="Construction Site Office"),

    # --- DLC2 ---
    LocationDef(PICKUP_BASE_ID + 17, "Chest - Sand Area (Full Tank Soup) #1",
                LocCategory.PICKUP, region="Sand Area"),
    LocationDef(PICKUP_BASE_ID + 18, "Chest - Sand Area (Full Tank Soup) #2",
                LocCategory.PICKUP, region="Sand Area"),
    LocationDef(PICKUP_BASE_ID + 19, "Chest - Coastline Area (Full Tank Soup)",
                LocCategory.PICKUP, region="Coastline Area"),
]

KEY_PICKUPS: list[LocationDef] = [
    LocationDef(EVENT_PICKUP_BASE_ID + 31, "VIP Card",
                LocCategory.EVENT_PICKUP, region="Tea House"),
]

EVENT_PURCHASES: list[LocationDef] = [
    # --- Lucky Besuke Reception  ---
    LocationDef(EVENT_PURCHASE_BASE_ID + 50, "Buy 5000 Yen Swimsuit Voucher 1",
                LocCategory.EVENT_PURCHASE, region="Lucky Besuke Reception",
                rule=CanReachLocation("Defeat White God")),
    LocationDef(EVENT_PURCHASE_BASE_ID + 51, "Buy 20000 Yen Swimsuit Voucher",
                LocCategory.EVENT_PURCHASE, region="Lucky Besuke Reception",
                rule=CanReachLocation("Defeat White God")),
    LocationDef(EVENT_PURCHASE_BASE_ID + 52, "Buy All Swimsuit Voucher",
                LocCategory.EVENT_PURCHASE, region="Lucky Besuke Reception",
                rule=CanReachLocation("Defeat White God")),
    LocationDef(EVENT_PURCHASE_BASE_ID + 54, "Buy 5000 Yen Swimsuit Voucher 2",
                LocCategory.EVENT_PURCHASE, region="Lucky Besuke Reception",
                rule=CanReachLocation("Defeat White God")),

    # --- Secret Shop ---
    LocationDef(EVENT_PURCHASE_BASE_ID + 41, "Buy Book of Shinobi",
                LocCategory.EVENT_PURCHASE, region="Secret Shop"),
    LocationDef(EVENT_PURCHASE_BASE_ID + 42, "Buy Strange Medicine",
                LocCategory.EVENT_PURCHASE, region="Secret Shop"),
    LocationDef(EVENT_PURCHASE_BASE_ID + 43, "Buy Electric Anal Vibe",
                LocCategory.EVENT_PURCHASE, region="Secret Shop"),
    LocationDef(EVENT_PURCHASE_BASE_ID + 44, "Buy Reserved Bath Ticket 1",
                LocCategory.EVENT_PURCHASE, region="Secret Shop"),
    LocationDef(EVENT_PURCHASE_BASE_ID + 45, "Buy Reserved Bath Ticket 2",
                LocCategory.EVENT_PURCHASE, region="Secret Shop"),
    LocationDef(EVENT_PURCHASE_BASE_ID + 46, "Buy Reserved Bath Ticket 3",
                LocCategory.EVENT_PURCHASE, region="Secret Shop"),
    LocationDef(EVENT_PURCHASE_BASE_ID + 47, "Buy Nose Hook",
                LocCategory.EVENT_PURCHASE, region="Secret Shop"),
    LocationDef(EVENT_PURCHASE_BASE_ID + 53, "Buy 20000 Yen Swimsuit Voucher Back",
                LocCategory.EVENT_PURCHASE, region="Secret Shop"),
    # Matsutake stocks after Luna hot-spring (sw 387, set by Luna Scene 3
    # which requires Reserved Bath Ticket 1) + Aoi Best Couple Contest
    # (sw 384, set by Aoi Scene 2 which requires both All Swimsuit Voucher
    # and 20000 Yen Swimsuit Voucher Back).
    LocationDef(EVENT_PURCHASE_BASE_ID + 56, "Buy Matsutake",
                LocCategory.EVENT_PURCHASE, region="Secret Shop",
                rule=(OnScenes(CanReachLocation("Luna Scene 3 (Hot Spring XXX)")) & OnScenes(CanReachLocation("Aoi Scene 2 (Pool 3some)")) & Has("Reserved Bath Ticket 1") & Has("All Swimsuit Voucher") & Has("20000 Yen Swimsuit Voucher Back"))),
    # Wonderful Spray stocks after the Leo swimsuit event (sw 369), which is
    # Leo Scene 3 — itself requires the 5000 Yen Swimsuit Voucher 1.
    LocationDef(EVENT_PURCHASE_BASE_ID + 57, "Buy Wonderful Spray",
                LocCategory.EVENT_PURCHASE, region="Secret Shop",
                rule=(OnScenes(CanReachLocation("Leo Scene 3 (Pool XXX)")) & Has("5000 Yen Swimsuit Voucher 1"))),

    # --- Resort Shop ---
    LocationDef(EVENT_PURCHASE_BASE_ID + 38, "Buy Super Ball",
                LocCategory.EVENT_PURCHASE, region="Resort"),
    LocationDef(EVENT_PURCHASE_BASE_ID + 39, "Buy White Fluff",
                LocCategory.EVENT_PURCHASE, region="Resort"),
]

SCENES: list[LocationDef] = [
    # --- Hikari (5 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 0, "Hikari Scene 1 (The First XXX)",
                LocCategory.SCENE_UNLOCK, region="Hajime Village",
                rule=CanReachLocation("Defeat Hikari")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 1, "Hikari Scene 2 (Wano Town XXX)",
                LocCategory.SCENE_UNLOCK, region="Wano Village",
                rule=CanReachLocation("Defeat Hikari (Wano)")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 2, "Hikari Scene 3 (Home XXX)",
                LocCategory.SCENE_UNLOCK, region="Hikari's House"),
    LocationDef(SCENE_UNLOCK_BASE_ID + 3, "Hikari Scene 4 (DLC1 - Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Wano Village",
                rule=CanReachLocation("Defeat Hikari (DLC1)")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 4, "Hikari Scene 5 (DLC2 - Small road XXX)",
                LocCategory.SCENE_UNLOCK, region="Hajime Forest Path",
                rule=(OnScenes(CanReachLocation("Hikari Scene 1 (The First XXX)")) & OnScenes(CanReachLocation("Hikari Scene 2 (Wano Town XXX)")) & OnScenes(CanReachLocation("Hikari Scene 3 (Home XXX)")) & OnScenes(CanReachLocation("Hikari Scene 4 (DLC1 - Victory XXX)")))),

    # --- Leo (6 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 10, "Leo Scene 1 (Harbor Town Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Harbor Town",
                rule=CanReachLocation("Defeat Leo (Harbor)")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 11, "Leo Scene 2 (Forest Rest Stop XXX)",
                LocCategory.SCENE_UNLOCK, region="Forest of Trials",
                rule=CanReachLocation("Defeat Leo (Forest of Trials)")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 12, "Leo Scene 3 (Pool XXX)",
                LocCategory.SCENE_UNLOCK, region="Pool",
                rule=(CanReachLocation("Defeat White God") & Has("5000 Yen Swimsuit Voucher 1"))),
    LocationDef(SCENE_UNLOCK_BASE_ID + 13, "Leo Scene 4 (DLC1 - Love Chat Meeting)",
                LocCategory.SCENE_UNLOCK, region="Big City",
                rule=(CanReachLocation("Defeat Athena") & OnScenes(CanReachLocation("Luna Scene 4 (Mother and Daughter 3some)")) & OnScenes(CanReachLocation("Flare Scene 2 (With my partner...)")) & Has("Matsutake"))),
    LocationDef(SCENE_UNLOCK_BASE_ID + 14, "Leo Scene 5 (DLC1 - Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Forest of Trials",
                rule=CanReachLocation("Defeat Leo (DLC1)")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 15, "Leo Scene 6 (I'll also do it!)",
                LocCategory.SCENE_UNLOCK, region="Resort",
                rule=(Has("Super Ball") & CanReachLocation("Defeat Tama"))),

    # --- Sanae (2 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 20, "Sanae Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Hajime Village",
                rule=CanReachLocation("Defeat Sanae")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 21, "Sanae Scene 2 (DLC1 - Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Hajime Village",
                rule=CanReachLocation("Defeat Sanae (DLC1)")),

    # --- Yuna (1 scene) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 30, "Yuna Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Hajime Road",
                rule=CanReachLocation("Defeat Yuna")),

    # --- Sumire (1 scene) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 40, "Sumire Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Hajime Road",
                rule=CanReachLocation("Defeat Sumire")),

    # --- Hotaru (2 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 50, "Hotaru Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Hajime Road",
                rule=CanReachLocation("Defeat Hotaru")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 51, "Hotaru Scene 2 (DLC1 - Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Hajime Road",
                rule=CanReachLocation("Defeat Hotaru (DLC1)")),

    # --- Honoka (2 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 60, "Honoka Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Hajime Road",
                rule=CanReachLocation("Defeat Honoka")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 61, "Honoka Scene 2 (DLC1 - Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Big City",
                rule=CanReachLocation("Defeat Honoka (DLC1)")),

    # --- Riona (2 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 70, "Riona Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Typeless Gym",
                rule=CanReachLocation("Defeat Riona")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 71, "Riona Scene 2 (DLC1 - Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Typeless Gym",
                rule=CanReachLocation("Defeat Riona (DLC1)")),

    # --- Natsumi (3 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 80, "Natsumi Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Big City",
                rule=CanReachLocation("Defeat Natsumi")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 81, "Natsumi Scene 2 (Urine)",
                LocCategory.SCENE_UNLOCK, region="Big City",
                rule=(CanReachLocation("Dream 3 Complete") & OnScenes(CanReachLocation("Natsumi Scene 1 (Victory XXX)")))),
    LocationDef(SCENE_UNLOCK_BASE_ID + 82, "Natsumi Scene 3 (Intimacy)",
                LocCategory.SCENE_UNLOCK, region="Big City",
                rule=(CanReachLocation("Defeat White God") & OnScenes(CanReachLocation("Natsumi Scene 2 (Urine)")))),

    # --- Kurumi (1 scene) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 90, "Kurumi Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="City Road",
                rule=CanReachLocation("Defeat Kurumi")),

    # --- Meena (2 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 100, "Meena Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Makina Ranch",
                rule=CanReachLocation("Defeat Meena")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 101, "Meena Scene 2 (DLC2 - Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Makina Ranch",
                rule=CanReachLocation("Defeat Meena (DLC2)")),

    # --- Emily (1 scene) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 110, "Emily Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Makina Ranch",
                rule=CanReachLocation("Defeat Emily")),

    # --- Nene (2 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 120, "Nene Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Holy Road",
                rule=CanReachLocation("Defeat Nene")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 121, "Nene Scene 2 (DLC2 - Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Resort",
                rule=CanReachLocation("Defeat Nene (DLC2)")),

    # --- Armin (1 scene) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 130, "Armin Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Central Church",
                rule=CanReachLocation("Defeat Armin")),

    # --- Marisa (2 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 140, "Marisa Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Central Church 2F",
                rule=CanReachLocation("Defeat Marisa")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 141, "Marisa Scene 2 (DLC1 - Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Central Church 2F",
                rule=CanReachLocation("Defeat Marisa (DLC1)")),

    # --- Murasaki (2 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 150, "Murasaki Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Beach Road",
                rule=CanReachLocation("Defeat Murasaki")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 151, "Murasaki Scene 2 (DLC1 - Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Beach Road",
                rule=CanReachLocation("Defeat Murasaki (DLC1)")),

    # --- Fran (1 scene) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 160, "Fran Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Beach Road",
                rule=CanReachLocation("Defeat Fran")),

    # --- Akari (1 scene) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 170, "Akari Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Harbor Town",
                rule=CanReachLocation("Defeat Akari")),

    # --- Marin (1 scene) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 180, "Marin Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Harbor Town",
                rule=CanReachLocation("Defeat Marin")),

    # --- Mei (1 scene) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 190, "Mei Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Harbor Gym",
                rule=CanReachLocation("Defeat Mei")),

    # --- Hibana (2 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 200, "Hibana Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Harbor Gym",
                rule=CanReachLocation("Defeat Hibana")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 201, "Hibana Scene 2 (What I'm good at)",
                LocCategory.SCENE_UNLOCK, region="Harbor Gym",
                rule=CanReachLocation("Defeat Hibana (DLC2)")),

    # --- Minako (2 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 210, "Minako Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Pool",
                rule=CanReachLocation("Defeat Minako")),
    # Scene 2 fires before the DLC1 battle — only Champion gate.
    LocationDef(SCENE_UNLOCK_BASE_ID + 211, "Minako Scene 2 (DLC1 - Crime?)",
                LocCategory.SCENE_UNLOCK, region="Pool",
                rule=CanReachLocation("Defeat Athena")),

    # --- Tina (2 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 220, "Tina Scene 1 (Lucky Pervert!)",
                LocCategory.SCENE_UNLOCK, region="Pool"),
    LocationDef(SCENE_UNLOCK_BASE_ID + 221, "Tina Scene 2 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Pool",
                rule=CanReachLocation("Defeat Tina")),

    # --- Tamaki (2 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 230, "Tamaki Scene 1 (Lucky Pervert!)",
                LocCategory.SCENE_UNLOCK, region="Pool"),
    LocationDef(SCENE_UNLOCK_BASE_ID + 231, "Tamaki Scene 2 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Pool",
                rule=CanReachLocation("Defeat Tamaki")),

    # --- Haruka (1 scene) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 240, "Haruka Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Tea House",
                rule=CanReachLocation("Defeat Haruka")),

    # --- Yume (2 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 250, "Yume Scene 1 (Secret Hospitality 1)",
                LocCategory.SCENE_UNLOCK, region="Tea House Special Room"),
    LocationDef(SCENE_UNLOCK_BASE_ID + 251, "Yume Scene 2 (Secret Hospitality 2)",
                LocCategory.SCENE_UNLOCK, region="Tea House Special Room",
                rule=OnScenes(CanReachLocation("Yume Scene 1 (Secret Hospitality 1)"))),

    # --- Kanata (2 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 260, "Kanata Scene 1 (You reap what you sow)",
                LocCategory.SCENE_UNLOCK, region="Tea House Special Room",
                rule=(CanReachLocation("Defeat White God") & Has("Electric Anal Vibe"))),
    LocationDef(SCENE_UNLOCK_BASE_ID + 261, "Kanata Scene 2 (Dance Debut)",
                LocCategory.SCENE_UNLOCK, region="Tea House Special Room",
                rule=(OnScenes(CanReachLocation("Kanata Scene 1 (You reap what you sow)")) & Has("Electric Anal Vibe"))),

    # --- Jill (2 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 270, "Jill Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Hajime Road",
                rule=CanReachLocation("Defeat Jill")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 271, "Jill Scene 2 (In the Ruins)",
                LocCategory.SCENE_UNLOCK, region="Ruins (Cleared)",
                rule=CanReachLocation("Defeat White God")),

    # --- Melon (2 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 280, "Melon Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Laboratory (Big City)",
                rule=CanReachLocation("Defeat Melon")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 281, "Melon Scene 2 (DLC1 - Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Laboratory (Big City)",
                rule=CanReachLocation("Defeat Melon (DLC1)")),

    # --- Marble (1 scene) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 290, "Marble Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Yarimon Center (Wano Village)",
                rule=CanReachLocation("Defeat Marble")),

    # --- Kanako (2 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 300, "Kanako Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Cave Road",
                rule=CanReachLocation("Defeat Kanako")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 301, "Kanako Scene 2 (DLC1 - Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Cave Road",
                rule=CanReachLocation("Defeat Kanako (DLC1)")),

    # --- Totoro (3 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 310, "Totoro Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Keidai Road A",
                rule=CanReachLocation("Defeat Totoro")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 311, "Totoro Scene 2 (Cultist Welcome)",
                LocCategory.SCENE_UNLOCK, region="Ruins",
                rule=CanReachLocation("Defeat Totoro")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 312, "Totoro Scene 3 (Anal Ninjutsu)",
                LocCategory.SCENE_UNLOCK, region="Keidai Road A",
                rule=(CanReachLocation("Defeat White God") & Has("Book of Shinobi"))),

    # --- Shishio (3 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 320, "Shishio Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Wano Village",
                rule=CanReachLocation("Defeat Shishio")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 321, "Shishio Scene 2 (Hot Spring Peeping)",
                LocCategory.SCENE_UNLOCK, region="Bath House"),
    LocationDef(SCENE_UNLOCK_BASE_ID + 322, "Shishio Scene 3 (DLC2 - Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Wano Village",
                rule=CanReachLocation("Defeat Shishio (DLC2)")),

    # --- Chie (1 scene) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 330, "Chie Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Wano Village",
                rule=CanReachLocation("Defeat Chie")),

    # --- Anna (2 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 340, "Anna Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Wano Village",
                rule=CanReachLocation("Defeat Anna")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 341, "Anna Scene 2 (DLC2 - Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Resort",
                rule=CanReachLocation("Defeat Anna (DLC2)")),

    # --- Phineh (1 scene) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 350, "Phineh Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Wano Village School",
                rule=CanReachLocation("Defeat Phineh")),

    # --- Nanase (2 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 360, "Nanase Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Dojo",
                rule=CanReachLocation("Defeat Nanase")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 361, "Nanase Scene 2 (DLC1 - Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Dojo",
                rule=CanReachLocation("Defeat Nanase (DLC1)")),

    # --- Kurohime (2 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 370, "Kurohime Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Wano Village",
                rule=CanReachLocation("Defeat Kurohime")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 371, "Kurohime Scene 2 (Mansion 3some)",
                LocCategory.SCENE_UNLOCK, region="Wano Village Hut",
                rule=(CanReachLocation("Defeat White God") & CanReachLocation("Defeat Kurohime") & CanReachLocation("Defeat Momohime"))),

    # --- Momohime (2 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 380, "Momohime Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Wano Village",
                rule=CanReachLocation("Defeat Momohime")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 381, "Momohime Scene 2 (Mansion 3some)",
                LocCategory.SCENE_UNLOCK, region="Wano Village Hut",
                rule=(CanReachLocation("Defeat White God") & CanReachLocation("Defeat Kurohime") & CanReachLocation("Defeat Momohime"))),

    # --- Sofia (2 scenes; trainer is named "Sophia" in trainer list) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 390, "Sofia Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Shrine",
                rule=CanReachLocation("Defeat Sophia")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 391, "Sofia Scene 2 (DLC2 - Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Resort",
                rule=CanReachLocation("Defeat Sophia (DLC2)")),

    # --- Murei (3 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 400, "Murei Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Shrine",
                rule=CanReachLocation("Defeat Murei")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 401, "Murei Scene 2 (DLC1 - Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Shrine",
                rule=CanReachLocation("Defeat Murei (DLC1)")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 402, "Murei Scene 3 (DLC1 - Evil Spirits, Begone!)",
                LocCategory.SCENE_UNLOCK, region="Wano Village",
                rule=OnScenes(CanReachLocation("Murei Scene 2 (DLC1 - Victory XXX)"))),

    # --- Sara (3 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 410, "Sara Scene 1 (OPPAI!)",
                LocCategory.SCENE_UNLOCK, region="Shrine"),
    LocationDef(SCENE_UNLOCK_BASE_ID + 411, "Sara Scene 2 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Shrine",
                rule=CanReachLocation("Defeat Sara")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 412, "Sara Scene 3 (DLC1 - Repaying with your body)",
                LocCategory.SCENE_UNLOCK, region="Shrine",
                rule=(CanReachLocation("Defeat Athena") & CanReachLocation("Defeat Sara"))),

    # --- Aoi (4 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 420, "Aoi Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Shrine",
                rule=CanReachLocation("Defeat Aoi")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 421, "Aoi Scene 2 (Pool 3some)",
                LocCategory.SCENE_UNLOCK, region="Pool",
                rule=(CanReachLocation("Defeat White God") & Has("All Swimsuit Voucher") & Has("20000 Yen Swimsuit Voucher Back"))),
    LocationDef(SCENE_UNLOCK_BASE_ID + 422, "Aoi Scene 3 (Anal Licking Handjob)",
                LocCategory.SCENE_UNLOCK, region="Shrine",
                rule=CanReachLocation("Defeat White God")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 423, "Aoi Scene 4 (Flirty Love XXX)",
                LocCategory.SCENE_UNLOCK, region="Resort",
                rule=CanReachLocation("Defeat Tama")),

    # --- Shiryu (3 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 430, "Shiryu Scene 1 (Masturbation)",
                LocCategory.SCENE_UNLOCK, region="Bath House",
                rule=CanReachLocation("Defeat Shiryu")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 431, "Shiryu Scene 2 (Seeing through)",
                LocCategory.SCENE_UNLOCK, region="Bath House",
                rule=CanReachLocation("Defeat Shiryu")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 432, "Shiryu Scene 3 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Bath House",
                rule=CanReachLocation("Defeat Shiryu")),

    # --- Linlin (1 scene; trainer is "Rinrin" in the trainer list) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 440, "Linlin Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Wano Road",
                rule=CanReachLocation("Defeat Rinrin")),

    # --- Rumi (2 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 450, "Rumi Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Harbor Town",
                rule=CanReachLocation("Defeat Rumi")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 451, "Rumi Scene 2 (DLC1 - Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Wano Village",
                rule=CanReachLocation("Defeat Rumi (DLC1)")),

    # --- Maho (2 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 460, "Maho Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Hajime Village",
                rule=CanReachLocation("Defeat Maho")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 461, "Maho Scene 2 (DLC1 - Forceful Kiss)",
                LocCategory.SCENE_UNLOCK, region="Hajime Village",
                rule=(CanReachLocation("Defeat Athena") & CanReachLocation("Defeat Maho"))),

    # --- Kuina (2 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 470, "Kuina Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Hajime Village",
                rule=CanReachLocation("Defeat Kuina")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 471, "Kuina Scene 2 (DLC1 - Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Hajime Village",
                rule=CanReachLocation("Defeat Kuina (DLC1)")),

    # --- Luna (6 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 480, "Luna Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Laboratory",
                rule=CanReachLocation("Defeat Luna")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 481, "Luna Scene 2 (Masturbation Peeping)",
                LocCategory.SCENE_UNLOCK, region="Laboratory Left",
                rule=CanReachLocation("Defeat Luna")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 482, "Luna Scene 3 (Hot Spring XXX)",
                LocCategory.SCENE_UNLOCK, region="Bath House",
                rule=(CanReachLocation("Defeat White God") & Has("Reserved Bath Ticket 1"))),
    LocationDef(SCENE_UNLOCK_BASE_ID + 483, "Luna Scene 4 (Mother and Daughter 3some)",
                LocCategory.SCENE_UNLOCK, region="Laboratory",
                rule=Has("Matsutake")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 484, "Luna Scene 5 (Titjob)",
                LocCategory.SCENE_UNLOCK, region="Laboratory Left",
                rule=(OnScenes(CanReachLocation("Luna Scene 4 (Mother and Daughter 3some)")) & Has("Matsutake"))),
    LocationDef(SCENE_UNLOCK_BASE_ID + 485, "Luna Scene 6 (Mother and Daughter 3some Pt.2)",
                LocCategory.SCENE_UNLOCK, region="Resort",
                rule=(CanReachLocation("Defeat Tama") & OnScenes(CanReachLocation("Hikari Scene 5 (DLC2 - Small road XXX)")) & OnScenes(CanReachLocation("Luna Scene 5 (Titjob)")) & Has("All Swimsuit Voucher") & Has("20000 Yen Swimsuit Voucher Back") & Has("Matsutake"))),

    # --- Vritra (3 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 490, "Vritra Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Central Church 2F",
                rule=CanReachLocation("Defeat Vritra")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 491, "Vritra Scene 2 (Breast Groping)",
                LocCategory.SCENE_UNLOCK, region="Central Church 2F",
                rule=CanReachLocation("Defeat Vritra")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 492, "Vritra Scene 3 (Rejuvenation Tricks)",
                LocCategory.SCENE_UNLOCK, region="Central Church 2F",
                rule=(CanReachLocation("Defeat White God") & Has("Strange Medicine"))),

    # --- Maki (4 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 500, "Maki Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Big City",
                rule=CanReachLocation("Defeat Maki")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 501, "Maki Scene 2 (Hot Spring XXX)",
                LocCategory.SCENE_UNLOCK, region="Bath House",
                rule=(CanReachLocation("Defeat White God") & Has("Reserved Bath Ticket 3"))),
    LocationDef(SCENE_UNLOCK_BASE_ID + 502, "Maki Scene 3 (DLC1 - Study Session XXX)",
                LocCategory.SCENE_UNLOCK, region="Big City",
                rule=CanReachLocation("Defeat Maki (DLC1)")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 503, "Maki Scene 4 (DLC2 - Video Shooting)",
                LocCategory.SCENE_UNLOCK, region="Hotel Lobby",
                rule=CanReachLocation("Defeat Tama")),

    # --- Aya (4 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 510, "Aya Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Ruins",
                rule=CanReachLocation("Defeat Aya")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 511, "Aya Scene 2 (Cultist Beverage)",
                LocCategory.SCENE_UNLOCK, region="Ruins",
                rule=CanReachLocation("Defeat Aya")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 512, "Aya Scene 3 (Toilet Mode!)",
                LocCategory.SCENE_UNLOCK, region="Ruins (Cleared)",
                rule=Has("Nose Hook")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 513, "Aya Scene 4 (DLC2 - Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Lake",
                rule=CanReachLocation("Defeat Aya (DLC2)")),

    # --- Iori (3 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 520, "Iori Scene 1 (Cultist Welcome Performance)",
                LocCategory.SCENE_UNLOCK, region="Ruins",
                rule=CanReachLocation("Defeat Aya")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 521, "Iori Scene 2 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Ryugasaki Gym",
                rule=CanReachLocation("Defeat Iori")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 522, "Iori Scene 3 (Iori & Yoru 3some)",
                LocCategory.SCENE_UNLOCK, region="Ryugasaki Gym",
                rule=(CanReachLocation("Defeat Iori") & CanReachLocation("Defeat Yoru") & OnScenes(CanReachLocation("Yoru Scene 2 (Touching...)")) & OnScenes(CanReachLocation("Neru Scene 2 (Must use it...)")))),

    # --- Taiga (3 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 530, "Taiga Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Harbor Town",
                rule=CanReachLocation("Defeat Taiga")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 531, "Taiga Scene 2 (Hot Spring XXX)",
                LocCategory.SCENE_UNLOCK, region="Bath House",
                rule=(CanReachLocation("Defeat White God") & Has("Reserved Bath Ticket 2"))),
    LocationDef(SCENE_UNLOCK_BASE_ID + 532, "Taiga Scene 3 (DLC2 - Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Coastline Area",
                rule=CanReachLocation("Defeat Taiga (DLC2)")),

    # --- Akira (4 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 540, "Akira Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Makina Ranch",
                rule=CanReachLocation("Defeat Akira")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 541, "Akira Scene 2 (At the Pool)",
                LocCategory.SCENE_UNLOCK, region="Pool",
                rule=(CanReachLocation("Defeat White God") & Has("5000 Yen Swimsuit Voucher 2"))),
    LocationDef(SCENE_UNLOCK_BASE_ID + 542, "Akira Scene 3 (Masturbation Support)",
                LocCategory.SCENE_UNLOCK, region="Makina Ranch",
                rule=CanReachLocation("Defeat White God")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 543, "Akira Scene 4 (DLC2 - Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Deep Forest Area",
                rule=CanReachLocation("Defeat Akira (DLC2)")),

    # --- Kana (1 scene) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 550, "Kana Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Tea House",
                rule=CanReachLocation("Defeat Kana")),

    # --- Hina (2 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 560, "Hina Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Tea House",
                rule=CanReachLocation("Defeat Hina")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 561, "Hina Scene 2 (Conversation in private room)",
                LocCategory.SCENE_UNLOCK, region="Tea House Special Room",
                rule=(CanReachLocation("Defeat Hina") & OnScenes(CanReachLocation("Yume Scene 1 (Secret Hospitality 1)")))),

    # --- Yoru (3 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 570, "Yoru Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Big City",
                rule=CanReachLocation("Defeat Yoru")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 571, "Yoru Scene 2 (Touching...)",
                LocCategory.SCENE_UNLOCK, region="Big City",
                rule=(CanReachLocation("Defeat Yoru") & CanReachLocation("Defeat White God"))),
    LocationDef(SCENE_UNLOCK_BASE_ID + 572, "Yoru Scene 3 (I want to serve you!)",
                LocCategory.SCENE_UNLOCK, region="Sand Area",
                rule=CanReachLocation("Defeat Yoru and Neru")),

    # --- Neru (2 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 580, "Neru Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Ryugasaki Gym",
                rule=CanReachLocation("Defeat Neru")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 581, "Neru Scene 2 (Must use it...)",
                LocCategory.SCENE_UNLOCK, region="Ryugasaki Gym Rest Area",
                rule=(CanReachLocation("Defeat Neru") & CanReachLocation("Defeat White God"))),

    # --- Mizuki (2 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 590, "Mizuki Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Harbor Town",
                rule=CanReachLocation("Defeat Mizuki")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 591, "Mizuki Scene 2 (Wonderful★Spray)",
                LocCategory.SCENE_UNLOCK, region="Secret Shop",
                rule=Has("Wonderful Spray")),

    # --- Patra (4 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 600, "Patra Scene 1 (Victory H)",
                LocCategory.SCENE_UNLOCK, region="Forest of Trials Entrance",
                rule=CanReachLocation("Defeat Patra")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 601, "Patra Scene 2 (Share it!)",
                LocCategory.SCENE_UNLOCK, region="Forest of Trials",
                rule=CanReachLocation("Defeat Athena")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 602, "Patra Scene 3 (Hitting it off)",
                LocCategory.SCENE_UNLOCK, region="Members-Only Bar",
                rule=(Has("Wonderful Spray") & OnScenes(CanReachLocation("Athena Scene 2 (Pool XXX)")) & Has("20000 Yen Swimsuit Voucher"))),
    LocationDef(SCENE_UNLOCK_BASE_ID + 603, "Patra Scene 4 (Interesting woman)",
                LocCategory.SCENE_UNLOCK, region="Hotel Lobby",
                rule=(OnScenes(CanReachLocation("Patra Scene 3 (Hitting it off)")) & CanReachLocation("Defeat Tama"))),

    # --- Opera (1 scene) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 610, "Opera Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Forest of Trials",
                rule=CanReachLocation("Defeat Opera")),

    # --- Vice (1 scene) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 620, "Vice Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Wano Mountain Cave 1F",
                rule=CanReachLocation("Defeat Vice")),

    # --- Quem (1 scene ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 630, "Quem Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Wano Mountain Cave 1F",
                rule=CanReachLocation("Defeat Quem (Cave)")),

    # --- Athena (5 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 640, "Athena Scene 1 (Victory XXX)",
                LocCategory.SCENE_UNLOCK, region="Central",
                rule=CanReachLocation("Defeat Athena")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 641, "Athena Scene 2 (Pool XXX)",
                LocCategory.SCENE_UNLOCK, region="Pool",
                rule=(CanReachLocation("Defeat Athena") & Has("20000 Yen Swimsuit Voucher"))),
    LocationDef(SCENE_UNLOCK_BASE_ID + 642, "Athena Scene 3 (Hidden Boob Job)",
                LocCategory.SCENE_UNLOCK, region="Hajime Village",
                rule=CanReachLocation("Defeat Athena")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 643, "Athena Scene 4 (Even with my butt...)",
                LocCategory.SCENE_UNLOCK, region="Hotel Lobby",
                rule=CanReachLocation("Defeat Tama")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 644, "Athena Scene 5 (Super VIP room)",
                LocCategory.SCENE_UNLOCK, region="Central",
                rule=(OnScenes(CanReachLocation("Athena Scene 2 (Pool XXX)")) & Has("20000 Yen Swimsuit Voucher"))),

    # --- Teresa (2 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 650, "Teresa Scene 1 (Boob job Invasion)",
                LocCategory.SCENE_UNLOCK, region="Central",
                rule=CanReachLocation("Defeat White God")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 651, "Teresa Scene 2 (Pussy Invasion)",
                LocCategory.SCENE_UNLOCK, region="Central",
                rule=CanReachLocation("Defeat White God")),

    # --- Flare (4 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 660, "Flare Scene 1 (Empathetic XXX)",
                LocCategory.SCENE_UNLOCK, region="Central",
                rule=CanReachLocation("Defeat White God")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 661, "Flare Scene 2 (With my partner...)",
                LocCategory.SCENE_UNLOCK, region="Central",
                rule=OnScenes(CanReachLocation("Flare Scene 1 (Empathetic XXX)"))),
    LocationDef(SCENE_UNLOCK_BASE_ID + 662, "Flare Scene 3 (DLC1 - Flirting)",
                LocCategory.SCENE_UNLOCK, region="Protagonists House",
                rule=OnScenes(CanReachLocation("Flare Scene 2 (With my partner...)"))),
    LocationDef(SCENE_UNLOCK_BASE_ID + 663, "Flare Scene 4 (DLC2 - Lovey-dovey flirting)",
                LocCategory.SCENE_UNLOCK, region="Villa Room",
                rule=(CanReachLocation("Defeat Tama") & Has("VIP Card"))),

    # --- Lisa (1 scene) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 670, "Lisa Scene 1 (Over in 5 minutes)",
                LocCategory.SCENE_UNLOCK, region="Resort",
                rule=CanReachLocation("Defeat Lisa")),

    # --- Hiroko (1 scene) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 680, "Hiroko Scene 1 (The One Who Realizes)",
                LocCategory.SCENE_UNLOCK, region="Hotel Lobby",
                rule=CanReachLocation("Defeat Hiroko")),

    # --- Ero-doujin Sensei (1 scene) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 690, "Ero-doujin Sensei Scene 1 (Ero-doujin sensei!)",
                LocCategory.SCENE_UNLOCK, region="Ero Doujin Building",
                rule=CanReachLocation("Defeat Ero-doujin Sensei")),

    # --- Tama (1 scene) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 700, "Tama Scene 1 (R18 Physical Examinations)",
                LocCategory.SCENE_UNLOCK, region="DLC2 Endgame",
                rule=(CanReachLocation("Defeat Tama") & OnScenes(CanReachLocation("Flare Scene 2 (With my partner...)")))),

    # --- Extras (3 scenes) ---
    LocationDef(SCENE_UNLOCK_BASE_ID + 710, "Extras Scene 1 (Extracurricular Activities)",
                LocCategory.SCENE_UNLOCK, region="Resort",
                rule=CanReachLocation("Defeat Tama")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 711, "Extras Scene 2 (Fleshlight Committee)",
                LocCategory.SCENE_UNLOCK, region="Resort",
                rule=CanReachLocation("Defeat Tama")),
    LocationDef(SCENE_UNLOCK_BASE_ID + 712, "Extras Scene 3 (Don't worry about it)",
                LocCategory.SCENE_UNLOCK, region="Resort",
                rule=CanReachLocation("Defeat Tama")),
]

STORY_CHECKPOINTS: list[LocationDef] = [
    LocationDef(STORY_CHECKPOINT_BASE_ID + 0, "Defeat White God",
                LocCategory.STORY_CHECKPOINT, region="Crystal Room", rule=CanReachLocation("Dream 4 Complete") & CanReachLocation("Defeat Hikari (Tournament)") & CanReachLocation("Defeat Maki (Tournament)")),
    LocationDef(STORY_CHECKPOINT_BASE_ID + 1, "Defeat Tama",
                LocCategory.STORY_CHECKPOINT, region="DLC2 Endgame", rule=CanReachLocation("Defeat Athena")),
    # Dream 1 puts you in Chapter 2
    LocationDef(STORY_CHECKPOINT_BASE_ID + 2, "Dream 1 Complete",
                LocCategory.STORY_CHECKPOINT, region="Big City", rule=CanReachLocation("Defeat Leo")),
    # Chapter 3
    LocationDef(STORY_CHECKPOINT_BASE_ID + 3, "Dream 2 Complete",
                LocCategory.STORY_CHECKPOINT, region="Central", rule=CanReachLocation("Dream 1 Complete")),
    # Chapter 4
    LocationDef(STORY_CHECKPOINT_BASE_ID + 4, "Dream 3 Complete",
                LocCategory.STORY_CHECKPOINT, region="Harbor Town",
                rule=(CanReachLocation("Defeat Hikari (Wano)") & CanReachLocation("Defeat Leo (Harbor)") & CanReachLocation("Dream 2 Complete"))),
    # Chapter 5
    LocationDef(STORY_CHECKPOINT_BASE_ID + 5, "Dream 4 Complete",
                LocCategory.STORY_CHECKPOINT, region="Hajime Village",
                rule=CanReachLocation("Defeat Leo (Forest of Trials)") & CanReachLocation("Dream 3 Complete")),
]

ULTIMATE_MOVES: list[LocationDef] = [
    LocationDef(ULTIMATE_MOVE_BASE_ID + 42, "Unlock Ultimate Typeless Move",
                LocCategory.STORY_CHECKPOINT, region="Typeless Gym", rule=CanReachLocation("Defeat Taiboku")),
    LocationDef(ULTIMATE_MOVE_BASE_ID + 43, "Unlock Ultimate Fire Move",
                LocCategory.STORY_CHECKPOINT, region="Dojo", rule=CanReachLocation("Defeat Nanase")),
    LocationDef(ULTIMATE_MOVE_BASE_ID + 44, "Unlock Ultimate Water Move",
                LocCategory.STORY_CHECKPOINT, region="Harbor Gym", rule=CanReachLocation("Defeat Ryusen")),
    LocationDef(ULTIMATE_MOVE_BASE_ID + 45, "Unlock Ultimate Wind Move",
                LocCategory.STORY_CHECKPOINT, region="Ryugasaki Gym", rule=CanReachLocation("Defeat Iori")),
    LocationDef(ULTIMATE_MOVE_BASE_ID + 46, "Unlock Ultimate Earth Move",
                LocCategory.STORY_CHECKPOINT, region="Wano Road", rule=CanReachLocation("Defeat Mitsukuni")),
    LocationDef(ULTIMATE_MOVE_BASE_ID + 47, "Unlock Ultimate Light Move",
                LocCategory.STORY_CHECKPOINT, region="Central Church", rule=CanReachLocation("Defeat Vitalis")),
    LocationDef(ULTIMATE_MOVE_BASE_ID + 48, "Unlock Ultimate Dark Move",
                LocCategory.STORY_CHECKPOINT, region="Old Road North", rule=CanReachLocation("Defeat Orochi")),
]

GOLD_REWARDS: list[LocationDef] = [
    LocationDef(TRAINER_GOLD_REWARD_BASE_ID + 57, "Watson Yen Reward",
                LocCategory.GOLD_REWARD, region="Big City", rule=CanReachLocation("Defeat Watson")),
    LocationDef(TRAINER_GOLD_REWARD_BASE_ID + 6, "Shota Yen Reward",
                LocCategory.GOLD_REWARD, region="Big City", rule=CanReachLocation("Defeat Shota")),
    LocationDef(TRAINER_GOLD_REWARD_BASE_ID + 7, "Rokurou Yen Reward",
                LocCategory.GOLD_REWARD, region="Big City", rule=CanReachLocation("Defeat Rokurou")),
    LocationDef(TRAINER_GOLD_REWARD_BASE_ID + 8, "Jinbei Yen Reward",
                LocCategory.GOLD_REWARD, region="Big City", rule=CanReachLocation("Defeat Jinbei")),
    LocationDef(TRAINER_GOLD_REWARD_BASE_ID + 9, "Yoshimitsu Yen Reward",
                LocCategory.GOLD_REWARD, region="Big City", rule=CanReachLocation("Defeat Yoshimitsu")),
    LocationDef(TRAINER_GOLD_REWARD_BASE_ID + 3, "Kantaro Yen Reward",
                LocCategory.GOLD_REWARD, region="Hajime Road", rule=CanReachLocation("Defeat Kantaro")),
    LocationDef(TRAINER_GOLD_REWARD_BASE_ID + 5, "Takezou Yen Reward",
                LocCategory.GOLD_REWARD, region="Hajime Road", rule=CanReachLocation("Defeat Takezou")),
    LocationDef(TRAINER_GOLD_REWARD_BASE_ID + 21, "Fence Yen Reward",
                LocCategory.GOLD_REWARD, region="Cave Road", rule=CanReachLocation("Defeat Fence")),
    LocationDef(TRAINER_GOLD_REWARD_BASE_ID + 31, "Dengaku Yen Reward",
                LocCategory.GOLD_REWARD, region="City Road", rule=CanReachLocation("Defeat Dengaku")),
    LocationDef(TRAINER_GOLD_REWARD_BASE_ID + 53, "Anderson Yen Reward",
                LocCategory.GOLD_REWARD, region="Wano Village", rule=CanReachLocation("Defeat Anderson")),
    LocationDef(TRAINER_GOLD_REWARD_BASE_ID + 52, "Little Ta-ke Yen Reward",
                LocCategory.GOLD_REWARD, region="Wano Village", rule=CanReachLocation("Defeat Little Ta-ke")),
    LocationDef(TRAINER_GOLD_REWARD_BASE_ID + 124, "Bunta Yen Reward",
                LocCategory.GOLD_REWARD, region="Wano Village", rule=CanReachLocation("Defeat Bunta")),
    LocationDef(TRAINER_GOLD_REWARD_BASE_ID + 55, "Umenoki Yen Reward",
                LocCategory.GOLD_REWARD, region="Shrine", rule=CanReachLocation("Defeat Umenoki")),
    LocationDef(TRAINER_GOLD_REWARD_BASE_ID + 24, "Battou Yen Reward",
                LocCategory.GOLD_REWARD, region="Wano Mountain Cave B1F", rule=CanReachLocation("Defeat Battou")),
    LocationDef(TRAINER_GOLD_REWARD_BASE_ID + 23, "Akage Yen Reward",
                LocCategory.GOLD_REWARD, region="Wano Mountain Cave B1F", rule=CanReachLocation("Defeat Akage")),
    LocationDef(TRAINER_GOLD_REWARD_BASE_ID + 14, "Yamato Yen Reward",
                LocCategory.GOLD_REWARD, region="Beach Road", rule=CanReachLocation("Defeat Yamato")),
    LocationDef(TRAINER_GOLD_REWARD_BASE_ID + 15, "Gyan Yen Reward",
                LocCategory.GOLD_REWARD, region="Beach Road", rule=CanReachLocation("Defeat Gyan")),
    LocationDef(TRAINER_GOLD_REWARD_BASE_ID + 122, "Manpuku Yen Reward",
                LocCategory.GOLD_REWARD, region="Beach Road", rule=CanReachLocation("Defeat Manpuku")),
    LocationDef(TRAINER_GOLD_REWARD_BASE_ID + 85, "Shouta Yen Reward",
                LocCategory.GOLD_REWARD, region="Harbor Town", rule=CanReachLocation("Defeat Shouta")),
    LocationDef(TRAINER_GOLD_REWARD_BASE_ID + 56, "Smith Yen Reward",
                LocCategory.GOLD_REWARD, region="Old Road", rule=CanReachLocation("Defeat Smith")),
    LocationDef(TRAINER_GOLD_REWARD_BASE_ID + 125, "Charlie Yen Reward",
                LocCategory.GOLD_REWARD, region="Old Road North", rule=CanReachLocation("Defeat Charlie")),
    LocationDef(TRAINER_GOLD_REWARD_BASE_ID + 123, "Masayuki Yen Reward",
                LocCategory.GOLD_REWARD, region="Wano Road", rule=CanReachLocation("Defeat Masayuki")),
    LocationDef(TRAINER_GOLD_REWARD_BASE_ID + 30, "Matsunoki Yen Reward",
                LocCategory.GOLD_REWARD, region="Holy Road", rule=CanReachLocation("Defeat Matsunoki")),
    LocationDef(TRAINER_GOLD_REWARD_BASE_ID + 26, "Shingo Yen Reward",
                LocCategory.GOLD_REWARD, region="Typeless Gym", rule=CanReachLocation("Defeat Shingo")),
    LocationDef(TRAINER_GOLD_REWARD_BASE_ID + 20, "Corn Yen Reward",
                LocCategory.GOLD_REWARD, region="Ryugasaki Gym", rule=CanReachLocation("Defeat Corn")),
]


# Pre-generate every possible extra-shop slot so we can put them in
# location_name_to_id.
from .Options import ExtraLevels as _ExtraLevels
_MAX_EXTRA_SHOP_LOCATIONS = max(
    int(_ExtraLevels.range_end),
    sum(cap for _, cap, _ in AP_PURCHASE_SLOTS),
)
ALL_EXTRA_SHOP_LOCATIONS: list[LocationDef] = extra_shop_locations(_MAX_EXTRA_SHOP_LOCATIONS)

ALL_LOCATIONS: list[LocationDef] = (
        TRAINER_FIGHTS + LEVEL_GRANTS + PICKUPS + KEY_PICKUPS
        + EVENT_PURCHASES + SCENES + STORY_CHECKPOINTS + ULTIMATE_MOVES
        + GOLD_REWARDS + ALL_EXTRA_SHOP_LOCATIONS 
)
LOCATION_BY_NAME: dict[str, LocationDef] = {loc.name: loc for loc in ALL_LOCATIONS}
LOCATION_BY_CODE: dict[int, LocationDef] = {loc.code: loc for loc in ALL_LOCATIONS}


class YarimonoLocation(Location):
    game = "Yarimono"
