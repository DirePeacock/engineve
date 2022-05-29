radial_square_sides = ['north', 'east', 'south', 'west']

def measure_distance(loc_a, loc_b):
    '''consider a east triangle b/w loc_a & loc_b return longest non-hypotenuse side of that triangle'''
    return max([abs(loc_a[i] - loc_b[i]) for i in range(0, min(len(loc_a), len(loc_b)))])

# ASSUMPTION coords are all positive numbers
def _north_side(center, r):
    y = center[1] + r
    start = (center[0] - r)
    stop = (center[0] + r)
    return [(x,y) for x in range(start, stop) if x >=0 and y >= 0]

def _east_side(center, r):
    x = center[0] + r
    start = (center[1] + r)
    stop = (center[1] - r)
    step = -1
    return [(x,y) for y in range(start, stop, step) if x >=0 and y >= 0]

def _south_side(center, r):
    y = center[1] - r
    start = (center[0] + r)
    stop = (center[0] - r)
    step = -1
    return [(x,y) for x in range(start, stop, step) if x >=0 and y >= 0]
    

def _west_side(center, r):
    x = center[0] - r
    start = (center[1] - r)
    stop = (center[1] + r)
    return [(x,y) for y in range(start, stop) if x >=0 and y >= 0]

sq_side_funcs = {
    'north':_north_side, 
    'east':_east_side, 
    'south':_south_side, 
    'west':_west_side, 
}
def get_radial_square_locs(center, r):
    return [loc for func in sq_side_funcs.values() for loc in func(center, r)]

