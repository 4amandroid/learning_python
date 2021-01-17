import pygame
from pygame.sprite import Sprite, Group
from pygame.time import Clock
from pygame.color import Color
from pygame import Surface

from Config import *
from Level import Level
 
FPS = 100

#define colors
WHITE = Color(255, 255, 255)
BACKGRAUND_COLOR = BLACK = Color(0, 0, 0)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
BRICK_IMAGE = ['brick.png','brick1.png','brick2.png','brick3.png']
BORDER_LOCATION = [(0,0),(SCREEN_WIDTH-20,0),(0,0)]

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
brick_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#brick_screen = pygame.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Game")
clock = Clock()
 
class Border(Sprite):
    def __init__(self): 
        super().__init__()
        self.image = Surface((20,SCREEN_WIDTH)) #TODO hardcore remove
        self.rect = self.image.get_rect()
        self.image.fill(GREEN)
        self.type_of_object = 'border'
        #self.rect.x = 0
        #self.rect.y = 0
        #self.right_border = Surface((5,SCREEN_HEIGHT))
        #self.right_border.fill(GREEN)
    pass
class Brick(Sprite):
    def __init__(self):
        super().__init__()
        self.brick_hardnes :int= 0
        self.image = Surface((BRICK_OFFSET_X, BRICK_OFFSET_Y))
        self.brick_image = pygame.image.load('brick.png')
        #self.image.blit(self.brick_image,(0,0))
        self.image.set_colorkey(BACKGRAUND_COLOR)
        
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.type_of_object = 'brick'
        #self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    def paint(self,brick_hardnes:int):
        self.brick_hardnes = brick_hardnes
        self.brick_image = pygame.image.load(BRICK_IMAGE[brick_hardnes-1])
        '''if self.brick_hardnes == 1:
            self.brick_image = pygame.image.load('brick.png')
        if self.brick_hardnes == 2:
            self.brick_image = pygame.image.load('brick1.png')    
        if self.brick_hardnes == 3:
            self.brick_image = pygame.image.load('brick2.png') 
        if self.brick_hardnes == 4:
            self.brick_image = pygame.image.load('brick3.png')'''    
        self.image.blit(self.brick_image,(0,0))      
        pass
    
    
class Ball(Sprite):
    
    def __init__(self):
        super().__init__()
        self.x_speed = 2
        self.y_speed = 2.3
        self.color = RED
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
        self.image.fill(GREEN)
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
 
class Colision_info():
    x: int = 0
    y: int = 0

    def __init__(self, x:int=0, y=0):
        self.x: int = x
        self.y: int = y
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
                print(_brick.type_of_object)    
                return _brick.rect
    def stick_detect(self):
        if self.ball.rect.colliderect(stick.rect):
            if abs(stick.rect.top - self.ball.rect.bottom) < self.tolerance and self.ball.y_speed > 0:
                    self.ball.y_speed *= -1
            if abs(stick.rect.bottom - self.ball.rect.top) < self.tolerance and self.ball.y_speed < 0:
                    self.ball.y_speed *= -1 
            if abs(stick.rect.right - self.ball.rect.left) < self.tolerance and self.ball.x_speed < 0:  
                    self.ball.x_speed *= -1   
            if abs(stick.rect.left - self.ball.rect.right) < self.tolerance and self.ball.x_speed > 0:  
                    self.ball.x_speed *= -1
    def border_detect(self):
        for _border in all_borders:
            if self.ball.rect.colliderect(_border.rect):
                if abs(_border.rect.top - self.ball.rect.bottom) < self.tolerance and self.ball.y_speed > 0:
                    self.ball.y_speed *= -1
                if abs(_border.rect.bottom - self.ball.rect.top) < self.tolerance and self.ball.y_speed < 0:
                    self.ball.y_speed *= -1 
                if abs(_border.rect.right - self.ball.rect.left) < self.tolerance and self.ball.x_speed < 0:  
                    self.ball.x_speed *= -1   
                if abs(_border.rect.left - self.ball.rect.right) < self.tolerance and self.ball.x_speed > 0:  
                    self.ball.x_speed *= -1
                print(_border.type_of_object)    
                
    pass                
class BaseGameObject():
    pass
class Game():
    def __init__(self):
        #self.current_level = 0
        self.level = Level()
        
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
    
    
    pass    
game = Game()
game.load_next_level()
#level=Level()
#game.level.load(0)
#print(level.brick_x)     
ball_colision = BallColision() 
border = Border()
border = [Border() for i in range(BORDER_LOCATION.__len__())]
all_borders = Group()

border[2].image =Surface((SCREEN_WIDTH,35))
border[2].rect = border[2].image.get_rect()
#border[2].rect.topleft = (100,100)
border[2].image.fill(GREEN)
for i in range(BORDER_LOCATION.__len__()):
    all_borders.add(border[i])
    border[i].rect.topleft = BORDER_LOCATION[i]
    
    
    #border[i].rect.topleft= BORDER_LOCATION[i]
    #brick[i].rect.y = game.level.brick_y[i]
#all_borders.add(border)
#all_balls = Group()
#ball = Ball()
#all_balls.add(ball)
#all_bricks = Group()
#brick = [Brick() for i in range(game.level.brick_x.__len__())]
#brick = Brick()
'''for i in range(game.level.brick_x.__len__()):
    all_bricks.add(brick[i])
    brick[i].rect.x = game.level.brick_x[i]
    brick[i].rect.y = game.level.brick_y[i]'''
    
stick = Stick()
all_borders.add(stick)
#all_sticks=Group()
#all_sticks.add(stick)

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
    
  
        
    #ball_colision.stick_detect()    
    ball_colision.border_detect()     
    
     
            
    # Draw / render
    screen.fill(BLACK)
    game.all_bricks.draw(brick_screen)
    ball_colision.all_balls.draw(screen)
    all_borders.draw(screen)
    all_borders.update()
    #border.left_border.blit(screen,(0,0))
    #border.left_border.update()
    ball_colision.all_balls.update()
    #all_sticks.draw(screen)
    #all_sticks.update()
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()