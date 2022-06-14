import logging

from .gamestatemanager import GameStateManager
from .enginecommands.invoker import Invoker
from .enginestates.combatstate import CombatState
from .enginestates.menustate import MenuState
from .enginestates.landingstate import LandingState
from .enginesync import EngineSync

class GameEngine():
    '''this is the top, 
    -   it has an invoker
    -   there is a gamestate of in-game objects
    -   engine_state is a state of the engine that knows what it's main method to do
    
    this uses the periodic method of the current_engine state to find commands for the invoker to execute .
    '''
    # used as a default val in some places
    fps=60
    def __init__(self):
        
        self.game_state = GameStateManager()
        self.engine_sync = EngineSync(self)
        self.invoker = Invoker(log=self.game_state.log)
        
        self.frame = 0
        self.engine_state = None
        
        self.invoker.register_observer(self.engine_sync)
        self.transition_to(MenuState(ready=False))
        

    def periodic(self):
        if not self.engine_sync.is_waiting():
            self.engine_state.periodic(self.game_state, self.invoker)
            # TODO should this be in the engine_state? 
            # # A: probly not
            self.invoker.periodic(self.game_state)
        
        # do @ end of every frame and in this order
        self.engine_sync.periodic()
        self.frame += 1

    def spawn_actors(self, actor_class, num=1, **kwargs):
        for some_actor in GameEngine.generate_actors(actor_class, num, **kwargs):
            self.game_state.add_actor(some_actor)
    
    @staticmethod
    def generate_actors(actor_class, num=1, **kwargs):
        return [actor_class(**kwargs) for i in range(0, num)]

    def add_observer(self, observer):
        '''hook in something like the graphics engine as an observer'''
        return

    def transition_to(self, engine_state):
        # logging.debug(f"{type(self.engine_state).__name__} to {type(engine_state).__name__}")
        if 'CombatState' == type(self.engine_state).__name__:
            logging.debug('done with combat. gg')
            
        self.engine_state = engine_state
        self.engine_state.engine = self
