import logging

from ..actorai.basicai import BasicAI
from ..actorai.gamemoves.attackaction import AttackAction
from ..actorai.gamemoves.usemovement import UseMovement
from .resource import Resource
from ..utils import get_id, get_random_name, get_stat_modifier, roll, get_kwarg
from ..serializable import Serializable
from ..tags import TaggedClass
from .loc import Loc

class Actor(Serializable, TaggedClass):
    serializable_attrs = ['name', 'team', 'loc', 'resources', 'game_moves']
    turn_resources = ['turn_movement', 'turn_action', 'turn_bonus_action']
    delete_after_combat=False

    def __init__(self, name=None, team=1, loc=(0,0), ai_class=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = get_id()
        self.team = team
        self.name = name if name is not None else get_random_name()
        # TODO this
        self.hit_dice_num = get_kwarg('hit_dice_num', kwargs, 2)
        self.hit_dice_size = get_kwarg('hit_dice_size', kwargs, 6)
        self.pb = 2
        self.proficiencies = [] if 'proficiencies' not in kwargs.keys() else kwargs['proficiencies']
        self.speed = {'land': 30} if 'speed' not in kwargs.keys() else kwargs['speed']
        self.str = 14 if 'str' not in kwargs.keys() else kwargs['str']
        self.dex = 14 if 'dex' not in kwargs.keys() else kwargs['dex']
        self.con = 10 if 'con' not in kwargs.keys() else kwargs['con']
        self.int = 10 if 'int' not in kwargs.keys() else kwargs['int']
        self.wis = 10 if 'wis' not in kwargs.keys() else kwargs['wis']
        self.cha = 10 if 'cha' not in kwargs.keys() else kwargs['cha']
        self.ac = 13 if 'ac' not in kwargs.keys() else kwargs['ac']
        self.max_hp = self.roll_for_hp()
        self.hp = self.max_hp
        self.ai_class = BasicAI if ai_class is None else ai_class
        self.loc = Loc(loc) if isinstance(loc, tuple) else loc
        self.game_moves = {}
        self.resources = {}  
        
        self._init_actor_core()

    def roll_for_hp(self):
        return self.hit_dice_num * (self.get_ability_modifier('con') + int(0.5 * self.hit_dice_size) + 1)
        
    @property
    def ability_scores(self):
        return [self.str, self.dex, self.con, self.int, self.wis, self.cha]

    @ability_scores.setter
    def ability_scores(self, score_list):
        if len(score_list) != 6 or not all([isinstance(score, int) for score in score_list]):
            logging.warning(f'ability score array setter; needs to be list of 6 ints @{score_list}')
            return
        self.str = score_list[0]
        self.dex = score_list[1]
        self.con = score_list[2]
        self.int = score_list[3]
        self.wis = score_list[4]
        self.cha = score_list[5]

    def _init_actor_core(self):
        self.add_game_move(AttackAction(actor_id=self.id))
        self.add_game_move(UseMovement(actor_id=self.id))
        for resource_name in ['turn_action', 'turn_movement']:        
            self.add_resource(Resource(name=resource_name, value=1, max=1))

    def get_ability_modifier(self, stat):
        stat_scrore = self.__getattribute__(stat.lower())
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