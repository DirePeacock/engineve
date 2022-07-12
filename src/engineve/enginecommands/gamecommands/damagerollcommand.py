import logging

from ..basecommands.command import Command
from  ..effectcommands.modifyhp import ModifyHP
from ...utils import roll

class DamageRollCommand(Command):    
    def __init__(self, attacker_id, target_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_id = target_id
        self.attacker_id = attacker_id
        
    def evaluate(self, state, invoker=None):
        super().evaluate(state)
        dmg_value = roll(size=6) + state.actors[self.attacker_id].get_ability_modifier('str')
        
        dmg_value = max(0, dmg_value)  # RULE no negative damage
        self.effects = [ModifyHP(self.target_id, (dmg_value * -1), self.attacker_id)]
        
        self.log = f"{dmg_value} dmg"
        
        invoker.notify(self.tags)

    def apply_effects(self, state, invoker=None):
        super().apply_effects(state)
    
    # def execute(self, state):
    #     self.evaluate(state)
    #     return self.value
