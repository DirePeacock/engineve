import logging

from ..basecommands.command import Command
from .rollcommand import RollCommand
from ..effectcommands.modifyhp import ModifyHP
from ...utils import roll, check_tag
from ...tags import TAGS


class DamageRollCommand(RollCommand):
    def __init__(self, attacker_id, target_id, dmg_dice=None, stat="str", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_id = target_id
        self.attacker_id = attacker_id

        self.dmg_dice = dmg_dice if dmg_dice is not None else "1d6"
        self.stat = stat

    def evaluate(self, state, invoker=None):
        super().evaluate(state)

        if self.stat is not None:
            self.add_flat_modifier(self.stat, state.actors[self.attacker_id].get_ability_modifier(self.stat))

        # check critical-ness of self then double the dice rolled
        if check_tag(self.tags, "critical_hit"):
            pass

        dmg_value = roll(self.dmg_dice)
        dmg_value += self.get_total_flat_modifier()

        dmg_value = max(0, dmg_value)  # RULE no negative damage
        self.effects = [ModifyHP(self.target_id, (dmg_value * -1), self.attacker_id)]

        self.log = f"{dmg_value} dmg"
        self.tags[TAGS["damage"]] = dmg_value
        invoker.notify(self.tags, state)

    # def apply_effects(self, state, invoker=None):
    #     super().apply_effects(state)

    # def execute(self, state):
    #     self.evaluate(state)
    #     return self.value
