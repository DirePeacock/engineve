import logging

from ..basecommands.command import Command
from .rollcommand import RollCommand
from ..effectcommands.modifyhp import ModifyHP
from ...utils import roll
from ...tags import TAGS, check_tag


class DamageRollCommand(RollCommand):
    def __init__(
        self, attacker_id, target_id, dmg_range=(1, 6), stat="str", *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.target_id = target_id
        self.attacker_id = attacker_id

        self.dmg_range = dmg_range if isinstance(dmg_range, tuple) else tuple(dmg_range)
        self.stat = stat

    def apply_effects(self, state, invoker=None):
        super().apply_effects(state, invoker)
        if state.actors[self.target_id].hp <= 0:
            self.add_tag(TAGS["death"])

    def evaluate(self, state, invoker=None):
        super().evaluate(state)

        if self.stat is not None:
            self.add_flat_modifier(
                self.stat,
                state.actors[self.attacker_id].get_ability_modifier(self.stat),
            )

        # check critical-ness of self then double the dice rolled
        roll_val = roll(self.dmg_range)

        flat_val = self.get_total_flat_modifier()
        dmg_value = roll_val + flat_val

        dmg_value = max(0, dmg_value)  # RULE no negative damage
        if check_tag(self.tags, "critical_hit"):
            dmg_value *= state.actors[self.attacker_id].critical_multiplier
            # BONUS CRIT DAMAGE DICE?

        self.effects = [ModifyHP(self.target_id, (dmg_value * -1), self.attacker_id)]

        func_log = f"{self.dmg_range}" + ("" if flat_val == 0 else f"+{flat_val}")
        if check_tag(self.tags, "critical_hit"):
            func_log = f"{self.dmg_range}" + "+" + func_log
        self.log = f"{dmg_value}=({func_log}) dmg"
        self.tags[TAGS["damage"]] = dmg_value

        # if check_tag(self.tags, "critical_hit"):

        #     logging.debug(f"crit: log:{self.log}")

        invoker.notify(self.tags, state)

    # def apply_effects(self, state, invoker=None):
    #     super().apply_effects(state)

    # def execute(self, state):
    #     self.evaluate(state)
    #     return self.value
