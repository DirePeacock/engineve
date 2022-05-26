from .enginestateinterface import EngineStateInterface

class EngineState(EngineStateInterface):
    "The command interface, that all commands will implement"
    def __init__(self, *args, **kwargs):
        pass

    def periodic(self, state, invoker):
        """called every frame, or more often depending on game_clock_speed
        if waiting
            return
        
        if stack_empty, 
        
        resolve
        """
        return
        
    
    def transition(self, next_engine_state):
        '''calculate effect and undo'''
        pass
