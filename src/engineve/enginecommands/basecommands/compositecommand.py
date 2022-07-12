from .command import Command

class CompositeCommand(Command):
    '''state as arg or state as cls var'''
    def __init__(self, *args, **kwargs):
        self.children = {}
        super().__init__(*args, **kwargs)
        
    def execute(self, state, invoker=None):
        '''execute all children'''
        self.evaluate(state)
        self.apply_effects(state)
        
    def apply_effects(self, state, invoker=None):
        for key in self.children.keys():
            self.children[key].apply_effects(state, invoker) 
        super().apply_effects(state, invoker)
        
    def evaluate(self, state, invoker=None):
        '''evaluate children until all my children are evaluated and I know what to do with them.'''
        self._evaluate_children(state, invoker)
        super().evaluate(state)

    def _evaluate_children(self, state, invoker=None):
        for key in self.children.keys():
            self.children[key].evaluate(state, invoker) 
    

