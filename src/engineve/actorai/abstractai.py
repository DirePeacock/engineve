from abc import ABCMeta, abstractmethod

class AbstractAI(metaclass=ABCMeta):
    "The command interface, that all commands will implement"
    
    @staticmethod
    @abstractmethod
    def is_turn_completed(state, actor_id):
        """ The required execute method that all command objects will use"""
        

    @staticmethod
    @abstractmethod
    def select_game_move(state, actor_id):
        """select a move from those available for that actor"""
    

    