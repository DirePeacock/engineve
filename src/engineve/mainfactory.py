from .gameengine import GameEngine
from .gametypes.actor import Actor
from .factory.spawningpool import make_actors_i_guess
from .archetypes.archetype import ARCHETYPES, new_monster, MonsterArchetype

def factory(spawn=True):
    GAMEENGINE = GameEngine()
    if spawn:
        for team_id in [0,1]:
            for i in range(4):
                GAMEENGINE.game_state.add_actor(new_monster('skeleton', team=team_id))
    return GAMEENGINE
    
