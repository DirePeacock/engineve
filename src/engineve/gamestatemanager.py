import logging
import json
from .gametypes.actor import Actor
from .gametypes.gridmap import GridMap
from .gametypes.combat import Combat
from .gametypes.log import Log
from .gametypes.time import GameTime


class GameStateManager:
    """I manage the state of the game, storing and changing
    as far as the command pattern goes, I am also the receiver of command objects from the Invoker?
    """

    actor_debug_attrs = ["name", "loc", "hp"]

    def __init__(self):
        self.actors = {}
        self.combat = Combat()
        self.overworld = None
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
            blah[actor.team].append({attr: actor.__getattribute__(attr) for attr in self.actor_debug_attrs})
        print(json.dumps(blah, indent=4))
