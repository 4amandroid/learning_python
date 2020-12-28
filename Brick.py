import pygame
from Config import *
from BaseGameObject import BaseGameObject
from Coordinate import Coordinate
from BrickOffset import *


class Brick(BaseGameObject):

    def __init__(self):
        super().__init__()
        self.offset = BrickOffset(BRICK_OFFSET_X, BRICK_OFFSET_Y)
        self.brick_color = {COLOR_LIGHT_GREEN : [0, 1, 2], 
                            COLOR_GREEN: [3, 4], 
                            COLOR_DARK_GREEN: [5, 6], 
                            COLOR_WHITE: [7]}
 
    def remove(self):
        self.level.brick_x.pop(0)
        self.level.brick_y.pop(0)
        self.level.brick_break.pop(0)
        number_of_bricks = len(self.level.brick_x)
        if number_of_bricks == 100: #replace with number_of_brick-unbreakable_brick
            self.level.current_level += 1
            self.level.load(self.level.current_level)
            self.level.levels.pop(0)
            self.level.save()
        return number_of_bricks
        
    def draw(self, screen: pygame.Surface, pygame: pygame):
        for i in range(self.level.brick_x.__len__()):
            self.coordinates[self.coordinateOf.brick] = Coordinate(self.level.brick_x[i], self.level.brick_y[i])
            brick_break = {value:key for key in self.brick_color for value in self.brick_color[key]}
            
            # remove using pygame drawing here
            pygame.draw.rect(screen, 
                             brick_break[self.level.brick_break[i]],
                             (self.coordinates[self.coordinateOf.brick].x, 
                              self.coordinates[self.coordinateOf.brick].y, 
                              self.offset.x, self.offset.y))
        return True
