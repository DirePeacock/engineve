import logging

from .effectcommand import EffectCommand


class ApplyEffect(EffectCommand):
    def __init__(self, effect, parent_id=None, *args, **kwargs):
        """put effect object into either an actor's zone or the general state
        give it a start time and a parent_id if needed"""
        super().__init__(*args, **kwargs)
        self.effect = effect
        self.parent_id = parent_id

    def apply(self, state, invoker=None):
        self.effect.start_time = state.time

        if self.parent_id is not None:
            self.effect.parent_id = self.parent_id
            state.actors[self.parent_id].add_effect(self.effect)
            invoker.register_observer(state.actors[self.parent_id].effects[self.effect.id])
        else:
            state.add_effect(self.effect)
            invoker.register_observer(state.effects[self.effect.id])
