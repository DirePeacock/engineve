import logging

from .effectcommand import EffectCommand

class ChangeLoc(EffectCommand):
    def __init__(self, actor_id, destination=None, *args, **kwargs):
        self.actor_id = actor_id
        self.destination = destination

    def apply(self, state, invoker=None):
        state.set_actor_loc(self.actor_id, self.destination)
        # state.actors[self.actor_id].loc = self.destination
