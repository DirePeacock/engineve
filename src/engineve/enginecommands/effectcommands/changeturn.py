import logging

from .effectcommand import EffectCommand

class ChangeTurn(EffectCommand):
    def __init__(self, old_init, next_init):
        self.old_init = old_init
        self.next_init = next_init

    def apply(self, state, invoker=None):
        state.actors[state.combat.order[self.next_init]].refresh_turn_resources()
        state.combat.current_iter = self.next_init

