import pygame
from Config import *
from pygame.sprite import Sprite
from pygame import Surface 
from Coordinate import Coordinate 


class Stick(Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.image = Surface((STICK_LENGTH, STICK_HEIGHT))   
        self.stick_image = pygame.image.load(STICK_TEXTURE)
        self.image.blit(self.stick_image,TOP_LEFT_SURFACE)
        self.image.set_colorkey(BACKGROUND_COLOR)
        self.rect = self.image.get_rect()
 
    def update(self) -> None:
        stick_position = Coordinate()
        stick_position.x = pygame.mouse.get_pos()[0] 
        self.rect.x = stick_position.x    #!!! mouse should return coordinate object: Coordinate(pygame.mouse.get_pos()).x
        self.rect.y = STICK_Y_POSITION
        if self.rect.right >= SCREEN_WIDTH - SIDE_BORDER_WIDTH:
            self.rect.right = SCREEN_WIDTH - SIDE_BORDER_WIDTH
        elif self.rect.left <= SIDE_BORDER_WIDTH:
            self.rect.left = SIDE_BORDER_WIDTH  