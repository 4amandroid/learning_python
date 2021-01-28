import pygame
from Config import *
from pygame.sprite import Sprite
from pygame import Surface 

class Brick(Sprite):
    
    def __init__(self):
        super().__init__()
        self.brick_hardness :int= 0
        self.image = Surface((BRICK_OFFSET_X, BRICK_OFFSET_Y))
        self.image.set_colorkey(BACKGROUND_COLOR)   
        self.rect = self.image.get_rect()     
              
    def paint(self,brick_hardness:int) -> None:               
        self.brick_hardness = brick_hardness           
        self.brick_image = pygame.image.load(BRICK_IMAGE[brick_hardness-1])
        self.image.blit(self.brick_image,TOP_LEFT_SURFACE)   