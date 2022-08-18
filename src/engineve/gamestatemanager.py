import logging
import json

from .gametypes.actor import Actor
from .gametypes.gridmap import GridMap
from .gametypes.combat import Combat
from .gametypes.log import Log
from .gametypes.time import GameTime
from .serializable import Serializable
from .gametypes.party import Party


class GameStateManager(Serializable):
    """I manage the state of the game, storing and changing
    as far as the command pattern goes...

    I am passed by the invoker into command executions which can then modify my state.
    """

    _actor_debug_attrs = ["name", "loc", "hp"]

    def __init__(self, *args, **kwargs):
        for key, val in kwargs.items():
            logging.debug(key)

        if "actors" not in kwargs.keys() or not hasattr(self, "actors"):
            self.actors = {}

        if "actors" in kwargs.keys():
            for key, actor_kwargs in kwargs["actors"].items():
                # logging.debug(key, )
                self.add_actor(Actor(**actor_kwargs))

        if "party" in kwargs.keys():
            for key, val in kwargs["party"].items():
                self.party = Party()
                # logging.debug(key, val)
        else:
            self.party = Party()

        self.overworld = None
        self.combat = Combat()
        self.gridmap = GridMap()
        self.log = Log()
        self.time = GameTime.now()
        self.global_effects = {}

    def add_actor(self, actor):
        self.actors[actor.id] = actor

    def add_effect(self, effect):
        self.global_effects[effect.id] = effect

    @classmethod
    def instantiate(cls):
        # TODO why is this here, just an artefact of old factory?
        instance = cls()
        return instance

    def blah(self):
        """just blast this stuff out"""
        blah = {}
        for aid, actor in self.actors.items():
            if actor.team not in blah.keys():
                blah[actor.team] = []
            blah[actor.team].append({attr: actor.__getattribute__(attr) for attr in self._actor_debug_attrs})
        print(json.dumps(blah, indent=4))
