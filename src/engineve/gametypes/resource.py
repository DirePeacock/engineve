from ..serializable import Serializable

class Resource(Serializable):
    serializable_attrs = ['name', 'val', 'max']
    def __init__(self, name, value=None, max=None):
        self.name = name
        self.value = value
        self.max = max
    
    def is_available(self):
        return self.value is None or self.value > 0

    def recharge(self):
        if self.value is not None:
            self.value = self.max