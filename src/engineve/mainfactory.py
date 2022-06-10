from .gameengine import GameEngine
from .gametypes.actor import Actor
from .factory.spawningpool import make_actors_i_guess
def factory(spawn=True):
    GAMEENGINE = GameEngine()
    if spawn:
        make_actors_i_guess(GAMEENGINE, num_actors=4)
    return GAMEENGINE
    
