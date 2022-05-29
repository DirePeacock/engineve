from ...utils import roll
from ..basecommands.command import Command

class AbilityCheckCommand(Command):
    '''roll attack to hit, evaluate if it hits or whatever
    '''
    def __init__(self, actor_id, ability, skill=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actor_id = actor_id
        self.ability = ability
        self.skill = skill

    def evaluate(self, state):
        super().evaluate(state)
        ability_mod = state.actors[self.actor_id].get_ability_modifier(self.ability)
        prof_bonus = 0
        self.value = ability_mod + prof_bonus + roll(size=20)
