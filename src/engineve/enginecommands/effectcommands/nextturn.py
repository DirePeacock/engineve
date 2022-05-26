import logging

from .effectcommand import EffectCommand

class NextTurn(EffectCommand):
    def apply(self, state):
        curr_i = state.combat.i
        next_i = state.combat.get_next_init(state)

        #notify?
        logging.debug(f"{state.actors[state.combat.order[curr_i]].name}@{curr_i} - turn ended")
        logging.debug(f"{state.actors[state.combat.order[next_i]].name}@{next_i} - turn began")
        

        state.combat.i = next_i
