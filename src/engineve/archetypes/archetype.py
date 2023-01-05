import pathlib
import logging
import yaml
from ..gametypes.actor import Actor
from ..utils import get_kwarg
ARCHETYPES = {}

rulebook_dir = pathlib.Path(__file__).parent.parent / 'rulebook'
"""   

"""
class Archetype():
    """this is a class
    an instance object of this class should be able to descripe the monster it is
    should be able to spawn an instance of it too i bet
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        return
    
    @classmethod
    def load_from_json(cls, data):
        '''the class should figure this out'''
        pass

class MonsterActor(Actor):
    archetype_name = ""
    delete_after_combat = True
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.archetype_name = get_kwarg('archetype_name', kwargs, 'unknown')
        self.cr = get_kwarg('cr', kwargs, 0.25)

class MonsterArchetype(Archetype):
    '''one object per monster stat block basically'''
    actor_class = MonsterActor
    def __init__(self, default_actor_kwargs, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_actor_kwargs = default_actor_kwargs

    def new_actor(self, **kwargs):
        actor_kwargs=self.default_actor_kwargs
        for kw, arg in kwargs.items():
            actor_kwargs[kw] = arg
        return self.actor_class(**actor_kwargs)

    @classmethod
    def spawn(cls, state, num=1, **kwargs):
        '''make new actor of archetype in the state.actors
        
        please kw your args for this
        '''
        for i in range(num):
            state.add_actor(cls.new_actor(**kwargs))
    
    @classmethod
    def load_from_json(cls, arch_data, **kwargs):
        # logging.debug(arch_data)
        return cls(default_actor_kwargs=arch_data)


def new_monster(arch_name, **kwargs):
    return ARCHETYPES['MonsterArchetypes'][arch_name].new_actor(**kwargs)

def traverse_roolbook():
    pass

def load_archetypes():
    ARCHETYPES['MonsterArchetypes'] = {}
    DATA = {}    
    with open(str(rulebook_dir / 'skeleton.yaml'), 'r') as rb_file:
        _book = yaml.safe_load(rb_file)
        for arch_name, arch_data in _book['MonsterArchetypes'].items():
            ARCHETYPES['MonsterArchetypes'][arch_name] = MonsterArchetype.load_from_json(arch_data)

class Archetypes():
    '''this object is the class of the rulebook'''
    def __init__():
        self.monsters = {}    

if ARCHETYPES == {}:
    load_archetypes()
