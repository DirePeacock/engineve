import logging

from .effectcommand import EffectCommand
from ...gametypes.time import GameTimeDelta


class IncrementGameTime(EffectCommand):
    def __init__(self, **kwargs):
        super().__init__()
        self.timedelta = GameTimeDelta(**kwargs)

    def apply(self, state, invoker=None):
        state.time = state.time + self.timedelta
