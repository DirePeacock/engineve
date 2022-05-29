import logging

from ..basecommands.command import Command
from ...utils import roll

class AttackRollCommand(Command):
    '''roll attack to hit, evaluate if it hits or whatever
    '''
    def __init__(self, attacker_id, target_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_id = target_id
        self.attacker_id = attacker_id
        
    def execute(self, state):
        self.evaluate(state)
        self.apply_effects(state)

    def evaluate(self, state):
        super().evaluate(state)
        to_hit_roll = roll(size=20) + state.actors[self.attacker_id].pb + state.actors[self.attacker_id].get_ability_modifier('str')
        attack_hits = to_hit_roll >= state.actors[self.target_id].ac
        self.log = (f"({to_hit_roll} v {state.actors[self.target_id].ac})")
        # if attack_hits:
        #     logging.debug(f"HIT! {self.log}")
        # else:
        #     logging.debug(f"MISS! {self.log}")
        self.value = attack_hits
