import includes
import logging

from engineve.tags import (meta, TAGS, TaggedClass)
from engineve.enginecommands.observer.observer import Observer
from engineve.enginecommands.observer.observermanager import ObserverManager

# def test_meta_match():
#     print(TAGS)
#     print('somehting')
#     for name, value in TAGS.__members__.items():
#         print(f"{name}: {value}")

def test_reation_command():
    """ test reactable actions
    make a state with combatants A and B
    B can react to an attack that misses or hits or somehting
    A attacks B
    B attacks A with its reaction
    reaction occurs before effects of triggering attack

    TODO:
    observer pattern - kinda
    game command types -
    Actor.get_command() ->
    tags
    pytest stubs?
    """
    def _trigger(state, obj):
        return isinstance(obj, TaggedClass) and TAGS.attack in obj.tags

    def _reaction(*args, **kwargs):
        print(f"_reaction({args}, {kwargs})")
        return True

    _reaction = 'reaction'
    test_observer= Observer(trigger=_trigger, reaction=_reaction)
    meta = TaggedClass(tags=[TAGS.attack])
    retval = test_observer.react(state=None, meta=meta)
    assert retval