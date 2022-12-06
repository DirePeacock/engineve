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
    assert engine.invoker.command_stack[0].stat == "dex"
    assert engine.invoker.command_stack[0].children["damage_roll"].dmg_dice == "1d6"

    # assert attack is a scimitar attack


# def test_get_target():
#     """verify"""
#     is_good = False
#     assert is_good
