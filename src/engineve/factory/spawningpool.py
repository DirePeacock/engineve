from ..gametypes.actor import Actor
from ..tags import TAGS
def make_actors_i_guess(GAMEENGINE, num_actors=4):
    for team_id in [0, 1]:
        GAMEENGINE.spawn_actors(actor_class=Actor, num=num_actors, team=team_id)
    
