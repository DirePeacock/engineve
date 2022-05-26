import logging

from .enginestate import EngineState
from .combatstate import CombatState

class LandingState(EngineState):
    def transition(self, next_engine_state):
        pass

    def periodic(self, state, invoker):
        self.start_combat(state, invoker)
    
    def start_combat(self, state, invoker):
        logging.debug('startingcombat')
        self.transition_to(CombatState(actor_ids=[actor_id for actor_id in state.actors.keys()]))
