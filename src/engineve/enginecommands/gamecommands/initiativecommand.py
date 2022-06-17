import logging

from ..basecommands.compositecommand import CompositeCommand
from .abilitycheckcommand import AbilityCheckCommand
from ..effectcommands.initiative import Initiative
class InitiativeCommand(CompositeCommand):
    def __init__(self, actor_ids, *args, **kwargs):
        '''make a skill check command for every actor_id'''
        super().__init__(*args, **kwargs)
        self.actor_ids = actor_ids
        self.add_tag('actor_ids', self.actor_ids)
        self.add_tag('log')
        for actor_id in self.actor_ids:
            self.children[actor_id] = AbilityCheckCommand(actor_id=actor_id, ability='dex')

    def evaluate(self, state):
        super().evaluate(state)
        self.value = {}
        for actor_id, init_command in self.children.items():
            init_score = init_command.value + (0.01 * float(state.actors[actor_id].dex))
            if init_score not in self.value.keys():
                self.value[init_score] = actor_id
            else:
                while init_score in self.value.keys():
                    init_score += 0.001
                self.value[init_score] = actor_id
        self.effects.append(Initiative(self.value))
        log_dict = {key: state.actors[val].name for key, val in self.value.items()}
        self.log = f"init = {log_dict}"
        