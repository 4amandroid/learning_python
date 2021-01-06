import pygame
from pygame.sprite import Sprite, Group
from pygame.time import Clock
from pygame.color import Color
from pygame import Surface

from Config import *
from Level import Level
 
FPS = 30

#define colors
WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Game")
clock = Clock()
 

class Brick(Sprite):
    def __init__(self):
        super().__init__()
        self.image = Surface((BRICK_OFFSET_X, BRICK_OFFSET_Y))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
            
'''objs = [MyClass() for i in range(10)]
for obj in objs:
    other_object.add(obj)

objs[0].do_sth()'''     
level=Level()
level.load(0)
print(level.brick_x)      
all_bricks = Group()
brick = [Brick() for i in range(level.brick_x.__len__())]
#brick = Brick()
for i in range(level.brick_x.__len__()):
    all_bricks.add(brick[i])
    brick[i].rect.x = level.brick_x[i]
    brick[i].rect.y = level.brick_y[i]
# Game loop
running = True

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

    # Draw / render
    screen.fill(BLACK)
    all_bricks.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()