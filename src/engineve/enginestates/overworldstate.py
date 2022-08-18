import logging
import random
from .enginestate import EngineState
from ..archetypes.archetype import new_monster
from ..enginecommands.effectcommands.restcommand import RestCommand

# from .combatstate import CombatState
from ..gametypes.combat import Combat


class OverworldState(EngineState):
    """this class should idk, wait to do stuff i guess?
    TODO how to handle menu inputs n stuff"""

    _combat_state: type = None

    def __init__(self, ready=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ready = ready

    def periodic(self, state, invoker):
        if self.ready:
            self.start_combat(state, invoker)
        else:
            invoker.put(RestCommand(state.party.actor_ids))
            self.ready = True

    def start_combat(self, state, invoker):
        logging.debug("startingcombat")

        team_id = 42
        for i in range(random.randint(1, 3)):
            state.add_actor(new_monster("skeleton", team=team_id))

        some_ids = [actor_id for actor_id, actor in state.actors.items() if actor.team in [team_id, state.party.team]]

        logging.debug(f"we have {len(state.actors.keys())} actors")
        state.combat = Combat(actor_ids=some_ids)
        self.transition_to(self._combat_state(actor_ids=some_ids))
