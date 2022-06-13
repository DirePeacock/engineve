from .observer import Observer
from .observermanager import ObserverManager

class PushObserver(Observer, ObserverManager):
    """only notify children if we match, and then also match the children also."""
    def __init__(self, *args, **kwargs):
        ObserverManager.__init__(self, *args, *kwargs)
        Observer.__init__(self, *args, *kwargs)

    def match_notification(self, meta):
        return self.trigger(meta)

    def react(self, meta):
        """should return command obj for the stack"""
        retval_list = [obs.reaction(meta) for obs in self.observers if obs.match_notification(meta)]
        retval_list.append(self.reaction(meta), 0)
        return retval_list