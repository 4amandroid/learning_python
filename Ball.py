import pygame
from Config import *
from pygame.sprite import Sprite
from pygame import Surface 
from random import choice

class Ball(Sprite):
    
    def __init__(self) -> None:
        super().__init__()
        self.x_speed = choice(BALL_X_SPEED)           
        self.y_speed = choice(BALL_Y_SPEED)          
        self.color = COLOR_RED
        self.ball_radius = BALL_RADIUS         
        self.image = Surface((self.ball_radius*2, self.ball_radius*2))
        self.image.set_colorkey(BACKGROUND_COLOR)
        pygame.draw.circle(self.image, self.color, (self.ball_radius,self.ball_radius), self.ball_radius)
        self.rect = self.image.get_rect()
        self.rect.center = (self.ball_radius, self.ball_radius)
        self.rect.y = STICK_Y_POSITION - self.ball_radius
        

    def update(self) -> None:
        self.rect.x += int(self.x_speed) #!!! coordinate += speed :) time-space continuum? :)
        self.rect.y += int(self.y_speed)  
        if self.rect.bottom >= SCREEN_HEIGHT or self.rect.top <= 0:
            self.y_speed *= -1 # will be removed
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.x_speed *= -1    
