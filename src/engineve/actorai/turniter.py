

# TODO may not be useful
class CombatActorIterator():
    '''i go through choices, resources and actions of an actors turn and end when turn is done'''
    def __init__(self, game_state, actor_id):
        self.GAME_STATE = game_state
        self.actor_id
    
    
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