import logging

from ..basecommands.compositecommand import CompositeCommand
from .abilitycheckcommand import AbilityCheckCommand
from ..effectcommands.initiative import Initiative
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
        for actor_id, init_command in self.children.items():
            init_score = init_command.value + (0.01 * float(state.actors[actor_id].dex))
            self.value[init_score] = actor_id
        self.effects.append(Initiative(self.value))
        