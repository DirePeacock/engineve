import logging
from ..basecommands.command import Command
from ..effectcommands.changeturn import ChangeTurn
from ..effectcommands.incrementgametime import IncrementGameTime


class NextTurnCommand(Command):
    """may not need to store the data on init TODO check later"""

    def evaluate(self, state, invoker=None):
        curr_i = state.combat.current_iter
        next_i = state.combat.get_next_init(state)
        if next_i > curr_i:
            # if we start jumping around the turn order, this will have to be amended
            self.add_tag("next_round")
            self.effects.append(ChangeTurn(old_init=curr_i, next_init=next_i))
            self.effects.append(IncrementGameTime(rounds=1))

        self.add_tag("end_turn", state.combat.order[curr_i])

        self.add_tag("start_turn", state.combat.order[next_i])
        self.effects.append(ChangeTurn(old_init=curr_i, next_init=next_i))
