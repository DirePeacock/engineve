import logging

from ..basecommands.command import Command
from ..effectcommands.changeloc import ChangeLoc
from ...utils import roll

class ChangeLocCommand(Command):
    '''roll attack to hit, evaluate if it hits or whatever
    '''
    def __init__(self, actor_id, locpath=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actor_id = actor_id
        self.locpath = [] if locpath is None else locpath
        self.add_tag('actor_ids', [actor_id])
        self.add_tag('loc_path', self.locpath)
        self.add_tag('log', None)
    
    def evaluate(self, state):
        for loc in self.locpath:
            self.effects.append(ChangeLoc(self.actor_id, loc))
        self.log = f"{state.actors[self.actor_id].name} moves {state.actors[self.actor_id].loc} -> {self.locpath[-1]}"