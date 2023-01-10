import includes
import logging
from utils import setup_game_engine, actor_put_command
from engineve.actorai.gamemoves.gamemove import GameMove


def test_init():
    """verify"""
    engine, id_a, id_b = setup_game_engine()
    engine.engine_state.start_combat(engine.game_state, engine.invoker)
    # Actor id_a should have the effect on it
    atk_cmd_id = actor_put_command(engine, id_a, cmd_substring="Scimitar")
    assert engine.invoker.command_stack[0].stat == "agi"
    assert engine.invoker.command_stack[0].children["damage_roll"].dmg_range == (1, 6)


def test_load_bonus_action_attack():
    """verify"""
    test_char = "kilsyth"
    engine, id_a, id_b = setup_game_engine()

    engine.import_character(test_char)

    test_char_id = None
    for i, actor in engine.game_state.actors.items():
        logging.debug(actor.name)
        if actor.name.lower() == test_char:
            test_char_id = i

    moves = engine.game_state.actors[test_char_id].game_moves
    # logging.debug(engine.game_state.actors[test_char_id].name)
    assert moves["swiftscythe_right"].resource_cost["turn_bonus_action"] == -1

    # Actor id_a should have the effect on it

    # assert attack is a scimitar attack


# def test_get_target():
#     """verify"""
#     is_good = False
#     assert is_good
