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
    pytest stubs?
    """

def test_get_reation_command():
    def _trigger(state, obj):
        return isinstance(obj, TaggedClass) and TAGS.attack in obj.tags

    def _reaction(*args, **kwargs):
        logging.debug(f"_reaction({args}, {kwargs})")
        return True

    test_observer= Observer(trigger=_trigger, reaction=_reaction)
    meta = TaggedClass(tags=[TAGS.attack])
    retval = test_observer.react(state=None, meta=meta)
    assert retval
    
    return

def test_notify():
    def _trigger(state, obj):
        return isinstance(obj, TaggedClass) and TAGS.attack in obj.tags

    def _reaction(*args, **kwargs):
        logging.debug(f"_reaction({args}, {kwargs})")
        return True
    
    manager = ObserverManager()
    manager.register_observer(Observer(trigger=_trigger, reaction=_reaction))
    meta_event = TaggedClass(tags=[TAGS.attack])
    manager.notify(state=None, meta=meta_event)
    return