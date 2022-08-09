from ..enginecommands.gamecommands.attackcommand import AttackCommand
from . import aiutils
from . import pathfinding
from . import pathingutils


class BasicAI:
    """class for making decision based on state and args thru static methods"""

    @classmethod
    def choose_game_move(cls, actor_id, state):

        # TODO make this smart
        key_wieghts = cls.get_available_game_move_keys(actor_id, state)
        # cls.get_available_game_move_keys(actor_id, state)
        return max(key_wieghts, key=key_wieghts.get)

    @classmethod
    def get_available_game_move_keys(cls, actor_id, state):
        move_keys = [
            key for key, game_move in state.actors[actor_id].game_moves.items() if game_move.is_available(state)
        ]
        weights = {key: state.actors[actor_id].game_moves[key].get_weight(state) for key in move_keys}
        return {key: value for key, value in weights.items() if value >= 0}

    @classmethod
    def is_turn_completed(cls, actor_id, state):
        """has no more available game moves for those that are available"""
        return 0 == len(cls.get_available_game_move_keys(actor_id, state))

    @classmethod
    def make_game_move_command(cls, actor_id, state):
        move_selection = cls.choose_game_move(actor_id, state)
        return state.actors[actor_id].game_moves[move_selection].make_command(state)

    @classmethod
    def find_movement_destination(cls, actor_id, state):
        return

    @classmethod
    def get_nearest_enemy_id(actor_id, state):
        enemy_dists = {}
        for enemy_id in [
            enemy_id for enemy_id in aiutils.get_enemy_ids(actor_id, state) if not state.actors[enemy_id].is_dead()
        ]:
            enemy_dists[enemy_id] = pathingutils.measure_distance(
                state.actors[actor_id].loc, state.actors[enemy_id].loc
            )

        return min(enemy_dists, key=enemy_dists.get)

    # @staticmethod
    # def take_turn(state, actor_id):
