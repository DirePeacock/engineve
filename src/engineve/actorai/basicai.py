from ..enginecommands.gamecommands.attackcommand import AttackCommand

class BasicAI():
    '''class for making decision based on state and args thru static methods'''

    @classmethod
    def choose_game_move(cls, actor_id, state):
        keys = cls.get_available_game_move_keys(actor_id, state)
        # TODO make this smart
        if len(keys) > 0:
            return keys[0]
        return None
    
    @classmethod
    def get_available_game_move_keys(cls, actor_id, state):
        return [key for key, game_move in state.actors[actor_id].game_moves.items() if game_move.is_available(actor_id, state)]

    @classmethod
    def is_turn_completed(cls, actor_id, state):
        '''has no more available game moves for those that are available'''
        return 0 == len(cls.get_available_game_move_keys(actor_id, state))

    @classmethod
    def make_game_move_command(cls, actor_id, state):
        move_selection = cls.choose_game_move(actor_id, state)
        return state.actors[actor_id].game_moves[move_selection].make_command(actor_id, state)

    # @staticmethod
    # def take_turn(state, actor_id):
        
            
