import logging

from ..actorai.basicai import BasicAI
from ..actorai.getaiclass import get_ai_class
from ..actorai.movefactory import load_game_move
from ..actorai.gamemoves.attackaction import AttackAction
from ..actorai.gamemoves.usemovement import UseMovement
from .resource import Resource
from ..utils import get_id, get_random_name, get_stat_modifier, roll, get_kwarg
from ..serializable import Serializable
from ..tags import TaggedClass
from .loc import Loc
from ..enginecommands.observer.observer import Observer

# todo how do I want to iterate over observers for effects
# notify with list of targets
class Actor(Serializable, TaggedClass):
    # serializable_attrs = ["name", "team", "loc", "resources", "game_moves"]
    turn_resources = ["turn_movement", "turn_action", "turn_bonus_action"]
    delete_after_combat = False

    def __init__(self, name=None, team=1, loc=(0, 0), ai_class=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = get_id()
        self.team = team
        self.name = name if name is not None else get_random_name()
        # # TODO this?
        # todo _init_hp(*args, **kwargs)
        self.hit_dice_num = get_kwarg("hit_dice_num", kwargs, 2)
        self.hit_dice_max = self.hit_dice_num
        self.hit_dice_size = get_kwarg("hit_dice_size", kwargs, 6)
        self.pb = 2
        self.proficiencies = [] if "proficiencies" not in kwargs.keys() else kwargs["proficiencies"]

        self.speed = {"land": 30} if "speed" not in kwargs.keys() else kwargs["speed"]
        self.ac = 13 if "ac" not in kwargs.keys() else kwargs["ac"]

        self._set_stats(*args, **kwargs)
        self.senses = {} if "senses" not in kwargs.keys() else kwargs["senses"]
        self.experience = get_kwarg("experience", kwargs, 0)
        self.death_saves = get_kwarg("death_saves", kwargs, 0)
        self.languages = get_kwarg("languages", kwargs, ["common"])
        self.flavor = get_kwarg("flavor", kwargs, {})

        # unused atm
        self.class_levels = get_kwarg("class_levels", kwargs, {})
        self.level_up_choices = get_kwarg("level_up_choices", kwargs, {})
        self.inventory = get_kwarg("inventory", kwargs, [])
        # probably not needed for headless but still
        self.sprites = get_kwarg("sprites", kwargs, {})

        self.max_hp = self.roll_for_hp()
        self.hp = self.max_hp

        if isinstance(ai_class, str):
            self.ai_class = get_ai_class(ai_class)
        elif ai_class is None:
            self.ai_class = BasicAI
        else:
            self.ai_class = ai_class

        self.loc = Loc(loc) if isinstance(loc, tuple) else loc
        self.game_moves = {}
        self.resources = {}
        self.effects = {}

        self._init_actor_core()
        if "game_moves" in kwargs.keys():
            self._load_game_moves(kwargs["game_moves"])

    def _load_game_moves(self, game_moves):
        for name, move in game_moves.items():
            new_move = load_game_move(**move)
            if new_move is None:
                logging.debug(f'idk what to do with {move}')
                continue
            self.game_moves[name] = new_move  # move
            self.game_moves[name].actor_id = self.id

    def _set_stats(self, *args, **kwargs):
        if "ability_scores" in kwargs.keys():
            self.ability_scores = kwargs["ability_scores"]
        elif all(stat for stat in ["str", "dex", "con", "int", "wis", "cha"] if stat in kwargs.keys()):
            self.str = 14 if "str" not in kwargs.keys() else kwargs["str"]
            self.dex = 14 if "dex" not in kwargs.keys() else kwargs["dex"]
            self.con = 10 if "con" not in kwargs.keys() else kwargs["con"]
            self.int = 10 if "int" not in kwargs.keys() else kwargs["int"]
            self.wis = 10 if "wis" not in kwargs.keys() else kwargs["wis"]
            self.cha = 10 if "cha" not in kwargs.keys() else kwargs["cha"]
        else:
            for arg in args:
                if isinstance(arg, list) and 6 == len(arg) and all(arg_i for arg_i in arg if isinstance(arg_i, int)):
                    self.ability_scores = arg
                    return

    def _set_stats_from_list(self, _list):
        self.ability_scores = _list

    def roll_for_hp(self):
        return self.hit_dice_num * (self.get_ability_modifier("con") + int(0.5 * self.hit_dice_size) + 1)

    @property
    def ability_scores(self):
        return [self.str, self.dex, self.con, self.int, self.wis, self.cha]

    @ability_scores.setter
    def ability_scores(self, score_list):
        if len(score_list) != 6 or not all([isinstance(score, int) for score in score_list]):
            logging.warning(f"ability score array setter; needs to be list of 6 ints @{score_list}")
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
        for resource_name in ["turn_action", "turn_movement"]:
            self.add_resource(Resource(name=resource_name, value=1, max=1))

    def get_ability_modifier(self, stat):
        stat_scrore = self.__getattribute__(stat.lower())
        return get_stat_modifier(stat_scrore)

    def add_game_move(self, game_move):
        self.game_moves[game_move.name] = game_move

    def add_resource(self, resource):
        self.resources[resource.name] = resource

    def is_turn_completed(self, state):
        return self.ai_class.is_turn_completed(self.id, state)

    def refresh_turn_resources(self):
        # TODO move to next turn or make this happen on observed next turn?
        for resource_name in self.turn_resources:
            if resource_name in self.resources.keys():
                self.resources[resource_name].value = self.resources[resource_name].max

    def make_game_move_command(self, state):
        return self.ai_class.make_game_move_command(self.id, state)

    def modify_hp(self, value):
        change = value.num if hasattr(value, "num") else value
        plus = "" if change <= 0 else "+"
        # logging.debug(f"{self.name}: hp {plus}{change}")
        self.hp += change
        # logging.debug(f"{self.name}.hp = {self.hp}")

    def __str__(self):
        return str({key: val for key, val in self.__dict__.items() if isinstance(val, (int, str))})

    def is_dead(self):
        return self.hp <= 0

    def add_effect(self, effect):
        """add_effect by id."""
        self.effects[effect.id] = effect

    def check_effects(self, meta):
        # TODO delete???
        for name, effect in self.effects.items():

            pass

    def check_reactions(self):
        # TODO delete???
        pass

    @classmethod
    def load_actor(cls):
        return cls.__init__()

    def save_actor(self) -> dict:
        return {}

    def serialize(self):
        """serialize and save type of AI and other stuff too"""
        retval = super().serialize()
        retval["ability_scores"] = self.ability_scores
        retval["ai_class"] = self.ai_class.__name__

        return retval
