from ..serializable import Serializable


class Log(Serializable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.history = []
        self.stack = []

    def write(self, obj):
        self.history.append(obj)
