from ..basecommands.command import Command


class EffectCommand(Command):
    """simplest observable changes to the state. has already been evaluated"""

    def apply(self, state, invoker=None):
        """i have a"""
        return

    def execute(self, state, invoker=None):
        """just do something to apply so this can be a standalone effect"""
        self.apply(state, invoker)
