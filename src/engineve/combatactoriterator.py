class CombatActorIterator():
    def __init__(self, game_state, ids=None):
        self.GAME_STATE = game_state
        self.order = self._roll_inits(ids if ids is not None else list(self.GAME_STATE.actors.keys()))
        self.i = self._get_max()

    def _roll_inits(self, ids):
        rv = {self.GAME_STATE.actors[id].roll_initiative(): id for id in ids}
        return rv
    def _get_max(self):
        return max(self.order.keys()) 
    def __iter__(self):
        return self
    def __next__(self):
        active_entries = {key: val for key, val in self.order.items() if self.GAME_STATE.actors[val].hp > 0}
        if len(active_entries) == 1:
            raise StopIteration

        lower_entries = {key: val for key, val in active_entries.items() if key < self.i}
        next_val = None

        if len(lower_entries) < 1:
            next_init_val = max(active_entries.keys())
        else:
            next_init_val = max(lower_entries.keys())
        self.i = next_init_val
        return self.order[next_init_val]

