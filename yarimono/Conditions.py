"""Rule helpers for Yarimono."""

from __future__ import annotations

from rule_builder.options import OptionFilter
from rule_builder.rules import Filtered, Rule

from .Options import RandomizeYarimanEncyclopedia


def OnScenes(rule: Rule) -> Rule:
    """Apply `rule` only when scene-unlock randomization is on."""
    return Filtered(
        rule,
        options=[OptionFilter(RandomizeYarimanEncyclopedia, 1)],
        filtered_resolution=True,
    )
