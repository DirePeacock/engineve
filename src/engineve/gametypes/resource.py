from ..serializable import Serializable
from ..tags import TAGS, TaggedClass
from ..utils import percent_rounding
import math


class Resource(Serializable, TaggedClass):
    def __init__(self, name, value=None, max=None, recharge=None, *args, **kwargs):
        """
        args
        name (str)
        value (int) - current value
        max (int) - max value
        recharge(str) ['short_rest', 'long_rest'] - when should the recharge observer recharge these?
        """
        super().__init__(*args, **kwargs)
        self.name = name
        self.value = value
        self.max = max
        if recharge is not None:
            self.add_tag("recharge", recharge)

    def is_available(self):
        return self.value is None or self.value > 0

    def recharge(self):
        if self.value is not None:
            remainder = math.abs(self.max) % 1
            margin = 0.1
            if remainder >= margin or remainder <= 1.0 - margin:
                self.value = percent_rounding(self.max)
            else:
                self.value = self.max
