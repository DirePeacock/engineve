import logging

from .enginestate import EngineState
from ..enginecommands.gamecommands.nextturncommand import NextTurnCommand
from ..enginecommands.gamecommands.initiativecommand import InitiativeCommand

class CombatState(EngineState):
    '''I move the engine through combat, the state of a combat is stored in the gametypes.combat'''
    _post_combat_state: type = None

    def __init__(self, actor_ids=None, *args, **kwargs):
        super().__init__(args, kwargs)
        # this will probably be set to something when the transition to combat happens ?
        # TODO engine transition?
        self.actor_ids = [] if actor_ids is None else actor_ids

    def periodic(self, state, invoker):
        # switch what_do

        if not state.combat.active or 0 == len(state.combat.order.keys()):  # TODO how to end combat
            self.start_combat(state, invoker)

        elif state.combat.is_done(state):
            self.end_combat(state, invoker)
        
        elif state.combat.active:
            if self.is_turn_done(state, invoker):
                self.next_turn(state, invoker)
            else:
                self.actor_make_game_move(state, invoker)

        else:
            logging.warning(f"sorry something's gone wrong.")
            self.end_combat(state, invoker)

    def is_turn_done(self, state, invoker):
        return state.actors[state.combat.get_current_actor_id()].is_turn_completed(state)

    def start_combat(self, state, invoker):
        state.combat.active = True
        self.roll_inits(state, invoker)
        

    def roll_inits(self, state, invoker):
        invoker.put(InitiativeCommand(self.actor_ids))
    
    def next_turn(self, state, invoker):
        '''do next trurn command'''
        invoker.put(NextTurnCommand())
        
    
    def actor_make_game_move(self, state, invoker):
        '''if things to do put commands on the stack'''
        invoker.put(state.actors[state.combat.get_current_actor_id()].make_game_move_command(state))
        
    def end_combat(self, state, invoker):
        state.combat.active = False
        self.transition_to(self._post_combat_state())

