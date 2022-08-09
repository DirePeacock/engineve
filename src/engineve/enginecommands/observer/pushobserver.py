from .observer import Observer
from .observermanager import ObserverManager


class PushObserver(Observer, ObserverManager):
    """only notify children if we match, and then also match the children also."""

    def __init__(self, *args, **kwargs):
        ObserverManager.__init__(self, *args, *kwargs)
        Observer.__init__(self, *args, *kwargs)

    def match_notification(self, meta, state=None):
        return self.trigger(meta)

    def react(self, meta, state=None, invoker=None):
        """should return command obj for the stack"""
        retval_list = [
            obs.reaction(meta, state, invoker) for obs in self.observers if obs.match_notification(meta, state)
        ]
        retval_list.append(self.reaction(meta, state, invoker), 0)
        return retval_list
