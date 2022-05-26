import logging

from ..actorai.basicai import BasicAI
from ..utils import get_id, get_random_name, get_stat_modifier, roll
from ..serializable import Serializable
from .loc import Loc

class Actor(Serializable):
    serializable_attrs = ['name', 'team', 'loc', 'resources', 'game_moves']
    turn_resources = ['turn_movement', 'turn_action', 'turn_bonus_action']
    def __init__(self, name=None, team=1, loc=(0,0), ai_class=BasicAI, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.team = team
        self.name = name if name is not None else get_random_name()
        self.id = get_id()
        self.hp = 9
        self.pb = 2
        self.dex = 14
        self.str = 14
        self.ac = 13
        self.ai_class = ai_class
        self.loc = Loc(loc) if isinstance(loc, tuple) else loc
        self.game_moves = {}
        self.resources = {}
        self.max_hp = self.hp
    
    def get_ability_modifier(self, stat):
        stat_scrore = self.dex if stat.lower() == 'dex' else self.str
        return get_stat_modifier(stat_scrore)
    
    def _init_actor_core(self):
        pass

    def add_game_move(self, game_move):
        self.game_moves[game_move.name] = game_move

    def is_turn_done(self, state):
        return self.ai_class.is_turn_done(self.id, state)
        
    def make_game_move_command(self, state):
        return self.ai_class.make_game_move_command(state, self.id)
    
    def modify_hp(self, value):
        change = value.num if hasattr(value,'num') else value
        plus = '' if change <= 0 else '+'
        logging.debug(f"{self.name}: hp {plus}{change}")
        self.hp += change

    # def roll_to_hit(self):
    #     return self.pb + get_stat_modifier(self.str) + roll()
    # def roll_damage(self):
    #     return get_stat_modifier(self.str) + roll(size=6)
    # def roll_initiative(self):
    #     return get_stat_modifier(self.dex) + roll()
    def __str__(self):
        return str({key: val for key, val in self.__dict__.items() if isinstance(val, (int, str))})
    def is_dead(self):
        return hp > 0

