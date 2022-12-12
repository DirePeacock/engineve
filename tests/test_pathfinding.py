import includes
from engineve.actorai.pathingutils import get_radial_square_locs
from engineve.gametypes.loc import Loc
import utils
import unittest


def test_radial_squares():
    """values should be tuples in the right order and not negative"""
    center = (1, 1)
    radius_expected_vals = [
        [center],
        [(0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0), (0, 0), (0, 1)],
        [(0, 3), (1, 3), (2, 3), (3, 3), (3, 2), (3, 1), (3, 0)],
    ]
    radius_test_results = [True, True, True]
    for r in range(len(radius_test_results)):
        method_retval = get_radial_square_locs(center=center, r=r)
        for i in range(len(method_retval)):
            assert method_retval[i] == radius_expected_vals[r][i]


def test_unoccupied_space():
    game_engine, id_one, id_two = utils.setup_game_engine(combat=False)

    test_loc_tuple = (2, 2)
    other_loc_tuple = (1 + test_loc_tuple[0], 1 + test_loc_tuple[1])
    test_loc_loc = Loc(*test_loc_tuple)

    game_engine.game_state.actors[id_one].loc = test_loc_tuple

    relevant_ids = [id_one, id_two]

    assert game_engine.game_state.gridmap.check_occupancy(test_loc_tuple, game_engine.game_state, relevant_ids)
    assert game_engine.game_state.gridmap.check_occupancy(test_loc_loc, game_engine.game_state, relevant_ids)

    game_engine.game_state.actors[id_one].loc = test_loc_loc

    assert game_engine.game_state.gridmap.check_occupancy(test_loc_tuple, game_engine.game_state, relevant_ids)
    assert game_engine.game_state.gridmap.check_occupancy(test_loc_loc, game_engine.game_state, relevant_ids)

    game_engine.game_state.actors[id_one].loc = other_loc_tuple

    assert False in (
        game_engine.game_state.gridmap.check_occupancy(test_loc_tuple, game_engine.game_state, relevant_ids),
        True,
    )


def test_nearest_unoccupied_space():
    # TODO

    pass
