from ..serializable import Serializable


class Party(Serializable):
    def __init__(self, actor_ids=None, team=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actor_ids = [] if actor_ids is None else actor_ids
        self.team = team

    def get_names(self, state):
        """this may not be needed"""
        return [state.actors[a_id].name for a_id in self.actor_ids if a_id in state.actors.keys()]
