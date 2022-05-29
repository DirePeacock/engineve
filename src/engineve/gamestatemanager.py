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

    # def get_combat_iter(self, ids=None):
    #     return CombatActorIterator(self, ids)

    # def manage_attack(self, attacker_id, target_id):  
    #     to_hit_roll = self.actors[attacker_id].roll_to_hit()
    #     attack_hits = to_hit_roll >= self.actors[target_id].ac
    #     if attack_hits:
    #         damage = self.actors[attacker_id].roll_damage() * -1
    #         self.actors[target_id].modify_hp(damage)
    #         logging.debug(f"{self.actors[attacker_id].name} hit {self.actors[target_id].name} for {damage}")
    #     else:
    #         logging.debug(f"{self.actors[attacker_id].name}'s {to_hit_roll} hits the {self.actors[target_id].ac} ac of {self.actors[target_id].name}")

    # def apply_effects(self, effects):
    #     print(effects)
    #     for effect in effects:
    #         print(effect)


