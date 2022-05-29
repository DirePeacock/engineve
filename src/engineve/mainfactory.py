from .gameengine import GameEngine
from .gametypes.actor import Actor
def factory(spawn=True):
    GAMEENGINE = GameEngine()
    if spawn:
        for team_id in [0, 1]:
            GAMEENGINE.spawn_actors(actor_class=Actor, num=1, team=team_id)
    return GAMEENGINE
    
