from typing import Tuple, List, Any
import pygame
from Config import BULLET_WIDTH, BULLET_HEIGHT, BULLET_TEXTURE, TOP_LEFT_SURFACE, BACKGROUND_COLOR, STICK_Y_POSITION, \
    STICK_LENGTH, STICK_HEIGHT, STICK_TEXTURE, SCREEN_WIDTH, SIDE_BORDER_WIDTH, UP_BORDER_HEIGHT, \
    SCREEN_HEIGHT, CHANCE_FOR_LUCK, STICK_CORRECTION, LUCK_IMAGES, STICK_IMAGES
from pygame.sprite import Sprite
from pygame import Surface
from Coordinate import Coordinate
from Brick import Brick
from random import randint
from pygame.sprite import Sprite, Group


class BaseStick(Sprite):
    """
    BaseStick class for stick related objects, derived from Sprite.
    Initialize the surface.
        self.shoot = False
        self.glue = False
    Args:
        BaseStick ([Abstract]): abstact class
    """
    def __init__(self, sprite_width: int = BULLET_WIDTH, sprite_height: int = BULLET_HEIGHT, sprite_texture: str = BULLET_TEXTURE,
                 sprite_top_surface: Tuple[int, int] = TOP_LEFT_SURFACE, bg_color: Tuple[int, int, int] = BACKGROUND_COLOR) -> None:
        super().__init__()
        
        self.image = Surface((sprite_width, sprite_height))
        self.luck_image = pygame.image.load(sprite_texture)
        self.image.blit(self.luck_image, sprite_top_surface)
        self.image.set_colorkey(bg_color)
        self.rect = self.image.get_rect() # type: ignore
        self.shoot = False
        self.glue = False
        self.longbar = False
        self.shortbar = False
        
class Luck(BaseStick):
    """
    Luck - helper for raining lucks

    Args:
        BaseStick ([StickTextureInfo]): [derived from BaseStick]
    """
    def __init__(self, midtop: Tuple[int, int] = (0, 0), sprite_top_surface: Tuple[int, int] = TOP_LEFT_SURFACE) -> None:
        super().__init__()
        self.images = LUCK_IMAGES
        self.number = randint(0,CHANCE_FOR_LUCK)
        if self.number in range(len(self.images)):
            self.luck_image = pygame.image.load(self.images[self.number])
            self.image.blit(self.luck_image, sprite_top_surface)
            self.rect.midtop = midtop
     
    def luckCollideDetect(self, stick, lucks: List[Any]) -> None:  # TO DO change name
        self.images = STICK_IMAGES
        def initChangedStick(stick: Stick, stick_image = STICK_TEXTURE):
            stick_length = STICK_LENGTH
            if stick.longbar:
                stick_length = STICK_LENGTH + STICK_CORRECTION
            elif stick.shortbar:
                stick_length = STICK_LENGTH - STICK_CORRECTION
                
            stick.image = Surface((stick_length,STICK_HEIGHT))
            stick.luck_image = pygame.image.load(stick_image)
            stick.image.blit(stick.luck_image, TOP_LEFT_SURFACE)
            stick.rect = stick.image.get_rect()
            
            
        def resetLucks(stick, luck, luck_number):
            stick_lucks=[False] * len(self.images)
            stick_lucks[luck_number] = True
            stick.shoot, stick.glue, stick.longbar, stick.shortbar = stick_lucks
        for luck in lucks:
            if luck.rect.colliderect(stick.rect):
                if luck.number in range(len(self.images)):
                    resetLucks(stick, luck, luck.number)
                    initChangedStick(stick, self.images[luck.number])
                luck.kill()
            elif luck.rect.bottom > SCREEN_HEIGHT:
                luck.kill()
    
    def update(self) -> None:
        self.rect.y += 1


class Bullet(BaseStick):
    """Feature of stick - responsible for shooting behavior

    Args:
        BaseStick ([x_offset]): int [bullet start position according to stick]
    """
    def __init__(self, x_offset: int = 0 ) -> None:
        super().__init__()
        self.rect.y = STICK_Y_POSITION
        self.bullet_position = Coordinate(x_offset, pygame.mouse.get_pos()[1])

    def bulletCollideDetect(self, bricks: List[Brick], bullets: List[Any]):
        """Action when bullet is collide to brick

        Args:
            bricks (List[Brick])
            bullets (List[Any])
        """
        for bullet in bullets:
            for brick in bricks:
                if bullet.rect.colliderect(brick.rect):
                    bullet.kill()
                    if brick.brick_hardness < 4:
                        brick.kill()
                elif bullet.rect.y < UP_BORDER_HEIGHT:
                    bullet.kill()

    def update(self) -> None:
        self.rect.x = self.bullet_position.x
        self.rect.y -= 1


class Stick(BaseStick):
    """
    Stick object. General player controlled object.
    """
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(STICK_LENGTH, 
                         STICK_HEIGHT,
                         STICK_TEXTURE, 
                         TOP_LEFT_SURFACE, 
                         BACKGROUND_COLOR)
        #self.bullet = Bullet()
        self.bullets = Group()
        self.screen = screen
     
    
    def update(self) -> None: # type: ignore
        self.stick_position = Coordinate(coordinates = pygame.mouse.get_pos())
        self.rect.x = self.stick_position.x
        self.rect.y = STICK_Y_POSITION
        if self.rect.right >= SCREEN_WIDTH - SIDE_BORDER_WIDTH:
            self.rect.right = SCREEN_WIDTH - SIDE_BORDER_WIDTH
        elif self.rect.left <= SIDE_BORDER_WIDTH:
            self.rect.left = SIDE_BORDER_WIDTH
        # for bullet in self.bullets:
        self.bullets.update()
        self.bullets.draw(self.screen)
      
    
    def shot(self) -> Bullet:
        
        self.bullet = Bullet(self.rect.x)
        self.bullets.add(self.bullet)
        self.bullet = Bullet(self.rect.x+STICK_LENGTH-BULLET_WIDTH)
        self.bullets.add(self.bullet)
        return self.bullet
