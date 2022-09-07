import includes
import logging
from unittest import mock
from utils import setup_game_engine

from engineve.actorai.gamemoves.attackaction import AttackAction
from engineve.actorai import pathingutils
from engineve.actorai import aiutils


def test_measure_distance():
    scenarios = [
        {"args": [(1, 2), (2, 2)], "expected": 1},
        {"args": [(1, 2), (2, 3)], "expected": 1},
        {"args": [(1, 2), (2, 4)], "expected": 2},
        {"args": [(1, 2), (3, 1)], "expected": 2},
    ]
    for case in scenarios:
        actual = pathingutils.measure_distance(*case["args"])
        assert actual == case["expected"]


# def test_measure_distance():
#     scenarios = [
#         {"args": [(1, 2), (2, 2)], "expected": 1},
#         {"args": [(1, 2), (2, 3)], "expected": 1},
#         {"args": [(1, 2), (2, 4)], "expected": 2},
#         {"args": [(1, 2), (3, 1)], "expected": 2},
#     ]
#     for case in scenarios:
#         actual = aiutils.is_actor_alive(*case["args"])
#         assert actual == case["expected"]


def test_attack_in_range():
    game_engine, id_one, id_two = setup_game_engine()
    atk_name = "scimitar"
    loc_one = (1, 1)
    loc_two = (1, 2)
    hp_one = 10
    hp_two = 10
    game_engine.game_state.actors[id_one].loc = loc_one
    game_engine.game_state.actors[id_one].hp = hp_one
    game_engine.game_state.actors[id_two].loc = loc_two
    game_engine.game_state.actors[id_two].hp = hp_two

    valid_ids = game_engine.game_state.actors[id_two].game_moves[atk_name].get_targets(game_engine.game_state)
    logging.debug(f"valid_ids {valid_ids}")
    assert 0 < len(valid_ids)


def test_attack_out_of_range():
    """shouldn't look at out of range things"""
    game_engine, id_one, id_two = setup_game_engine()
    atk_name = "scimitar"
    loc_one = (1, 1)
    loc_two = (1, 3)
    hp_one = 10
    hp_two = 10
    game_engine.game_state.actors[id_one].loc = loc_one
    game_engine.game_state.actors[id_one].hp = hp_one
    game_engine.game_state.actors[id_two].loc = loc_two
    game_engine.game_state.actors[id_two].hp = hp_two

    valid_ids = game_engine.game_state.actors[id_two].game_moves[atk_name].get_targets(game_engine.game_state)
    logging.debug(f"valid_ids {valid_ids}")
    assert 1 > len(valid_ids)


def test_attack_in_range_but_dead():
    game_engine, id_one, id_two = setup_game_engine()
    atk_name = "scimitar"
    loc_one = (1, 1)
    loc_two = (1, 2)
    hp_one = 10
    hp_two = 0
    game_engine.game_state.actors[id_one].loc = loc_one
    game_engine.game_state.actors[id_one].hp = hp_one
    game_engine.game_state.actors[id_two].loc = loc_two
    game_engine.game_state.actors[id_two].hp = hp_two

    valid_ids = game_engine.game_state.actors[id_one].game_moves[atk_name].get_targets(game_engine.game_state)
    logging.debug(f"valid_ids {valid_ids}")
    assert 1 > len(valid_ids)


from engineve.enginestates.menustate import MenuState
from engineve.enginestates.overworldstate import OverworldState
from engineve.enginestates.combatstate import CombatState
from engineve.enginecommands.observer.observer import Observer
import time


def test_engine_trans_wait():
    game_engine, id_one, id_two = setup_game_engine()
    game_engine._state_transition_await_frames = 3
    test_frames = 10
    unpause_frames = game_engine._state_transition_await_frames * 1
    if isinstance(game_engine.engine_state, MenuState):
        game_engine.engine_state.open_overworld()
    if isinstance(game_engine.engine_state, MenuState):
        game_engine.engine_state.open_overworld()
    assert isinstance(game_engine.engine_state, CombatState)
    for i in range(0, test_frames):
        game_engine.periodic()
        is_good = False
        if i <= unpause_frames:
            is_good = game_engine.engine_sync.is_waiting()
        else:
            is_good = not game_engine.engine_sync.is_waiting()
        logging.debug(f"frame: {i} is_good: {is_good}")
        assert is_good
        # time.sleep(0.1)
    # get game to overworld start combat
    # have some arbitrary wait on transition
