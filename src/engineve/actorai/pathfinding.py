from . import pathingutils

"""pathing logic"""


def _tech_demo_spoof(actor_id, destination, state):
    return [destination]


def find_path(actor_id, destination, state):
    # TODO implement: hey future me! don't put this in prod!
    return _tech_demo_spoof(actor_id, destination, state)


def is_coord_in_bounds(coord, gridmap):
    return coord[0] < gridmap.width and coord[1] < gridmap.height


def nearest_unoccupied_space(destination, state, grid_range=10, blacklist=()):
    """expanding radially outward then clockwise from NW corner search for"""
    actor_locs_dict = state.gridmap.get_actor_locs_dict(state)

    for r in range(0, grid_range + 1):
        valid_loc_distances = {
            coord: pathingutils.measure_distance(coord, destination)
            for coord in pathingutils.get_radial_square_locs(center=destination, r=r)
            if coord not in blacklist
            and coord not in actor_locs_dict.values()
            and is_coord_in_bounds(coord, state.gridmap)
        }
        if 0 < len(valid_loc_distances):
            return min(valid_loc_distances, key=valid_loc_distances.get)
