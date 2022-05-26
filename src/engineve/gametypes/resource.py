from ..serializable import Serializable

class Resource(Serializable):
    serializable_attrs = ['name', 'val', 'max']
    def __init__(self, name, val=None, max=1):
        self.name = name
        self.val = val
        self.max = max
    
    def is_available(self):
        return self.val is None or self.val > 0

    def recharge(self):
        self.val = self.max