import pygame
from Config import *
import random
from Level import Level
from BaseGameObject import BaseGameObject
 
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
 

class Brick(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((BRICK_OFFSET_X, BRICK_OFFSET_Y))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        #print(self.level.brick_x)
    def update(self):
        self.rect.x += 5
        if self.rect.left > WIDTH:
            self.rect.right = 0
            
'''objs = [MyClass() for i in range(10)]
for obj in objs:
    other_object.add(obj)

objs[0].do_sth()'''     
level=Level()
level.load(0)
print(level.brick_x)      
all_bricks = pygame.sprite.Group()
brick = [Brick() for i in range(level.brick_x.__len__())]
#brick = Brick()
for i in range(level.brick_x.__len__()):
    all_bricks.add(brick[i])
    brick[i].rect.x = level.brick_x[i]
    brick[i].rect.y = level.brick_y[i]
# Game loop
running = True
p=0
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
                brick[p].kill()
                p +=1 

    # Update
    all_bricks.update()
    # Draw / render
    screen.fill(BLACK)
    all_bricks.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()