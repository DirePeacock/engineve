import logging

from .gamestatemanager import GameStateManager
from .enginecommands.invoker import Invoker
from .enginestates.combatstate import CombatState
from .enginestates.menustate import MenuState
from .enginestates.landingstate import LandingState
from .enginesync import EngineSync
from .durationobserver import DurationObserver
from .archetypes.archetype import new_monster
from .loader import Loader
from .serializable import Serializable
from .tags import TAGS


class GameEngine(Loader, Serializable):
    """this is the top,
    -   it has an invoker
    -   it has a gamestate of in-game objects
    -   engine_state is a state of the engine that has a main method for its particular function

    this uses the periodic method of the current_engine state to find commands for the invoker to execute .
    """

    # used as a default val in some places

    blacklist_strs = ["duration_observer", "invoker", "engine_sync"]

    fps = 60
    _state_transition_await_frames = 0

    def __init__(self, save_slot="auto", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_state = (
            GameStateManager() if "game_state" not in kwargs.keys() else GameStateManager(**kwargs["game_state"])
        )
        self.engine_sync = EngineSync(self)
        self.invoker = Invoker(log=self.game_state.log)
        self.duration_observer = DurationObserver()

        self.frame = 0
        self.engine_state = None

        self.invoker.register_observer(self.duration_observer)
        self.invoker.register_observer(self.engine_sync)
        self.transition_to(MenuState(ready=False))
        self._save_slot = save_slot

    def periodic(self):
        if not self.engine_sync.is_waiting():
            self.engine_state.periodic(self.game_state, self.invoker)
            # # Q: should this be in the engine_state?
            # # A: probly not
            self.invoker.periodic(self.game_state)

        # do @ end of every frame and in this order
        self.engine_sync.periodic()
        self.frame += 1

    def spawn_actors(self, actor_class, num=1, **kwargs):
        for some_actor in GameEngine.generate_actors(actor_class, num, **kwargs):
            self.game_state.add_actor(some_actor)

    def pick_party(self, names=(), ids=None, team=0):
        a_ids = []
        if ids is not None:
            a_ids = ids
        else:
            for name in names:
                for actor in self.game_state.actors.values():
                    if name.lower() == actor.name.lower():
                        a_ids.append(actor.id)
                        break

        self.game_state.party.actor_ids = a_ids
        self.game_state.party.team = team
        for a_id in a_ids:
            self.game_state.actors[a_id].team = team

    @staticmethod
    def generate_actors(actor_class, num=1, **kwargs):
        return [actor_class(**kwargs) for i in range(0, num)]

    def register_observer(self, observer):
        """hook in something like the graphics engine as an observer"""
        self.invoker.register_observer(observer)

    def start_combat(self, num):
        if "MenuState" == type(self.engine_state).__name__:
            logging.debug(f"starting combat with {num} skeletons per side")
            self.engine_state.start_combat(num=num, state=self.game_state, invoker=self.invoker)

    def stop_combat(self, num):
        if "CombatState" == type(self.engine_state).__name__:
            logging.debug(f"starting combat with {num} skeletons per side")
            self.engine_state.end_combat(num=num, state=self.game_state, invoker=self.invoker)

    def transition_to(self, engine_state):
        new_state_name = type(engine_state).__name__
        logging.debug(f"{type(self.engine_state).__name__} to {new_state_name}")
        self.engine_state = engine_state
        self.engine_state.engine = self
        notice_meta = {TAGS["engine_state_transition"], new_state_name}
        if self._state_transition_await_frames > 0:
            notice_meta[TAG["animation"]] = self._state_transition_await_frames
        self.invoker.notify(meta=notice_meta, state=self.game_state, invoker=self.invoker)

    def spawn_archetype(self, archetype_name, **kwargs):
        new_actor = new_monster(archetype_name, **kwargs)
        self.game_state.add_actor(new_actor)
        return new_actor.id

    def import_character(self, *args, **kwargs):
        actor = super().load_character(*args, **kwargs)
        if actor is not None:
            return self.game_state.add_actor(actor)

    def garbage_collection(self):
        """delete things that take up too much memory or that we miss frequently"""
        pass

    def serialize(self):
        retval = super().serialize()
        return retval
