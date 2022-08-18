import logging

from .enginestate import EngineState
from ..archetypes.archetype import new_monster

# from .combatstate import CombatState
from ..gametypes.combat import Combat


class MenuState(EngineState):
    """this class should idk, wait to do stuff i guess?
    TODO how to handle menu inputs n stuff"""

    _combat_state: type = None
    _overworld_state: type = None

    def __init__(self, ready=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ready = ready

    def periodic(self, state, invoker):
        if self.ready:
            self.open_overworld(state, invoker)
        else:
            self.uhh_setup()

    # def load_party(self, state, invoker):
    #     # loaded_actor_ids = []
    #     state.party.actor_ids = loaded_actor_ids
    def uhh_setup(self):
        # TODO idk get input or something idk
        chars = ["solaire"]
        for char in chars:
            self._engine.import_character(char)
        self._engine.pick_party(chars)
        self.ready = True

    def open_overworld(self, state, invoker):
        self.transition_to(self._overworld_state())

    # def start_combat(self, num, state, invoker):
    #     logging.debug("startingcombat")

    #     # TODO should starting a combat be a command or something observable, idk
    #     # TODO don't spawn skeletons?

    #     for team_id in [0, 1]:
    #         for i in range(num):
    #             state.add_actor(new_monster("skeleton", team=team_id))
    #     some_ids = [actor_id for actor_id in state.actors.keys()]
    #     logging.debug(f"we have {len(state.actors.keys())} actors")
    #     state.combat = Combat(actor_ids=some_ids)
    #     self.transition_to(self._combat_state(actor_ids=some_ids))
