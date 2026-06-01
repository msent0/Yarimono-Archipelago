"""Access rules for Yarimono."""

from __future__ import annotations

from rule_builder.rules import And, CanReachLocation, Has, Rule, True_

from .Locations import LOCATION_BY_NAME, LocCategory
from .Regions import TRANSITIONS


TRAINER_LEVEL_ITEM = "Trainer Level"


def _compose(*rules) -> Rule:
    """AND together any number of rules, dropping True_ no-ops."""
    rules = [r for r in rules if r is not None and not isinstance(r, True_)]
    if not rules:
        return True_()
    if len(rules) == 1:
        return rules[0]
    return And(*rules)


def set_rules(world) -> None:
    """Apply per-location and per-entrance access rules."""
    multiworld = world.multiworld
    player = world.player

    # Locations
    for loc_def in LOCATION_BY_NAME.values():
        try:
            loc_obj = multiworld.get_location(loc_def.name, player)
        except KeyError:
            # Some locations (notably scenes when encyclopedia is off) are
            # intentionally omitted from this seed.
            continue
        rule = _build_location_rule(loc_def)
        if rule is not None and not isinstance(rule, True_):
            world.set_rule(loc_obj, rule)

    # Entrances
    for t in TRANSITIONS:
        if t.rule is None:
            continue
        entrance_name = f"{t.src} -> {t.dst}"
        try:
            entrance = multiworld.get_entrance(entrance_name, player)
        except KeyError:
            continue
        if not isinstance(t.rule, True_):
            world.set_rule(entrance, t.rule)


def _build_location_rule(loc_def):
    """AND the LocationDef.rule with any level requirement."""
    parts = []
    if loc_def.required_level > 0:
        parts.append(Has(TRAINER_LEVEL_ITEM, loc_def.required_level))
    if loc_def.rule is not None:
        parts.append(loc_def.rule)
    return _compose(*parts) if parts else None


GOAL_LOCATION = {
    0: "Defeat White God",
    1: "Defeat Athena",
    2: "Defeat Tama",
    3: "Defeat Nupuryu",
}


def set_completion_condition(world) -> None:
    """Mark the seed as complete when the goal location is reachable."""
    goal_value = int(world.options.goal)
    goal_loc_name = GOAL_LOCATION[goal_value]
    world.set_completion_rule(CanReachLocation(goal_loc_name))
