import logging
import random
from .enginestate import EngineState
from ..archetypes.archetype import new_monster
from ..enginecommands.effectcommands.restcommand import RestCommand
from ..utils import roll, get_random_coords
from ..config import constants
from ..gametypes.loc import Loc

# from .combatstate import CombatState
from ..gametypes.combat import Combat


class OverworldState(EngineState):
    """this class should idk, wait to do stuff i guess?
    TODO how to handle menu inputs n stuff"""

    _combat_state: type = None

    def __init__(self, ready=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ready = ready
        self.i = 0
        self.wait_frames = 1

    def periodic(self, state, invoker):
        if self.ready:
            self.start_combat(state, invoker)

        # else:
        #     pass
        #     self.ready = True
        # if i > self.wait_frames:
        #     pass
        # else:
        #     self.i += 1

    def randomize_actor_locs(self, actor_ids, state):
        max_x = state.gridmap.width - 1
        max_y = state.gridmap.height - 1
        for actor_id in actor_ids:
            team = state.actors[actor_id].team
            min_x_spawn = 0 if (team % 2 == 0) else max_x // 2
            max_x_spawn = max_x - (max_x // 2) if (team % 2 == 0) else max_x
            x_range = (min_x_spawn, max_x_spawn)
            y_range = (0, max_y)

            new_loc = get_random_coords(x_range, y_range)
            while state.gridmap.check_occupancy(
                loc=new_loc, state=state, relevant_ids=[i for i in actor_ids if i != actor_id]
            ):
                new_loc = get_random_coords(x_range, y_range)
            state.actors[actor_id].loc = Loc(new_loc)

    def start_combat(self, state, invoker, num_roll="1d3"):
        # logging.debug("startingcombat")
        invoker.put(RestCommand(state.party.actor_ids))
        self.i = 0
        team_id = constants.MONSTER_TEAM_ID

        num_monsters = roll(num_roll)

        for i in range(random.randint(1, num_monsters)):
            state.add_actor(new_monster("skeleton", team=team_id))

        some_ids = [actor_id for actor_id, actor in state.actors.items() if actor.team in [team_id, state.party.team]]
        self.randomize_actor_locs(some_ids, state)
        state.combat = Combat(actor_ids=some_ids)
        mobs = len([mob for mob in state.combat.actor_ids if mob not in state.party.actor_ids])
        # state.log.append()
        self.transition_to(self._combat_state(actor_ids=some_ids))
