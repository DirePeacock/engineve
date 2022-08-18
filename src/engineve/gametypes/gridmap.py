from ..serializable import Serializable
from ..tags import TaggedClass


class GridLoc(Serializable, TaggedClass):
    #### TODO  how does this relate to the Loc class?
    def __init__(self, difficult_terrain=False, obscuration=0, passible=True, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.difficult_terrain = difficult_terrain
        self.obscuration = obscuration
        self.passible = passible


class GridMap(Serializable, TaggedClass):
    def __init__(self, w=10, h=10, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.locs = [[GridLoc() for y in range(0, h)] for x in range(0, w)]

        # this doesn't follow with the other ones but we may want this referenced for
        # use determining loc occupancy

    def check_occupancy(self, loc, state):
        for actor_id in state.combat.order.values():
            if state.actors[actor_id].loc.coords == loc.coords:
                return True
        return False

    def get_actor_locs_dict(self, state):
        return {actor_id: state.actors[actor_id].loc for actor_id in state.combat.order.values()}

    def serialize(self):
        # todo idk
        return {"GridLoc": "not used"}
