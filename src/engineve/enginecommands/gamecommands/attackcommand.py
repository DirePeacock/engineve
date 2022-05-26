import logging

from ..basecommands.compositecommand import CompositeCommand
from ..effectcommands.modifyresources import ModifyResources
from .attackrollcommand import AttackRollCommand
from .damagerollcommand import DamageRollCommand

class AttackCommand(CompositeCommand):
    def __init__(self,  attacker_id, target_id, *args, **kwargs):
        '''make attackRoll and damage roll command childres'''
        super().__init__(args, kwargs)
        self.attacker_id=attacker_id
        self.target_id=target_id
        self.children['attack_roll'] = AttackRollCommand(self.attacker_id, self.target_id)
        self.children['damage_roll'] = DamageRollCommand(self.attacker_id, self.target_id)
        # self.resources= [] if resources is None else ModifyResources(actor_id=attacker_id, changes={'turn_action': -1})
        
    def evaluate(self, state):
        self.evaluated = True
        self.children['attack_roll'].evaluate(state)
        attack_hits = self.children['attack_roll'].value
        if attack_hits:
            self.children['damage_roll'].evaluate(state)    
        # for resource in self.resources:
        #     self.effects.append(resource)

    