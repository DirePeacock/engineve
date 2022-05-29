import includes
from engineve.actorai.pathingutils import get_radial_square_locs

def test_radial_squares():
    '''values should be tuples in the right order and not negative'''
    center=(1,1)    
    radius_expected_vals=[
        [center],
        [(0,2), (1,2), (2,2), (2,1), (2,0), (1,0), (0,0), (0,1)],
        [(0,3), (1,3), (2,3), (3,3), (3,2), (3,1), (3,0)]
    ]
    radius_test_results = [True, True, True]
    for r in range(len(radius_test_results)):
        method_retval = get_radial_square_locs(center=center, r=r)
        for i in range(len(method_retval)):
            assert method_retval[i] == radius_expected_vals[r][i]
                

def test_nearest_unoccupied_space():
    #TODO
    pass
