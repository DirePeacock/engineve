import pathlib
rulebook_dir = pathlib.Path(__file__).parent.parent / 'rulebook'
class Archetype():
    """this is a class
    an instance object of this class should be able to descripe the monster it is
    should be able to spawn an instance of it too i bet
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        return
    
    @classmethod
    def load_abstract_from_json(cls, data):
        '''the class should figure this out'''
        pass

import yaml
ARCHETYPES = {}
from ..gametypes.actor import Actor
class MonsterActor(Actor):
    archetype_name = ""
    delete_after_combat = True
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class MonsterArchetype(Archetype):
    actor_class = MonsterActor

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def new_actor(cls, *args, **kwargs):
        return cls.actor_class(*args, **kwargs)

    @classmethod
    def spawn(cls, state, num=1, *args, **kwargs):
        '''make new actor of archetype in the state.actors'''
        for i in range(num):
            state.add_actor(cls.new_actor(*args, **kwargs))
        

