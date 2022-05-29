from .gamemove import GameMove

from ...enginecommands.effectcommands.modifyresources import ModifyResources
from ...enginecommands.gamecommands.changeloccommand import ChangeLocCommand
from ...enginecommands.basecommands.command import Command
from ..aiutils import get_target, get_enemy_ids
from ..pathfinding import nearest_unoccupied_space
from ..pathingutils import measure_distance

class UseMovement(GameMove):
    # TODO do we really need a name for moves?
    command_type = ChangeLocCommand  # None
    name = None
    resource_cost = {'turn_movement': -1}    
    
    def get_weight(self, state):
        target_in_already_range = any(weight for weight in self.wiegh_targets(state).values() if weight <= 1)
        return -1 if target_in_already_range else 111
    
    def _dist_to_target(self, target_id, state):
        return measure_distance(state.actors[self.actor_id].loc, state.actors[target_id].loc)

    def wiegh_targets(self, state):
        '''return dict {target, weight}'''
        return {enemy_id: self._dist_to_target(enemy_id, state) for enemy_id in self.get_targets(state)}

    def get_targets(self, state):
        return [enemy_id for enemy_id in get_enemy_ids(self.actor_id, state)]



    def make_command(self, state, *args, **kwargs) -> ChangeLocCommand:
        '''find nearest enemy, set loc to nearest unoccupied space to that enemy'''
        # nearest enemy
        # nearest adjacent space to them
        # make new cmd
        # add movement use cmd
        # add turn_movement use cmd
        target_distances = self.wiegh_targets(state)
                
        # if any(tgt for tgt in self.wiegh_targets(state).values() <= 1):
        #     # burn movement resource?
        #     # todo maybe set weight to negative and then don't do it
        #     new_cmd =  Command()
        #     new_cmd.effects.append(ModifyResources(new_cmd.attacker_id, changes=self.resource_cost))

        target_enemy_id = min(target_distances, key=target_distances.get)
        destination_loc = nearest_unoccupied_space(state.actors[target_enemy_id].loc, state)
        
        locpath = [destination_loc]
        
        new_cmd = ChangeLocCommand(self.actor_id, locpath=locpath, log=f"{state.actors[self.actor_id].name} moves")
        new_cmd.effects.append(ModifyResources(self.actor_id, changes=self.resource_cost))
        
        
        return new_cmd
        
        # target_id = get_target(actor_id, state)    
        # new_cmd = self.command_type(attacker_id=actor_id, target_id=target_id)
        # new_cmd.effects.append(ModifyResources(new_cmd.attacker_id, changes=self.resource_cost))
        # return new_cmd