from .enginestate import EngineState
from ..enginecommands.effectcommands.nextturn import NextTurn
from ..enginecommands.gamecommands.initiativecommand import InitiativeCommand

class CombatState(EngineState):
    ''' TODO: WTF do i not do that the combat object does? should i delete that thing?(probly)'''
    def __init__(self, actor_ids=None, *args, **kwargs):
        super().__init__(args, kwargs)
        # this will probably be set to something when the transition to combat happens ?
        # TODO engine transition
        self.actor_ids = [] if actor_ids is None else actor_ids

    def periodic(self, state, invoker):
        # switch what_do
        if not state.combat.active:
            self.start_combat(state, invoker)
        if state.combat.active:
            if self.is_turn_done(state, invoker):
                self.next_turn(state, invoker)
            else:
                self.take_turn(state, invoker)
        else:
            self.end_combat(state, invoker)

    def is_turn_done(self, state, invoker):
        return state.actors[state.combat.current_iter].is_turn_done(state)

    def start_combat(self, state, invoker):
        self.roll_inits(state, invoker)

    def roll_inits(self, state, invoker):
        state.combat.active = True
        invoker.put(InitiativeCommand(self.actor_ids))
    
    def next_turn(self, state, invoker):
        '''do next trurn command'''
        invoker.put(NextTurn())
        
    
    def take_turn(self, state, invoker):
        '''if things to do put commands on the stack'''
        invoker.put(state.actors[state.combat.current_iter].make_game_move_command(state))
        
    def end_combat(self, state, invoker):
        pass

