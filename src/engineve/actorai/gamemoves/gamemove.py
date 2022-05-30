from ...serializable import Serializable
from ...tags import TaggedClass
import random
class GameMove(Serializable, TaggedClass):
    '''this class represents a possible action to be taken by an actor in the game
    actor should know which moves are available to it
    TODO ugh weighing this needs to be improved a lot
    '''
    command_type = object  # None
    resource_cost = {} # if resource_cost is None else resource_cost
    
    # def __init__(self, command_type, name='', resource_cost=None):
    #     self.command_type = command_type
    #     self.name = name
    #     self.resource_cost = {} if resource_cost is None else resource_cost
    def __init__(self, actor_id=None, name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actor_id = actor_id
        self.name = name if name is not None else type(self).__name__

    def get_weight(self, state):
        return random.randint(1, 10)
    
    def wiegh_targets(self, state):
        '''return dict {target, weight}'''
        return {}

    def get_targets(self, state):
        return []

    def make_command(self, *args, **kwargs):
        cmd = self.command_type(*args, **kwargs)
        for key, val in self.tags.items():
            cmd.tags[key] = val
        return cmd
    
    def is_available(self, state):
        for key, change in self.resource_cost.items():
            if key in state.actors[self.actor_id].resources.keys():
                if 0 <= state.actors[self.actor_id].resources[key].value + change:
                    continue
                else:
                    return False
            else:
                return False

        return True
                    