from .gamemove import GameMove

from ...enginecommands.effectcommands.modifyresources import ModifyResources
from ...enginecommands.gamecommands.changeloccommand import ChangeLocCommand
from ...enginecommands.basecommands.command import Command


class UseMovement(GameMove):
    # TODO do we really need a name for moves?
    command_type = ChangeLocCommand  # None
    name = None
    resource_cost = {"turn_action": -1, "turn_movement": 1}

    def get_weight(self, state):
        return 1

    def make_command(self, state, *args, **kwargs) -> ChangeLocCommand:
        """find nearest enemy, set loc to nearest unoccupied space to that enemy"""
        new_cmd = ChangeLocCommand(self.actor_id, locpath=locpath, log=f"{state.actors[self.actor_id].name} moves")
        new_cmd.effects.append(ModifyResources(self.actor_id, changes=self.resource_cost))

        return new_cmd

        # target_id = get_target(actor_id, state)
        # new_cmd = self.command_type(attacker_id=actor_id, target_id=target_id)
        # new_cmd.effects.append(ModifyResources(new_cmd.attacker_id, changes=self.resource_cost))
        # return new_cmd
