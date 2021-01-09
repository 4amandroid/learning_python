import pygame
from pygame.sprite import Sprite, Group
from pygame.time import Clock
from pygame.color import Color
from pygame import Surface

from Config import *
from Level import Level
 
FPS = 50

#define colors
WHITE = Color(255, 255, 255)
BACKGRAUND_COLOR = BLACK = Color(0, 0, 0)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
brick_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#brick_screen = pygame.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Game")
clock = Clock()
 

class Brick(Sprite):
    def __init__(self):
        super().__init__()
        self.image = Surface((BRICK_OFFSET_X, BRICK_OFFSET_Y))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
class Ball(Sprite):
    def __init__(self):
        super().__init__()
        self.x_speed = 2
        self.y_speed = 2
        self.color = RED
        #self.ball_x = self.ball_y = 100
        self.ball_radius = 5
        self.image = Surface((self.ball_radius*2, self.ball_radius*2))
        #self.image.fill(GREEN)
        self.image.set_colorkey(BACKGRAUND_COLOR)
        pygame.draw.circle(self.image, self.color, (self.ball_radius,self.ball_radius), self.ball_radius)
        self.rect = self.image.get_rect()
        self.rect.center = (self.ball_radius, self.ball_radius)
    def update(self) -> None:
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        if self.rect.bottom >= SCREEN_HEIGHT or self.rect.top <= 0:
            self.y_speed *= -1
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.x_speed *= -1    
        #pygame.sprite.spritecollide(all_balls,all_bricks,True)
        pass   
    
class Colission(Ball,Brick):
    def __init__(self):
        super().__init__()
    pass                
'''objs = [MyClass() for i in range(10)]
for obj in objs:
    other_object.add(obj)

objs[0].do_sth()'''     
level=Level()
level.load(0)
#print(level.brick_x)      
all_balls = Group()
ball = Ball()
all_balls.add(ball)
all_bricks = Group()
brick = [Brick() for i in range(level.brick_x.__len__())]
#brick = Brick()
for i in range(level.brick_x.__len__()):
    all_bricks.add(brick[i])
    brick[i].rect.x = level.brick_x[i]
    brick[i].rect.y = level.brick_y[i]
    

# Game loop
running = True
tolerance = 5 # ror test
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                brick[all_bricks.__len__()-1].kill()
                brick[all_bricks.__len__()-1].remove()
    for _brick in all_bricks:
        if ball.rect.colliderect(_brick.rect):
            
            if ball.rect.bottom - _brick.rect.top <= tolerance:
                ball.y_speed *= -1
            if ball.rect.top - _brick.rect.bottom <= tolerance:
                ball.y_speed *= -1    
            _brick.kill()   
            
    # Draw / render
    screen.fill(BLACK)
    all_bricks.draw(brick_screen)
    all_balls.draw(screen)
    all_balls.update()
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()