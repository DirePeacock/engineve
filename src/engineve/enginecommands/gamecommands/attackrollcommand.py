import logging

from .rollcommand import RollCommand
from ...utils import roll, calculate_advantage
from ...tags import TAGS


class AttackRollCommand(RollCommand):
    """roll attack to hit, evaluate if it hits or whatever"""

    # TODO Calculating Flat Bonuses

    def __init__(self, attacker_id, target_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_id = target_id
        self.attacker_id = attacker_id
        self.stat = "str"

    def execute(self, state, invoker=None):
        self.evaluate(state)
        self.apply_effects(state)

    def evaluate(self, state, invoker=None):
        super().evaluate(state, invoker)
        # setup that attacker is making a target

        # notify that we are making an attack before we roll
        self.tags[TAGS["attack_roll_declared"]] = None
        if invoker is not None:
            invoker.notify(self.tags, state, invoker)
        del self.tags[TAGS["attack_roll_declared"]]
        # get modifiers

        #
        dice_val = roll(size=20)
        # advantage_value = calculate_advantage(self.tags)
        if dice_val == 20:
            self.add_tag("critical_hit")
        elif dice_val == 1:
            self.add_tag("critical_miss")

        to_hit_roll = (
            dice_val
            + state.actors[self.attacker_id].pb
            + state.actors[self.attacker_id].get_ability_modifier(self.stat)
        )

        attack_hits = to_hit_roll >= state.actors[self.target_id].ac
        self.log = f"({to_hit_roll} v {state.actors[self.target_id].ac})"

        # notify that we are making an attack after we've determined a hit/crit/miss or whatever
        self.tags[TAGS["attack_roll_completed"]] = None
        if invoker is not None:

            invoker.notify(self.tags, state, invoker)

        # if attack_hits:
        #     logging.debug(f"HIT! {self.log}")
        # else:
        #     logging.debug(f"MISS! {self.log}")

        self.value = attack_hits
