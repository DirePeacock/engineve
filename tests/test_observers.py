import includes
import logging

from engineve.tags import (meta, TAGS, TaggedClass, check_tags)
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

def _trigger(obj, *args, **kwargs):
    return check_tags(obj, TAGS.attack)
def _reaction(*args, **kwargs):
    logging.debug(f"_reaction({args}, {kwargs})")
    return True

def test_register_observer():
    manager = ObserverManager()
    assert len(manager.observers) == 0
    manager.register_observer(Observer(trigger=_trigger, reaction=_reaction))
    assert len(manager.observers) > 0
    
    
    
def test_get_reation_command():
    test_observer= Observer(trigger=_trigger, reaction=_reaction)
    meta = TaggedClass(tags=[TAGS.attack])
    retval = test_observer.react(meta=meta)
    assert retval
    
    

def test_notify():
    manager = ObserverManager()
    manager.register_observer(Observer(trigger=_trigger, reaction=_reaction))
    meta_event = TaggedClass(tags=[TAGS.attack])
    retval = manager.notify(meta=meta_event)
    return len(retval) > 0