from .effectcommand import EffectCommand
class ModifyResources(EffectCommand):
    def __init__(self, actor_id, changes=None):
        self.actor_id = actor_id
        self.changes = {} if changes is None else changes
        
    def apply(self, state):
        '''do thing to state'''
        for name, net_change in self.changes.items():
            if name in state.actors[self.actor_id].resources.keys():
                state.actors[self.actor_id].resources[name].val += net_change
        
