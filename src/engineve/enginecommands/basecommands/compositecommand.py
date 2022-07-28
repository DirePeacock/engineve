from .command import Command


class CompositeCommand(Command):
    """state as arg or state as cls var"""

    def __init__(self, *args, **kwargs):
        self.children = {}
        super().__init__(*args, **kwargs)

    def execute(self, state, invoker):
        """execute all children"""
        self.evaluate(state, invoker)
        self.apply_effects(state, invoker)

    def apply_effects(self, state, invoker):
        for key in self.children.keys():
            self.children[key].apply_effects(state, invoker)
        super().apply_effects(state, invoker)

    def evaluate(self, state, invoker):
        """evaluate children until all my children are evaluated and I know what to do with them."""
        self._evaluate_children(state, invoker)
        super().evaluate(state, invoker)

    def _evaluate_children(self, state, invoker):
        for key in self.children.keys():
            self.children[key].evaluate(state, invoker)
