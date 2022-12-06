from .effectcommand import EffectCommand
from ...tags import TAGS


class ModifyHP(EffectCommand):
    def __init__(self, target_id, num, attacker_id=None):
        self.target_id = target_id
        self.num = num

    def apply(self, state, invoker=None):
        """do thing to state"""
        state.actors[self.target_id].modify_hp(self.num)
