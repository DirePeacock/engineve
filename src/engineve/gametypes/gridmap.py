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
    def __init__(self, width=10, height=10, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.width = width
        self.height = height

        self.locs = [[GridLoc() for y in range(0, self.height)] for x in range(0, self.width)]

        # this doesn't follow with the other ones but we may want this referenced for
        # use determining loc occupancy

    def check_occupancy(self, loc, state, relevant_ids=None):
        """you can pass in relevant ids if you want"""
        loc_tuple = loc if isinstance(loc, tuple) else loc.coord
        relevant_ids = relevant_ids if relevant_ids is not None else state.combat.order.values()
        for actor_id in relevant_ids:
            # TODO FIX THIS BRO, this will be too much type checking, maybe just remove the loc type obj
            actor_loc_tuple = (
                state.actors[actor_id].loc
                if isinstance(state.actors[actor_id].loc, tuple)
                else state.actors[actor_id].loc.coord
            )
            if actor_loc_tuple == loc_tuple:
                return True
        return False

    def get_actor_locs_dict(self, state):
        return {actor_id: state.actors[actor_id].loc for actor_id in state.combat.order.values()}

    def serialize(self):
        # todo idk
        return {"GridLoc": "not used"}
