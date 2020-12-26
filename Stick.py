from Config import *
from Coordinate import Coordinate
import pygame


class Stick:
    
    def move(self, screen: pygame.Surface):
        stick_position = Coordinate()
        # remove hardcoded position
        stick_position.x = pygame.mouse.get_pos()[0]
        if stick_position.x > (RIGHT_WALL_X - STICK_LENGHT):
            stick_position.x = (RIGHT_WALL_X - STICK_LENGHT)
        screen.blit(pygame.image.load(POPCORN_GREEN_BAR_PNG), (stick_position.x, STICK_Y_POSITION))
        return stick_position.x
    pass       
