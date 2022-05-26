from ...serializable import Serializable
from ...tags import TaggedClass
class GameMove(Serializable, TaggedClass):
    '''this class represents a possible action to be taken by an actor in the game
    actor should know which moves are available to it
    '''
    command_type = object  # None
    name = None
    # resource_cost = {} # if resource_cost is None else resource_cost
    
    # def __init__(self, command_type, name='', resource_cost=None):
    #     self.command_type = command_type
    #     self.name = name
    #     self.resource_cost = {} if resource_cost is None else resource_cost
    
    def make_command(self, *args, **kwargs):
        return self.command_type(args, kwargs)
        

    