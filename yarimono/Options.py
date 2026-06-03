"""Yaml options for Yarimono."""

from dataclasses import dataclass
from Options import Choice, DefaultOnToggle, PerGameCommonOptions, Range, Toggle


class Goal(Choice):
    """Which final boss must be defeated to win the seed.

    - white_god: The base game's final boss.
    - champion: Postgame Champion fight against Athena.
    - tama: DLC2's storyline boss.
    - nupuryu: DLC2 dev-room secret boss.
    """
    display_name = "Goal"
    option_white_god = 0
    option_champion = 1
    option_tama = 2
    option_nupuryu = 3
    default = option_champion


class RandomizeYarimanEncyclopedia(DefaultOnToggle):
    """When on, each Yariman Encyclopedia scene unlock becomes an Archipelago
    location and item.
    """
    display_name = "Randomize Yariman Encyclopedia"


class LimitedCheatTackle(Range):
    """Hard cap on Cheat Tackle uses for the entire playthrough.

    - 0 (default): Unlimited (vanilla behavior).
    - 1+: The move Cheat Tackle can't be selected if the number of times it's,
        been used is greater than or equal to this number.

    The amount of times it can be used in a single battle is still determined
    by the in-game difficulty setting.
    """
    display_name = "Limited Cheat Tackle"
    range_start = 0
    range_end = 99
    default = 0


class ExtraLevels(Range):
    """How many additional `Trainer Level` items beyond the vanilla levels
    to add to the item pool.

    An equal number of AP Locations will be placed as purchasable items
    in shops and vending machines.
    """
    display_name = "Extra Levels"
    range_start = 0
    range_end = 80
    default = 30


class EncyclopediaCheatTackleBonus(Range):
    """If non-zero, every N Yariman Encyclopedia scene unlocks grants one extra
    Cheat Tackle use.

    Only meaningful if `LimitedCheatTackle > 0`. Default 0 (no bonus).
    """
    display_name = "Encyclopedia Cheat Tackle Bonus (every N scenes)"
    range_start = 0
    range_end = 50
    default = 0
    
class OpponentLevelAdjustment(Range):
    """Adjust opponent Yarimon levels in trainer fights by this amount.
    """
    display_name = "Enemy Trainer Level Adjustment"
    range_start = -100
    range_end = 100
    default = 0
    
class FixedTrainerLevels(Toggle):
    """Most trainers added in the DLC scale the level of their team based on the player's 
    Trainer Level. This option prevents that scaling and sets all trainers to a fixed level 
    depending on the specific trainer.
    """
    display_name = "Fixed Trainer Levels"
    

@dataclass
class YarimonoOptions(PerGameCommonOptions):
    goal: Goal
    randomize_yariman_encyclopedia: RandomizeYarimanEncyclopedia
    limited_cheat_tackle: LimitedCheatTackle
    extra_levels: ExtraLevels
    encyclopedia_ct_bonus: EncyclopediaCheatTackleBonus
    opponent_level_adjustment: OpponentLevelAdjustment
    fixed_trainer_levels: FixedTrainerLevels
