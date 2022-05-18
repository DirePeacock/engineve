import logging

from .compositecommand import CompositeCommand
from .attackrollcommand import AttackRollCommand
from .damagerollcommand import DamageRollCommand
        
class AttackCommand(CompositeCommand):
    def __init__(self,  attacker_id, target_id, *args, **kwargs):
        '''make attackRoll and damage roll command childres'''
        super().__init__(args, kwargs)
        self.children['attack_roll'] = AttackRollCommand(attacker_id, target_id)
        self.children['damage_roll'] = DamageRollCommand(attacker_id, target_id)
    
    # def execute(self, state):
    #     self.evaluate(state)
        
    def evaluate(self, state):
        self.evaluated = True
        self.children['attack_roll'].evaluate(state)
        attack_hits = self.children['attack_roll'].value
        if attack_hits:
            self.children['damage_roll'].evaluate(state)
    