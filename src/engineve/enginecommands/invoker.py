from .observer.observermanager import ObserverManager
from ..tags import meta 
class Invoker(ObserverManager):
    """Client calls this to send command to the receiver
    keep track of history
    execute commands
    """

    def __init__(self):
        self.command_stack = []
        self.command_log = []
    
    def periodic(self, state):
        if len(self.command_stack) < 1:
            return
        self.command_stack[0].execute(state)
        self.command_log.append(self.command_stack.pop(0))

    def put(self, command):
        self.command_stack.insert(0, command)
