import logging

from .gametypes.actor import Actor
from .gametypes.gridmap import GridMap
from .gametypes.combat import Combat
from .gametypes.log import Log

class GameStateManager():
    """I manage the state of the game, storing and changing
    as far as the command pattern goes, I am also the receiver of command objects from the Invoker?
    """
    def __init__(self):
        self.actors= {}
        self.combat = Combat()
        self.overworld = None
        self.gridmap = GridMap()
        self.log = Log()

    def add_actor(self, actor):
        self.actors[actor.id] = actor
    
    @classmethod
    def instantiate(cls):
        instance = cls()
        return instance
