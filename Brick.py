import pygame
from Config import *
from BaseGameObject import BaseGameObject
from Coordinate import Coordinate

class Brick_offset():
    x: int = 0
    y: int = 0

class Brick(BaseGameObject):
    
    def __init__(self):
        self.offset_x = BRICK_OFFSET_X
        self.offset_y = BRICK_OFFSET_Y
        
        super().__init__()
 
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
        
        color_brick = LIGHT_GREEN
        for i in range(self.level.brick_x.__len__()):
            self.coordinates[self.descriminator.brick].x = self.level.brick_x[i]
            self.coordinates[self.descriminator.brick].y = self.level.brick_y[i]
            _p = self.level.brick_break[i]
            if _p == 1 or _p == 2:
                color_brick = LIGHT_GREEN
            elif _p == 3 or _p == 4:
                color_brick = GREEN
            elif _p == 5 or _p == 6:
                color_brick = DARK_GREEN
            elif _p == 7:
                color_brick = WHITE
            # remove using pygame drawing here
            pygame.draw.rect(screen, color_brick,
                             (self.coordinates[self.descriminator.brick].x, self.coordinates[self.descriminator.brick].y, self.offset_x, self.offset_y))
        return True
