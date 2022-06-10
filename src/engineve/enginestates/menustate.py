import logging

from .enginestate import EngineState
# from .combatstate import CombatState
from ..gametypes.combat import Combat

class MenuState(EngineState):
    '''this class should idk, wait to do stuff i guess?
    TODO how to handle menu inputs n stuff'''
    _combat_state: type = None
    def __init__(self, ready=False,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ready=ready
    
    def periodic(self, state, invoker):
        if self.ready:
            self.start_combat(state, invoker)
        else:
            pass
    
    def start_combat(self, state, invoker):
        logging.debug('startingcombat')
        some_ids = [actor_id for actor_id in state.actors.keys()]
        # TODO should starting a combat be a command or something observable, idk
        for actor_id in some_ids:
            state.actors[actor_id].hp = state.actors[actor_id].max_hp
            
        state.combat = Combat(actor_ids=some_ids)
        self.transition_to(self._combat_state(actor_ids=some_ids))
