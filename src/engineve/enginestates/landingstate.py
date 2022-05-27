import logging

from .enginestate import EngineState
# from .combatstate import CombatState
from ..gametypes.combat import Combat

class LandingState(EngineState):
    _combat_state: type = None

    def periodic(self, state, invoker):
        self.start_combat(state, invoker)
    
    def start_combat(self, state, invoker):
        logging.debug('startingcombat')
        some_ids = [actor_id for actor_id in state.actors.keys()]
        # TODO should starting a combat be a command or something observable, idk
        for actor_id in some_ids:
            state.actors[actor_id].hp = state.actors[actor_id].max_hp
            
        state.combat = Combat(actor_ids=some_ids)
        self.transition_to(self._combat_state(actor_ids=some_ids))
