import logging
from .utils import get_id
from .enginecommands.observer.observer import Observer
from .tags import TAGS, check_tag
from .gametypes.time import roundsdelta


class DurationObserver(Observer):
    def __init__(self):
        super().__init__(trigger=self._is_gametime_updated, reaction=self.clean_up)

    def _is_gametime_updated(self, meta, state):
        return check_tag(meta, TAGS.gametime_update)

    def clean_up(self, meta, state, invoker):
        """this is before the gametime has updated"""
        logging.debug(f"game_time = {state.time}")
        logging.debug(f"tagged_time = {meta[TAGS.gametime_update]}")
        # clear out global effects
        for effect_id in state.global_effects.keys():
            if state.global_effects[effect_id].duration is not None:
                effect_age = meta[TAGS.gametime_update] - state.global_effects[effect_id].start_time
                if roundsdelta(state.global_effects[effect_id].duration) <= effect_age:
                    invoker.unregister_observer(state.global_effects[effect_id])
                    del state.global_effects[effect_id]
        # clear out actor effects
        for actor_id in state.actors.keys():
            delete_these_effect_ids = []  # don't change length of dict while its in the for loop generator
            for effect_id in state.actors[actor_id].effects.keys():
                if state.actors[actor_id].effects[effect_id].duration is not None:
                    effect_age = meta[TAGS.gametime_update] - state.actors[actor_id].effects[effect_id].start_time
                    if roundsdelta(state.actors[actor_id].effects[effect_id].duration) <= effect_age:
                        delete_these_effect_ids.append(effect_id)
            # now delete these
            for e_id in delete_these_effect_ids:
                invoker.unregister_observer(state.actors[actor_id].effects[e_id])
                state.actors[actor_id].effects.pop(e_id)
