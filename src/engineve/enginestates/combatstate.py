import logging
import random

from .enginestate import EngineState
from ..enginecommands.gamecommands.nextturncommand import NextTurnCommand
from ..enginecommands.gamecommands.initiativecommand import InitiativeCommand
from ..enginecommands.effectcommands.changeloc import ChangeLoc

class CombatState(EngineState):
    '''I move the engine through combat, the state of a combat is stored in the gametypes.combat'''
    _post_combat_state: type = None

    def __init__(self, actor_ids=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # this will probably be set to something when the transition to combat happens ?
        # TODO engine transition?
        self.actor_ids = [] if actor_ids is None else actor_ids

    def periodic(self, state, invoker):
        # switch what_do
        if not state.combat.active or 0 == len(state.combat.order.keys()):  # TODO how to end combat
            self.start_combat(state, invoker)

        elif state.combat.is_done(state):
            self.declare_victory(state, invoker)
            self.end_combat(state, invoker)
            
        elif state.combat.active:
            if self.is_turn_done(state, invoker):
                self.next_turn(state, invoker)
            else:
                self.actor_make_game_move(state, invoker)

        else:
            logging.warning(f"sorry something's gone wrong.")
            self.end_combat(state, invoker)

    def declare_victory(self, state, invoker):
        actor_names = [state.actors[a_id].name for a_id in state.combat.order.values() if state.actors[a_id].team == state.combat.winning_team] 
        log_entry = " ".join((f"party {state.combat.winning_team} of", ", ".join(actor_names), "is victorious"))
        state.log.write(log_entry)

    def is_turn_done(self, state, invoker):
        return state.actors[state.combat.get_current_actor_id()].is_turn_completed(state)

    def start_combat(self, state, invoker):
        state.combat.active = True
        self.roll_inits(state, invoker)
        #TODO spawn locations
        self.randomize_locs(state, invoker)

    def roll_inits(self, state, invoker):
        invoker.put(InitiativeCommand(self.actor_ids))
    
    def randomize_locs(self, state, invoker):
        for actor_id in self.actor_ids:
            random_loc = (random.randint(0,9), random.randint(0,9))
            while state.gridmap.check_occupancy(random_loc, state):
                random_loc = (random.randint(0,9), random.randint(0,9))
            invoker.command_stack[0].effects.append(ChangeLoc(actor_id, random_loc))

    def next_turn(self, state, invoker):
        '''do next trurn command'''
        invoker.put(NextTurnCommand())
        
    
    def actor_make_game_move(self, state, invoker):
        '''if things to do put commands on the stack'''
        invoker.put(state.actors[state.combat.get_current_actor_id()].make_game_move_command(state))
        
    def clean_up_combat(self, state, invoker):
        for actor_id in state.combat.order.values():
            if actor_id in state.actors.keys() and state.actors[actor_id].delete_after_combat:
                del state.actors[actor_id]

    def end_combat(self, state, invoker):
        state.combat.active = False
        self.clean_up_combat(state, invoker)
        import logging
        logging.debug('combat')
        self.transition_to(self._post_combat_state())

