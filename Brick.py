import pygame
from Config import *
from BaseGameObject import BaseGameObject
from Coordinate import Coordinate

class Brick_Offset():
    x: int = 0
    y: int = 0
    
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

class Brick(BaseGameObject):

    def __init__(self):
        self.offset = Brick_Offset(BRICK_OFFSET_X, BRICK_OFFSET_Y)
        
        
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
        
        color_brick = COLOR_LIGHT_GREEN
        for i in range(self.level.brick_x.__len__()):
            self.coordinates[self.descriminator.brick].x = self.level.brick_x[i]
            self.coordinates[self.descriminator.brick].y = self.level.brick_y[i]
            brick_break = self.level.brick_break[i]
            if brick_break == 1 or brick_break == 2:
                color_brick = COLOR_LIGHT_GREEN
            elif brick_break == 3 or brick_break == 4:
                color_brick = COLOR_GREEN
            elif brick_break == 5 or brick_break == 6:
                color_brick = COLOR_DARK_GREEN
            elif brick_break == 7:
                color_brick = COLOR_WHITE
            # remove using pygame drawing here
            pygame.draw.rect(screen, color_brick,
                             (self.coordinates[self.descriminator.brick].x, self.coordinates[self.descriminator.brick].y, self.offset.x, self.offset.y))
        return True
