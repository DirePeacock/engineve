import pathlib
import includes
import logging

from engineve.mainfactory import factory
from engineve.enginestates.combatstate import CombatState
from engineve.gametypes.combat import Combat
from engineve.gameengine import GameEngine


def new_game_engine():
    return GameEngine()


def setup_game_engine():
    game_engine = new_game_engine()
    game_engine.base_dir = pathlib.Path(__file__).parent / "test_data_load_loc"
    game_engine.characters_dir = game_engine.base_dir / "characters"
    id_one = game_engine.spawn_archetype("skeleton", team=1, name="ONE")
    id_two = game_engine.spawn_archetype("skeleton", team=2, name="TWO")

    all_ids = [actor_id for actor_id in game_engine.game_state.actors.keys()]
    game_engine.engine_state = CombatState(all_ids)
    game_engine.game_state.combat = Combat(all_ids)
    return game_engine, id_one, id_two


def actor_put_command(engine, actor_id, cmd_substring="attack"):
    for name, game_move in engine.game_state.actors[actor_id].game_moves.items():
        if cmd_substring.lower() in name.lower():
            engine.invoker.put(game_move.make_command(engine.game_state))
            return engine.invoker.command_stack[0].id
    raise Exception(f"no move containing the name {cmd_substring}")
