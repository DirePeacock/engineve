from .abstractcommand import AbstractCommand
from ...tags import TaggedClass
from ...utils import get_id


class Command(AbstractCommand, TaggedClass):
    """
    can be evaluated
    can do application of evaluated change
    can undo application of evaluated change
    can store tags for obeservers
    can be a composite command
    can be logged
    has ref to the invoker so command can track when it needs to
    """

    def __init__(self, *args, **kwargs):
        TaggedClass.__init__(self, *args, **kwargs)
        self.id = get_id()
        self.add_tag("command_id", self.id)
        self.args = args
        self.kwargs = kwargs
        self.effects = []
        self.inverse_effects = []
        self.evaluated = False
        self.log = "" if "log" not in kwargs.keys() else kwargs["log"]

    def execute(self, state, invoker=None):
        if not self.evaluated:
            self.evaluate(state, invoker)
        self.apply_effects(state, invoker)

    def evaluate(self, state, invoker=None) -> None:
        """resolves command down to primitive command"""
        self.evaluated = True
        # self.effects = [] if
        self.inverse_effects = []

    def apply_effects(self, state, invoker=None):
        for effect in self.effects:
            effect.apply(state, invoker)

    def undo(self, state, invoker=None):
        if not self.evaluated:
            self.evaluate(state, invoker)
        state.apply_effects(self.inverse_effects)
