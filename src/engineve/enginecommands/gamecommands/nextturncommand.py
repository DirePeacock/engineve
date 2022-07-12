import logging
from ..basecommands.command import Command
from ..effectcommands.changeturn import ChangeTurn

class NextTurnCommand(Command):
    '''may not need to store the data on init TODO check later'''
    def evaluate(self, state):
        curr_i = state.combat.current_iter
        next_i = state.combat.get_next_init(state)

        self.add_tag('end_turn')
        self.add_tag('start_turn')
        self.effects.append(ChangeTurn(old_init=curr_i, next_init=next_i))