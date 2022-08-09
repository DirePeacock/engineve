import logging
import includes
import unittest

import engineve.utils as engineve_utils
from engineve import tags
from utils import setup_game_engine
from engineve.gametypes.time import GameTime, roundsdelta, GameTimeDelta


class test_advantage_calcs(unittest.TestCase):
    cases = [
        {"args": [{tags.TAGS["advantage"]: 1}], "expected": 1},
        {"args": [{tags.TAGS["advantage"]: 1, tags.TAGS["disadvantage"]: 1}], "expected": 0},
        {"args": [{tags.TAGS["disadvantage"]: 1}], "expected": -1},
        {"args": [{}], "expected": 0},
    ]

    def test_advantage_calcs(self):
        for case in self.cases:
            logging.debug(case["args"])
            self.assertEqual(case["expected"], engineve_utils.calculate_advantage(*case["args"]))


def test_stack_iter():
    engine, id_a, id_b = setup_game_engine()
    engine.engine_state.start_combat(engine.game_state, engine.invoker)
    for cmd in engineve_utils.command_stack_df_traversal(engine.invoker.command_stack):
        logging.debug(f"{type(cmd).__name__}: {cmd.id}")
    print("bruh")


def test_time_add_sub():
    diff_x = 1
    time_a = GameTime.now()
    time_b = time_a
    delta_x = roundsdelta(rounds=diff_x)
    time_b = time_b + delta_x

    time_diff = time_b - time_a
    assert time_diff == roundsdelta(rounds=diff_x)
