import pygame
from pygame.sprite import Sprite, Group
from pygame.time import Clock
from pygame.color import Color
from pygame import Surface

from Config import *
from Level import Level
 
FPS = 100

#define colors
 
BACKGRAUND_COLOR = COLOR_BLACK #= Color(0, 0, 0)
BRICK_IMAGE = ['brick.png','brick1.png','brick2.png','brick3.png']
BORDER_LOCATION = [(0,0),(SCREEN_WIDTH-20,0),(0,0)]

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
brick_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
 
pygame.display.set_caption("My Game")
clock = Clock()
 
class Border(Sprite):
    def __init__(self): 
        super().__init__()
        self.image = Surface((20,SCREEN_WIDTH)) #TODO hardcore remove
        self.rect = self.image.get_rect()
        self.image.fill(COLOR_GREEN)
        self.type_of_object = 'border'
         
    pass
class Brick(Sprite):
    def __init__(self):
        super().__init__()
        self.brick_hardnes :int= 0
        self.image = Surface((BRICK_OFFSET_X, BRICK_OFFSET_Y))
        self.brick_image = pygame.image.load('brick.png')
        self.image.set_colorkey(BACKGRAUND_COLOR)
        self.rect = self.image.get_rect()
        self.type_of_object = 'brick'
    def paint(self,brick_hardnes:int):
        self.brick_hardnes = brick_hardnes
        self.brick_image = pygame.image.load(BRICK_IMAGE[brick_hardnes-1])
        self.image.blit(self.brick_image,(0,0))      
        pass
    
    
class Ball(Sprite):
    
    def __init__(self):
        super().__init__()
        self.x_speed = 2
        self.y_speed = 2.3
        self.color = COLOR_RED
        self.ball_radius = 5
        self.image = Surface((self.ball_radius*2, self.ball_radius*2))
        self.image.set_colorkey(BACKGRAUND_COLOR)
        
        pygame.draw.circle(self.image, self.color, (self.ball_radius,self.ball_radius), self.ball_radius)
        self.rect = self.image.get_rect()
        self.rect.center = (self.ball_radius, self.ball_radius)
        self.rect.y = 550 
    def update(self) -> None:
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        if self.rect.bottom >= SCREEN_HEIGHT or self.rect.top <= 0:
            self.y_speed *= -1
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.x_speed *= -1    
        #pygame.sprite.spritecollide(ball,all_bricks,True)
        pass

class Stick(Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = Surface((107, 22))
        #self.image.fill(GREEN)
        self.stick_image = pygame.image.load(STICK_TEXTURE)
        self.image.blit(self.stick_image,(0,0))
        self.image.set_colorkey(BACKGRAUND_COLOR)
        self.rect = self.image.get_rect()
        self.type_of_object = 'stick' 
        
    def update(self):
        self.rect.x = pygame.mouse.get_pos()[0]
        self.rect.y = STICK_Y_POSITION
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH #- STICK_LENGHT
         
    pass             
 
 
class BallColision():
    def __init__(self):
        self.all_balls = Group()
        self.ball = Ball()
        self.all_balls.add(self.ball)
        self.tolerance = 5
      
    def brick_detect(self):    
        for _brick in game.all_bricks:
            if self.ball.rect.colliderect(_brick.rect):
                
                if abs(_brick.rect.top - self.ball.rect.bottom) < self.tolerance and self.ball.y_speed > 0:
                    self.ball.y_speed *= -1
                if abs(_brick.rect.bottom - self.ball.rect.top) < self.tolerance and self.ball.y_speed < 0:
                    self.ball.y_speed *= -1 
                if abs(_brick.rect.right - self.ball.rect.left) < self.tolerance and self.ball.x_speed < 0:  
                    self.ball.x_speed *= -1   
                if abs(_brick.rect.left - self.ball.rect.right) < self.tolerance and self.ball.x_speed > 0:  
                    self.ball.x_speed *= -1
                if _brick.type_of_object == 'brick':
                    if _brick.brick_hardnes == 1:    
                        _brick.kill() 
                    if _brick.brick_hardnes > 1 and _brick.brick_hardnes < 4:
                        _brick.brick_hardnes -= 1
                        _brick.paint(_brick.brick_hardnes) 
                    print(_brick.brick_hardnes)
                    print(len(game.all_bricks))
                 
                if len(game.all_bricks) == 65:
                    game.level.current_level += 1
                    game.load_next_level() 
                    game.load_all_visual_object()
                print(_brick.type_of_object)    
                return _brick.rect
    
                
    pass                
class BaseGameObject():
    pass
class Game():
    def __init__(self):
        #self.current_level = 0
        self.level = Level()
        self.border = Border()
        self.border = [Border() for i in range(BORDER_LOCATION.__len__())]
        self.border[2].image =Surface((SCREEN_WIDTH,35))
        self.border[2].rect = self.border[2].image.get_rect()
        self.border[2].image.fill(COLOR_GREEN)
        self.all_borders = Group()
        self.stick = Stick()
        self.all_sticks = Group()
        self.all_sticks.add(self.stick)
        for i in range(BORDER_LOCATION.__len__()):
            self.all_borders.add(self.border[i])
            self.border[i].rect.topleft = BORDER_LOCATION[i]
    def load_next_level(self):   
        self.level.load(self.level.current_level)
        self.all_bricks = Group()
    
        self.brick = [Brick() for i in range(self.level.brick_x.__len__())]
        for i in range(self.level.brick_x.__len__()):
            self.all_bricks.add(self.brick[i])
            self.brick[i].rect.x = self.level.brick_x[i]
            self.brick[i].rect.y = self.level.brick_y[i]
            self.brick[i].brick_hardnes = self.level.brick_break[i]
            self.brick[i].paint(self.brick[i].brick_hardnes)
        pass    
    def load_all_visual_object(self):
        for _border in self.all_borders:
            self.all_bricks.add(_border)
        self.all_bricks.add(self.stick)
        pass
    
    pass    
game = Game()
game.load_next_level()
game.load_all_visual_object()
  
ball_colision = BallColision() 
  
    
 

# Game loop
running = True
 
while running:
     
    clock.tick(FPS)
     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                game.brick[game.all_bricks.__len__()-1].kill()
                game.brick[game.all_bricks.__len__()-1].remove()
        
    ball_colision.brick_detect()        
    # Draw / render
    screen.fill(COLOR_BLACK)
    game.all_bricks.draw(brick_screen)
    ball_colision.all_balls.draw(screen)
    game.all_borders.update()
    ball_colision.all_balls.update()
    game.all_sticks.update()
    pygame.display.flip()

pygame.quit()