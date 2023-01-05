import includes
import logging

from unittest.mock import Mock

from engineve.tags import meta, TAGS, TaggedClass, check_tag
from engineve.enginecommands.observer.observer import Observer
from engineve.enginecommands.observer.observermanager import ObserverManager
from engineve.utils import get_tag_enum

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
mock = Mock()


def log_args(*args, **kwargs):
    logging.debug(f"\nargs\t{args}\nkwargs\t{kwargs}")


def _trigger(obj, *args, **kwargs):
    return check_tag(obj, TAGS.attack)


def _reaction(*args, **kwargs):
    logging.debug(f"_reaction({args}, {kwargs})")
    return True


def test_register_observer():
    manager = ObserverManager()
    assert len(manager.observers) == 0
    manager.register_observer(Observer(trigger=_trigger, reaction=_reaction))
    assert len(manager.observers) > 0


def test_get_reation_command():
    test_observer = Observer(trigger=_trigger, reaction=_reaction)
    meta = TaggedClass(tags=[TAGS.attack])
    retval = test_observer.react(meta=meta)
    assert retval


def test_notify():
    manager = ObserverManager()
    manager.register_observer(Observer(trigger=_trigger, reaction=_reaction))
    meta_event = TaggedClass(tags={TAGS.attack: None})
    retval = manager.notify(meta=meta_event)
    return len(retval) > 0


def actor_ids_trigger(obj, *args, **kwargs):
    return check_tag(obj, TAGS.actor_ids)


def log_meta_args(meta, *args, **kwargs):
    logging.debug(f"meta: {meta}")
    logging.debug(f"actor_ids: {meta[get_tag_enum('actor_ids')]}")


mock.reaction.side_effect = log_meta_args


def test_notify_actor_ids():
    manager = ObserverManager()

    manager.register_observer(Observer(trigger=actor_ids_trigger, reaction=mock.reaction))
    ids = [1, 2]
    meta_obj = TaggedClass(tags={TAGS.actor_ids: ids})
    retval = manager.notify(meta=meta_obj.tags)
    mock.reaction.assert_called()
    # return len(retval) > 0


def test_pushobserver_matches_children():
    pass
    # manager = ObserverManager()
    # mock.reaction.side_effect = log_meta_args


def test_pushobserver_calls_children():
    pass
