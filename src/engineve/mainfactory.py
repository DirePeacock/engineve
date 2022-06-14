from .gameengine import GameEngine
from .gametypes.actor import Actor
from .factory.spawningpool import make_actors_i_guess
from .archetypes.archetype import MonsterArchetype

def factory(spawn=True):
    GAMEENGINE = GameEngine()
    if spawn:
        for team_id in [0,1]:
            MonsterArchetype.spawn(state=GAMEENGINE.game_state, num=4, team=team_id)
        
    return GAMEENGINE
    
