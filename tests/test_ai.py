import includes
import logging

from engineve.tags import meta, TAGS, TaggedClass
from engineve.enginecommands.observer.observer import Observer
from engineve.enginecommands.observer.observermanager import ObserverManager

from engineve.enginestates.combatstate import CombatState
from engineve.gametypes.combat import Combat
from engineve.mainfactory import factory
from engineve.enginecommands.gamecommands.initiativecommand import InitiativeCommand


def _setup_game_engine():
    """game engine should start at the top of an active combat"""
    game_engine = factory(spawn=True)
    all_ids = [actor_id for actor_id in game_engine.game_state.actors.keys()]
    game_engine.engine_state = CombatState(all_ids)
    game_engine.game_state.combat = Combat(all_ids)
    game_engine.engine_state.start_combat(game_engine.game_state, game_engine.invoker)
    game_engine.invoker.periodic(game_engine.game_state)

    current_actor_id = game_engine.game_state.combat.order[game_engine.game_state.combat.current_iter]

    return game_engine, current_actor_id


def test_is_turn_completed():
    """tests is actor turn is done when it has things to do and then returns false"""
    game_engine, actor_i = _setup_game_engine()

    for resource_key in game_engine.game_state.actors[actor_i].resources.keys():
        if resource_key in game_engine.game_state.actors[actor_i].turn_resources:
            game_engine.game_state.actors[actor_i].resources[resource_key].value = 0

    is_complete = game_engine.game_state.actors[actor_i].is_turn_completed(game_engine.game_state)
    assert is_complete


def test_select_game_move():
    "actorai should return an appropriate move based on the state"
    game_engine, actor_i = _setup_game_engine()
    new_cmd = game_engine.game_state.actors[actor_i].make_game_move_command(game_engine.game_state)
    assert new_cmd is not None
