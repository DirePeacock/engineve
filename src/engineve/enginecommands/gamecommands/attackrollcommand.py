import logging

from ..basecommands.command import Command
from ...utils import roll

class AttackRollCommand(Command):
    '''roll attack to hit, evaluate if it hits or whatever

    '''
    # TODO Calculating Flat Bonuses
    
    def __init__(self, attacker_id, target_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_id = target_id
        self.attacker_id = attacker_id
        self.stat = 'str'
        self.proficiency = 2
        
    def execute(self, state, invoker=None):
        self.evaluate(state)
        self.apply_effects(state)

    def evaluate(self, state, invoker=None):
        super().evaluate(state)
        dice_val = roll(size=20)
        #setup that attacker is making a target

        # notify that we are making an attack before we roll
        if invoker is not None:
            invoker.notify(self.tags)

        if dice_val == 20:
            self.add_tag('critical_hit')
        elif dice_val == 1:
            self.add_tag('critical_miss')

        to_hit_roll = dice_val  + state.actors[self.attacker_id].pb + state.actors[self.attacker_id].get_ability_modifier('str')
        
        attack_hits = to_hit_roll >= state.actors[self.target_id].ac
        self.log = (f"({to_hit_roll} v {state.actors[self.target_id].ac})")
        
        # notify that we are making an attack after we've determined a hit/crit/miss or whatever
        if invoker is not None:
            invoker.notify(self.tags)
        
        # if attack_hits:
        #     logging.debug(f"HIT! {self.log}")
        # else:
        #     logging.debug(f"MISS! {self.log}")
        
        self.value = attack_hits
