from .observer.observermanager import ObserverManager
from ..tags import TAGS


class Invoker(ObserverManager):
    """Client calls this to send command to the receiver
    keep track of history
    execute commands
    """

    _max_cmd_history = 1000

    def __init__(self, log=None):
        super().__init__()
        self.command_stack = []
        self.command_log = []
        self._log = log

    def periodic(self, state):
        if len(self.command_stack) < 1:
            return

        # if top of stack has a loggable thing, rmv
        if self.command_stack[0].log and self._log:
            self._log.stack.pop(0)

        # execute the command and have it beable to send notifications for its own logic too
        self.command_stack[0].execute(state=state, invoker=self)

        self.notify(meta=self.command_stack[0].tags, state=state, invoker=self)
        self.command_log.append(self.command_stack.pop(0))

        # if end of the history has a loggable str, append
        if self.command_log[-1].log:
            state.log.history.append(self.command_log[-1].log)

    def put(self, command):
        self.command_stack.insert(0, command)
        if self._log is not None and command.log:
            self._log.stack.insert(0, command.log)


class stack_iterator:
    def __init__(self, invoker):
        self._invoker = invoker
        self._index = 0
        self._child_keys = []

    def __iter__(self):
        pass

    def __next__(self):
        raise StopIteration
