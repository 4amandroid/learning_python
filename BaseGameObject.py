from Coordinate import Coordinate
from Level import Level

class Base_discriminator:
    brick = 0
    stick = 1

class BaseGameObject:

    coordinates = [10]
    descriminator = Base_discriminator()

    def __init__(self):
        self.coordinates = [Coordinate() for i in range(10)]
            
        self.descriminator = Base_discriminator()
        self.level = Level()
        self.level.load(self.level.current_level)
        self.coordinates[self.descriminator.brick]
    pass
