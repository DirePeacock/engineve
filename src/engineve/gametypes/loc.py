class Loc():
    def __init__(self, *args, **kwagrs):
        if 1 == len(args) and isinstance(args[0], tuple):
            self._set_from_tuple(args[0])
        else:
            self.x = args[0]
            self.y = args[1]
            self.z = None if 2 == len(args) else args[2]
        # else:
        #     self._set_from_tuple((0,0))
    
    def _set_from_tuple(self, coord):
            self.x=coord[0]
            self.y=coord[1]
            self.z = None if 2 >= len(coord) else coord[2]
    
    def __getitem__(self, key):
        return self.coord[key]
        
    @property
    def coord(self):
        return tuple(val for val in [self.x, self.y, self.z] if val is not None)

    @coord.setter
    def coord(self, coord):
        self._set_from_tuple(coord)

    def __len__(self) -> int:
        return len([0 for attr in self.coord])

    def __str__(self) -> int:
        return self.coord.__str__()

