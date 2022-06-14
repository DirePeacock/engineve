from .gamemove import GameMove
from ...enginecommands.gamecommands.attackcommand import AttackCommand
from ...enginecommands.effectcommands.modifyresources import ModifyResources
from .. import pathingutils
from .. import aiutils

class AttackAction(GameMove):
    command_type = AttackCommand   # None
    name = None
    resource_cost = {'turn_action': -1} # if resource_cost is None else resource_cost
    attack_range=5
    # def __init__(self, command_type, name='', resource_cost=None):
    #     self.command_type = command_type
    #     self.name = name
    #     self.resource_cost = {} if resource_cost is None else resource_cost
    
    # def is_available(self, state)
    def get_ttk_weight(self, target_id, state):
        return max((100.0 / state.actors[target_id].hp), -0.001)

    def wiegh_targets(self, state):
        return {target_id: self.get_ttk_weight(target_id, state) for target_id in self.get_targets(state)}

    def enemy_in_range(self, enemy_id, state):
        return 1 <= pathingutils.measure_distance(state.actors[self.actor_id].loc, state.actors[enemy_id].loc)

    def make_command(self, state, *args, **kwargs) -> AttackCommand:
        target_weights = self.wiegh_targets(state)
        if len(target_weights) ==0:
            print(self.wiegh_targets(state))
        target_id = max(target_weights, key=target_weights.__getitem__)

        attack_declaration = f"{state.actors[self.actor_id].name} attacks {state.actors[target_id].name}"
        new_cmd = super().make_command(attacker_id=self.actor_id, target_id=target_id, log=attack_declaration)
        new_cmd.effects.append(ModifyResources(new_cmd.attacker_id, changes=self.resource_cost))
        
        return new_cmd
    
    def get_targets(self, state):
        enemy_ids = [eid for eid in aiutils.get_enemy_ids(self.actor_id, state)]
        enemy_ids = [eid for eid in enemy_ids if aiutils.is_actor_alive(eid, state) and self.enemy_in_range(eid, state)]
        #  
        return enemy_ids
