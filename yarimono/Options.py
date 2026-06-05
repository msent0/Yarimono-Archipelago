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


class RandomizeYarimanEncyclopedia(Toggle):
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

class RandomizeTrainerYarimon(Choice):
    """Randomizes the Yarimon that trainers use in battle.
    
    - off: Trainers use the same Yarimon as in vanilla.
    - on: Trainers use random Yarimon.
    - bst: Trainers use random Yarimon, but the replacement Yarimon will be around the same base stat total as the one it's replacing.
    
    """
    display_name = "Randomize Trainer Yarimon"
    option_off = 0
    option_on = 1
    option_bst = 2
    default = option_off
    
class RandomizeWildYarimon(Choice):
    """Randomizes the Yarimon that appear in the wild.
    
    - off: Wild encounters are the same as in vanilla.
    - on: Wild encounter slots are randomized.
    - bst: Wild encounter slots are randomized, but the replacement Yarimon will be around the same base stat total as the one it's replacing.
    
    """
    display_name = "Randomize Wild Yarimon"
    option_off = 0
    option_on = 1
    option_bst = 2
    default = option_off
    
class RandomizeYarimonAbilities(Choice):
    """Randomizes the abilities of all Yarimon.

    - off: Yarimon have the same abilities as in vanilla.
    - on: Yarimon have random abilities.
    
    """
    display_name = "Randomize Yarimon Abilities"
    option_off = 0
    option_on = 1
    default = option_off

class RandomizeYarimonMoves(Choice):
    """Randomizes the moves of all Yarimon.

    - off: Yarimon have the same moves as in vanilla.
    - on: Yarimon have random moves.
    
    """
    display_name = "Randomize Yarimon Moves"
    option_off = 0
    option_on = 1
    default = option_off

class RoadPassesRequired(Toggle):
    """When on, the three exits out of Big City each require a corresponding
    key item ("Central Road Pass" for the north exit, "Beach Road Pass" for the
    west, "Cave Road Pass" for the south).
    """
    display_name = "Road Passes Required"


class RoadPassHints(Toggle):
    """When on the NPC at each of the three exits out of Big City will tell
    you where to find the corresponding road pass.
    """
    display_name = "Road Pass Hints"
    
class RandomizeTrainerGoldReward(Toggle):
    """When on, money recieved from defeating trainers are now locations and
    battle prize money is added to the item pool.
    """
    display_name = "Randomize Trainer Money Reward"

class TrainerRewardMoneyAmount(Range):
    """The game, by default, gives a flat 1000 yen for defeating a male trainer.
    This option allows you to change that amount.
    """
    display_name = "Trainer Reward Money Amount"
    range_start = 0
    range_end = 100000
    default = 1000
    

@dataclass
class YarimonoOptions(PerGameCommonOptions):
    goal: Goal
    randomize_yariman_encyclopedia: RandomizeYarimanEncyclopedia
    limited_cheat_tackle: LimitedCheatTackle
    extra_levels: ExtraLevels
    encyclopedia_ct_bonus: EncyclopediaCheatTackleBonus
    opponent_level_adjustment: OpponentLevelAdjustment
    fixed_trainer_levels: FixedTrainerLevels
    randomize_trainer_yarimon: RandomizeTrainerYarimon
    randomize_wild_yarimon: RandomizeWildYarimon
    randomize_yarimon_abilities: RandomizeYarimonAbilities
    randomize_yarimon_moves: RandomizeYarimonMoves
    road_passes_required: RoadPassesRequired
    road_pass_hints: RoadPassHints
    randomize_trainer_gold_reward: RandomizeTrainerGoldReward
    trainer_reward_money_amount: TrainerRewardMoneyAmount
