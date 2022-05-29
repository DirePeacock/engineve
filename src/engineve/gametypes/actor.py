import logging

from ..actorai.basicai import BasicAI
from ..actorai.gamemoves.attackaction import AttackAction
from ..actorai.gamemoves.usemovement import UseMovement
from .resource import Resource
from ..utils import get_id, get_random_name, get_stat_modifier, roll
from ..serializable import Serializable
from .loc import Loc

class Actor(Serializable):
    serializable_attrs = ['name', 'team', 'loc', 'resources', 'game_moves']
    turn_resources = ['turn_movement', 'turn_action', 'turn_bonus_action']
    def __init__(self, name=None, team=1, loc=(0,0), ai_class=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.team = team
        self.name = name if name is not None else get_random_name()
        self.id = get_id()
        self.hp = 9
        self.pb = 2
        self.dex = 14
        self.str = 14
        self.ac = 13
        self.ai_class = BasicAI if ai_class is None else ai_class
        self.loc = Loc(loc) if isinstance(loc, tuple) else loc
        self.game_moves = {} # dict of objects
        self.resources = {}  # dict of objects
        self.max_hp = self.hp
        self._init_actor_core()
    
    def _init_actor_core(self):
        self.add_game_move(AttackAction(actor_id=self.id))
        self.add_game_move(UseMovement(actor_id=self.id))
        for resource_name in ['turn_action', 'turn_movement']:        
            self.add_resource(Resource(name=resource_name, value=1, max=1))

    def get_ability_modifier(self, stat):
        stat_scrore = self.dex if stat.lower() == 'dex' else self.str
        return get_stat_modifier(stat_scrore)
    
    def add_game_move(self, game_move):
        self.game_moves[game_move.name] = game_move

    def add_resource(self, resource):
        self.resources[resource.name] = resource

    def is_turn_completed(self, state):
        # self.hp=0
        return self.ai_class.is_turn_completed(self.id, state)

    def refresh_turn_resources(self):
        # TODO move to next turn or make this happen on observed next turn?
        for resource_name in self.turn_resources:
            if resource_name in self.resources.keys():
                self.resources[resource_name].value = self.resources[resource_name].max

        
    def make_game_move_command(self, state):
        return self.ai_class.make_game_move_command(self.id, state)
    
    def modify_hp(self, value):
        change = value.num if hasattr(value,'num') else value
        plus = '' if change <= 0 else '+'
        # logging.debug(f"{self.name}: hp {plus}{change}")
        self.hp += change
        # logging.debug(f"{self.name}.hp = {self.hp}")

    def __str__(self):
        return str({key: val for key, val in self.__dict__.items() if isinstance(val, (int, str))})

    def is_dead(self):
        return (self.hp <= 0)