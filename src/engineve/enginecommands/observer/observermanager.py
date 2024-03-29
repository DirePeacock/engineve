class ObserverManager:
    """has logic fror appending and notifying observers"""

    def __init__(self):
        self.observers = []

    def register_observer(self, observer):
        self.observers.append(observer)

    def unregister_observer(self, observer):
        # TODO compare to id storage?
        self.observers.remove(observer)

    def notify(self, meta, state=None, invoker=None):
        """Alert the observers
        TODO: what should this return
        """
        return [
            observer.react(meta=meta, state=state, invoker=self)
            for observer in self.observers
            if observer.match_notification(meta, state)
        ]
