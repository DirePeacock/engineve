from .effectcommand import EffectCommand
class Initiative(EffectCommand):
    def __init__(self, order):
        self.order = order
        
    def apply(self, state):
        '''do thing to state'''
        state.combat.order = self.order
        state.combat.current_iter = max(self.order.keys())
