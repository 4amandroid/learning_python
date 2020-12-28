from Coordinate import Coordinate
from Level import Level

class CoordinateOf:
    brick = 0
    stick = 1

class BaseGameObject:

    coordinates = [len([a for a in dir(CoordinateOf) if not a.startswith('__') and not callable(getattr(CoordinateOf, a))])]
    coordinateOf = CoordinateOf()

    def __init__(self):
        self.coordinates = [Coordinate() for i in range(len([a for a in dir(CoordinateOf) if not a.startswith('__') and not callable(getattr(CoordinateOf, a))]))]
            
        self.coordinateOf = CoordinateOf()
        self.level = Level()
        self.level.load(self.level.current_level)
        self.coordinates[self.coordinateOf.brick]
    pass
