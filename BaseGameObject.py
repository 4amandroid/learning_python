from typing import Tuple, List, Any
import pygame
from Config import *
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
        self.image.set_colorkey(BACKGROUND_COLOR)
class Ball(BaseGameObject):
    
    def __init__(self) -> None:
        super().__init__()
        self.x_speed =  BALL_X_SPEED
        self.y_speed =  BALL_Y_SPEED
        self.color = COLOR_RED
        self.ball_radius = BALL_RADIUS         
        self.image = Surface((self.ball_radius*2, self.ball_radius*2))
        #self.image.set_colorkey(BACKGROUND_COLOR)
        pygame.draw.circle(self.image, self.color, (self.ball_radius,self.ball_radius), self.ball_radius)
        self.rect = self.image.get_rect()
        self.rect.center = (self.ball_radius, self.ball_radius)
        self.rect.y = STICK_Y_POSITION - self.ball_radius
        self.rect.x = SCREEN_WIDTH//2
        self.glued = False
        self.glueXPos = 0
        self.x_correction = 0
        self.correct_glue_direction = 1
    def update(self, x) -> None:
        if self.glued:
            self.rect.x = x + self.x_correction
        else:
            self.rect.x += int(self.x_speed) #!!! coordinate += speed :) time-space continuum? :)
            self.rect.y += int(self.y_speed)  
        
        if self.rect.top <= 0:
            self.y_speed *= -1  
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.x_speed *= -1
        # TODO debug when colision bug ball to border
        if self.rect.top <= UP_BORDER_HEIGHT - COLISION_TOLERANCE:
            print("collision bug")
            self.y_speed *= -1  
        if self.rect.left <= SIDE_BORDER_WIDTH - COLISION_TOLERANCE or self.rect.right >= SCREEN_WIDTH-SIDE_BORDER_WIDTH+COLISION_TOLERANCE: 
            self.x_speed *= -1
            print("collision bug") 
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


    