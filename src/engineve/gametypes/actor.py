import logging
import random

from .loc import Loc


def roll(size=20):
    return random.randint(1, size)

class Actor():
    def __init__(self, name=1, team=1, loc=(0,0)):
        self.team = team 
        self.name = name
        self.id = self.name
        self.hp = 9
        self.pb = 2
        self.dex = 2
        self.str = 2
        self.ac = 13
        self.loc = Loc(loc) if isinstance(loc, tuple) else loc
    
    def modify_hp(self, value):
        change = value.num if hasattr(value,'num') else value
        word = 'dmg' if change <= 0 else 'oh'
        logging.debug(f"{self.name}: {word} {change}")
        self.hp += change
    def roll_to_hit(self):
        return self.pb + self.str + roll()
    def roll_damage(self):
        return self.str + roll(size=6)
    def roll_initiative(self):
        return self.dex + roll()
    def __str__(self):
        return str({key: val for key, val in self.__dict__.items() if isinstance(val, (int, str))})


