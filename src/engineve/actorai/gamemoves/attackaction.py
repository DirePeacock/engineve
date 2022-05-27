from .gamemove import GameMove
from ...enginecommands.gamecommands.attackcommand import AttackCommand
from ...enginecommands.effectcommands.modifyresources import ModifyResources
from ..aiutils import get_target

class AttackAction(GameMove):
    command_type = AttackCommand   # None
    name = None
    resource_cost = {'turn_action': -1} # if resource_cost is None else resource_cost
    
    # def __init__(self, command_type, name='', resource_cost=None):
    #     self.command_type = command_type
    #     self.name = name
    #     self.resource_cost = {} if resource_cost is None else resource_cost
    
    def make_command(self, actor_id, state, *args, **kwargs) -> AttackCommand:
        target_id = get_target(actor_id, state)    
        new_cmd = self.command_type(attacker_id=actor_id, target_id=target_id)
        new_cmd.effects.append(ModifyResources(new_cmd.attacker_id, changes=self.resource_cost))
        return new_cmd