# """ TODO:
# tags
# actor.get_command
# actor.register_observer()
# command effects another command on the stack
# """


class Observer:
    def __init__(self, trigger, reaction):
        self.trigger = trigger
        self.reaction = reaction

    def react(self, meta, state=None, invoker=None):
        """should return command obj for the stack"""
        return self.reaction(meta, state, invoker)

    def match_notification(self, meta, state=None):
        return self.trigger(meta, state)
