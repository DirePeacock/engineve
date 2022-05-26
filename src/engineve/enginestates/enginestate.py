# from .enginestateinterface import EngineStateInterface

class EngineState():
    "The command interface, that all commands will implement"
    @property
    def engine(self):
        return self._engine

    @engine.setter
    def engine(self, engine):
        self._engine = engine

    def __init__(self, *args, **kwargs):
        pass

    def periodic(self, state, invoker):
        """called every frame, or more often depending on game_clock_speed
        """
        return

    def transition_to(self, engine_state):
        '''change state of parent game_engine objecct'''
        # having self.engine as a pointer everywhere makes passing state & invoker around all over seem weird
        # EngineStates do not have ownership of the state or the invoker
        self.engine.transition_to(engine_state)