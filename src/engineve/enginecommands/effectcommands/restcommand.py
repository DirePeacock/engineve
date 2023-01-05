import logging

from ..basecommands.command import Command
from ..effectcommands.effectcommand import EffectCommand
from ...utils import roll


class RestCommand(EffectCommand):
    """just do a long rest for now"""

    # TODO short rest option

    def __init__(self, actor_ids, rest_type="long", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actor_ids = actor_ids
        self.rest_type = rest_type

    def apply(self, state, invoker=None):
        names = []
        for a_id in self.actor_ids:
            if a_id in state.actors.keys():
                for resource in state.actors[a_id].resources.keys():
                    state.actors[a_id].resources[resource].recharge
                state.actors[a_id].hp = state.actors[a_id].max_hp
                state.actors[a_id].hit_dice_num = state.actors[a_id].hit_dice_max
                names.append(state.actors[a_id].name)
        self.log = f"{self.rest_type} rest for {', '.join(names)}"
