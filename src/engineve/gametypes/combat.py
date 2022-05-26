from ..serializable import Serializable
from ..tags import TaggedClass


class Combat(Serializable, TaggedClass):
    def __init__(self, ids, active=False, *args, **kwargs):
        # super().__init__(args, kwargs)
        self.ids = ids
        self.order = {}
        self.active = active
        self.current_iter = None

    def _get_max(self, state):
        return max([key for key, _val in self.order.items() if not state.actors[_val].is_dead()]) 
        
    def get_next_init(self, state):
        active_entries = {key: val for key, val in self.order.items() if not state.actors[val].is_dead()}
        if len(active_entries) == 1:
            raise StopIteration

        lower_entries = {key: val for key, val in active_entries.items() if key < self.current_iter}

        next_init_val = None
        if len(lower_entries) < 1:
            next_init_val = max(active_entries.keys())
        else:
            next_init_val = max(lower_entries.keys())

        self.current_iter = next_init_val
        return self.order[next_init_val]

