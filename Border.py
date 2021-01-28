from Config import *
from pygame.sprite import Sprite
from pygame import Surface 

class Border(Sprite):
    def __init__(self) -> None: 
        super().__init__()
        self.image = Surface((SIDE_BORDER_WIDTH, SCREEN_WIDTH))  
        self.rect = self.image.get_rect()
        self.image.fill(COLOR_GREEN)