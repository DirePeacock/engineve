import logging

from ..basecommands.command import Command
from  ..effectcommands.modifyhp import ModifyHP
from ...utils import roll

class DamageRollCommand(Command):    
    def __init__(self, attacker_id, target_id, *args, **kwargs):
        super().__init__(args, kwargs)
        self.target_id = target_id
        self.attacker_id = attacker_id
        
    def evaluate(self, state):
        super().evaluate(state)
        dmg_value = roll(size=6) + state.actors[self.attacker_id].get_ability_modifier('str')
        dmg_value = dmg_value * -1
        self.effects = [ModifyHP(self.target_id, dmg_value, self.attacker_id)]

    def apply_effects(self, state):
        super().apply_effects(state)
    
    # def execute(self, state):
    #     self.evaluate(state)
    #     return self.value
