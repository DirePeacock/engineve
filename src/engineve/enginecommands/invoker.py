class Invoker():
    """Client calls this to send command to the receiver
    keep track of history
    apply commands
    """

    def __init__(self):
        self.command_stack = []
        self.command_log = []
    
    def tick_stack(self, state):
        if len(self.command_stack) < 1:
            return
        self.command_stack[0].execute(state)
        self.command_log.append(self.command_stack.pop())

    def put(self, command):
        self.command_stack.insert(0, command)
    

    def execute(self, state, command):
        "evaluate command, send actionable change to receiver"
        self.put(command)
        self.tick_stack(state)

            
