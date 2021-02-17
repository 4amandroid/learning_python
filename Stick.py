import pygame
from Config import BULLET_WIDTH, BULLET_HEIGHT, BULLET_TEXTURE, TOP_LEFT_SURFACE, BACKGROUND_COLOR, STICK_Y_POSITION, \
                    STICK_LENGTH, STICK_HEIGHT, STICK_TEXTURE, SCREEN_WIDTH, SIDE_BORDER_WIDTH
from pygame.sprite import Sprite
from pygame import Surface 
from Coordinate import Coordinate
from random import choice
from pygame.sprite import Sprite, Group

class BaseStick(Sprite):
    def __init__(self, sprite_width = BULLET_WIDTH, sprite_height = BULLET_HEIGHT, sprite_texture = BULLET_TEXTURE,\
                        sprite_top_surface = TOP_LEFT_SURFACE, bg_color = BACKGROUND_COLOR) -> None:
        super().__init__()
        self.image = Surface((sprite_width, sprite_height))   
        self.luck_image = pygame.image.load(sprite_texture)
        self.image.blit(self.luck_image, sprite_top_surface)
        self.image.set_colorkey(bg_color)
        self.rect = self.image.get_rect()

class Luck(BaseStick):
    def __init__(self, midtop, sprite_top_surface = TOP_LEFT_SURFACE) -> None:
        super().__init__()
        luck_images=('./images/luck1.png','./images/luck2.png','./images/luck3.png','./images/luck4.png')
        self.luck_image = pygame.image.load(choice(luck_images))
        self.image.blit(self.luck_image, sprite_top_surface)
        self.rect.midtop = midtop
        
    def update(self) -> None:
        self.rect.y += 1 
        
class Bullet(BaseStick):
    def __init__(self, x_offset) -> None:
        super().__init__()
        self.rect.y = STICK_Y_POSITION
        self.bullet_position = Coordinate(x_offset  , pygame.mouse.get_pos()[1])
        
    def update(self) -> None:
        self.rect.x = self.bullet_position.x
        self.rect.y -=1
        
        
class Stick(BaseStick):
    def __init__(self, screen) -> None:
        super().__init__(STICK_LENGTH, STICK_HEIGHT, STICK_TEXTURE, TOP_LEFT_SURFACE, BACKGROUND_COLOR)
        self.bullets = Group() 
        self.screen = screen
 
    def update(self) -> None:
        stick_position = Coordinate(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        self.rect.x = stick_position.x
        self.rect.y = STICK_Y_POSITION
        if self.rect.right >= SCREEN_WIDTH - SIDE_BORDER_WIDTH:
            self.rect.right = SCREEN_WIDTH - SIDE_BORDER_WIDTH
        elif self.rect.left <= SIDE_BORDER_WIDTH:
            self.rect.left = SIDE_BORDER_WIDTH
        #for bullet in self.bullets:
        self.bullets.update()
        self.bullets.draw(self.screen)
            
    def shot(self) -> Bullet:
        bullet = Bullet(self.rect.x)
        self.bullets.add(bullet)
        bullet = Bullet(self.rect.x+STICK_LENGTH-BULLET_WIDTH)
        self.bullets.add(bullet)
        return bullet