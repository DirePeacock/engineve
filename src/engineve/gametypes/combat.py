from ..serializable import Serializable
from ..tags import TaggedClass


class Combat(Serializable, TaggedClass):
    def __init__(self, actor_ids=None, active=False, *args, **kwargs):
        # super().__init__(args, kwargs)
        self.actor_ids = [] if actor_ids is None else actor_ids
        self.active = active
        self.current_iter = None

        # dict of init_score: actor_id
        self.order = {}
        self.winning_team = None

    def get_active_entries(self, state):
        return {init: actor_id for init, actor_id in self.order.items() if not state.actors[actor_id].is_dead()}

    def get_active_actor_ids(self, state):
        return [actor_id for actor_id in self.get_active_entries(state).values()]

    def _get_max(self, state):
        return max([init for init, actor_id in self.order.items() if not state.actors[actor_id].is_dead()])

    def get_next_init(self, state):
        active_entries = self.get_active_entries(state)
        if len(active_entries) <= 1:
            return self.current_iter

        lower_entries = {init: actor_id for init, actor_id in active_entries.items() if init < self.current_iter}

        next_init_val = None
        if len(lower_entries) < 1:
            next_init_val = max(active_entries.keys())
        else:
            next_init_val = max(lower_entries.keys())

        return next_init_val

    def get_current_actor_id(self):
        return self.order[self.current_iter] if self.current_iter in self.order.keys() else -1

    def is_done(self, state):
        active_entries = self.get_active_entries(state)
        active_teams = []
        for init, actor_id in active_entries.items():
            team_id = state.actors[actor_id].team
            if team_id not in active_teams:
                active_teams.append(team_id)

        is_combat_done = 1 >= len(active_teams)
        if is_combat_done:
            self.winning_team = active_teams[0]
        return is_combat_done
