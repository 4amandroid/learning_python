from typing import Tuple, List, Any
import pygame
from Config import  BORDER_LOCATION, UP_BORDER_NUMBER, SCREEN_WIDTH, UP_BORDER_HEIGHT, \
    COLOR_RED,COLOR_GREEN, SIDE_BORDER_WIDTH
from pygame.sprite import Sprite
from pygame import Surface
from Coordinate import Coordinate
from Brick import Brick
from pygame.sprite import Sprite, Group
 

class BaseGameObject(Sprite):
    def __init__(self) -> None: 
        super().__init__()
        self.image = Surface((SIDE_BORDER_WIDTH, SCREEN_WIDTH))  
        self.rect = self.image.get_rect()
        self.image.fill(COLOR_GREEN)        
class Border(BaseGameObject):
    def __init__(self) -> None:
        super().__init__()
        #self.border = Border()
        #self.__initializeBorderFrame()

    def initializeBorderFrame(self) -> None:
        self.border = [Border() for i in range(BORDER_LOCATION.__len__())]
        self.border[UP_BORDER_NUMBER].image = Surface((SCREEN_WIDTH, UP_BORDER_HEIGHT))                        
        self.border[UP_BORDER_NUMBER].rect = self.border[UP_BORDER_NUMBER].image.get_rect()
        self.border[UP_BORDER_NUMBER].image.fill(COLOR_RED)  
        self.all_borders = Group()
        border_location = Coordinate()    
        for i in range(BORDER_LOCATION.__len__()):
            self.all_borders.add(self.border[i])
            border_location.x , border_location.y = BORDER_LOCATION[i] 
            self.border[i].rect.topleft = (border_location.x , border_location.y) 
        self.all_borders.add(self.border)


    