import logging

from ..basecommands.compositecommand import CompositeCommand
from .abilitycheckcommand import AbilityCheckCommand

class InitiativeCommand(CompositeCommand):
    def __init__(self, actor_ids, *args, **kwargs):
        '''make a skill check command for every actor_id'''
        super().__init__(args, kwargs)
        self.actor_ids = actor_ids
        for actor_id in self.actor_ids:
            self.children[actor_id] = AbilityCheckCommand(actor_id=actor_id, ability='dex')

    def evaluate(self, state):
        super().evaluate(state)
        self.value = {}
        for actor_id, child_command in self.children:
            self.value[actor_id] = child_command.value + (0.01 * float(state.actors[actor_id].dex))
        