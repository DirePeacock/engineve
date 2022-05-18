import logging

from .compositecommand import CompositeCommand
from .command import Command


class AttackRollCommand(Command):
    '''roll attack to hit, evaluate if it hits or whatever
    '''
    def __init__(self, attacker_id, target_id, *args, **kwargs):
        super().__init__(args, kwargs)
        self.target_id = target_id
        self.attacker_id = attacker_id

    def execute(self, state):
        self.evaluate(state)
        self.apply_effects(state)

    def evaluate(self, state):
        super().evaluate(state)
        to_hit_roll = state.actors[self.attacker_id].roll_to_hit()
        attack_hits = to_hit_roll >= state.actors[self.target_id].ac
        if attack_hits:
            logging.debug(f"HIT! {state.actors[self.attacker_id].name} hit {state.actors[self.target_id].name}")
        else:
            logging.debug(f"MISS! {state.actors[self.attacker_id].name}'s {to_hit_roll} misses the {state.actors[self.target_id].ac} ac of {state.actors[self.target_id].name}")
        self.value = attack_hits
