class ObserverManager():
    """ has logic fror appending and notifying observers
    """
    def __init__(self):
        self.observers = []

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify(self, state, meta):
        """Alert the observers"""
        for observer in self.observers:
            if observer.match_notification(state, meta):
                observer.get_reaction(self)