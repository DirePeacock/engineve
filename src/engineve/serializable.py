
class Serializable():
    serializable_attrs = []
    def _init_serializable_attrs(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.serializable_attrs:
                setattr(self, key, value)

    @classmethod
    def load_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        retval = {}
        for attr in self.serializable_attrs:
            if hasattr(getattr(self, attr), 'to_dict'):
                retval[attr] = getattr(self, attr).to_dict()
            else:
                retval[attr] = getattr(self, attr)
        return retval