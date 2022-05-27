import logging
from ..basecommands.command import Command
from ..effectcommands.changeturn import ChangeTurn

class NextTurnCommand(Command):
    '''may not need to store the data on init TODO check later'''
    def evaluate(self, state):
        curr_i = state.combat.current_iter
        next_i = state.combat.get_next_init(state)

        #notify?
        logging.debug(f"{state.actors[state.combat.order[curr_i]].name}@{curr_i} - turn ended")
        logging.debug(f"{state.actors[state.combat.order[next_i]].name}@{next_i} - turn began")
        
        self.effects.append(ChangeTurn(old_init=curr_i, next_init=next_i))