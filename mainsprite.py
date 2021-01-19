import pygame
from pygame.sprite import Sprite, Group
from pygame.time import Clock
from pygame.color import Color
from pygame import Surface

from Config import *
from Level import Level
 
FPS = 100

#define colors
 
BACKGROUND_COLOR = COLOR_BLACK #= Color(0, 0, 0)                        #!!! one color = another color ?
BRICK_IMAGE = ['brick.png','brick1.png','brick2.png','brick3.png']      #!!! use function to load names e.g. brick+level+.png
BORDER_LOCATION = [(0,0),(SCREEN_WIDTH-20,0),(0,0)]                     #!!! remove magic numbers

# initialize pygame and create window
#!!! above should be only in game constructor (__init__)
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
        self.type_of_object = 'border' #!!! always use build in functions to do this: type(self).__name__
         
    pass
class Brick(Sprite):
    def __init__(self):
        super().__init__()
        self.brick_hardnes :int= 0
        self.image = Surface((BRICK_OFFSET_X, BRICK_OFFSET_Y))
        self.brick_image = pygame.image.load('brick.png')
        self.image.set_colorkey(BACKGROUND_COLOR)   #!!! typo - streetsidesoftware.code-spell-checker
        self.rect = self.image.get_rect()           
        self.type_of_object = 'brick'               #!!! always use build in functions to do this: type(self).__name__
    def paint(self,brick_hardnes:int):              #!!! typo - streetsidesoftware.code-spell-checker
        self.brick_hardnes = brick_hardnes          #!!! typo - streetsidesoftware.code-spell-checker
        self.brick_image = pygame.image.load(BRICK_IMAGE[brick_hardnes-1])
        self.image.blit(self.brick_image,(0,0))      
        pass
    
    
class Ball(Sprite):
    
    def __init__(self):
        super().__init__()
        self.x_speed = 2            #!!! avoid magic numbers
        self.y_speed = 2.3          #!!! avoid magic numbers
        self.color = COLOR_RED
        self.ball_radius = 5        #!!! avoid magic numbers
        self.image = Surface((self.ball_radius*2, self.ball_radius*2))
        self.image.set_colorkey(BACKGROUND_COLOR)
        
        pygame.draw.circle(self.image, self.color, (self.ball_radius,self.ball_radius), self.ball_radius)
        self.rect = self.image.get_rect()
        self.rect.center = (self.ball_radius, self.ball_radius)
        self.rect.y = 550           #!!! avoid magic numbers
    def update(self) -> None:
        self.rect.x += self.x_speed #!!! coordinate += speed :) time-space continuum? :)
        self.rect.y += self.y_speed #!!! very strange hack - rect coordinates are integer but it is assigned from speed float(2.3) :)
        if self.rect.bottom >= SCREEN_HEIGHT or self.rect.top <= 0:
            self.y_speed *= -1 # will be removed
        #if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
        #    self.x_speed *= -1    
         
        pass                        #!!! method definition is declared as return None but pass? should be return None instead

class Stick(Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = Surface((107, 22))             #!!! avoid magic numbers
        self.stick_image = pygame.image.load(STICK_TEXTURE)
        self.image.blit(self.stick_image,(0,0))
        self.image.set_colorkey(BACKGROUND_COLOR)
        self.rect = self.image.get_rect()
        self.type_of_object = 'stick'               #!!! always use build in functions to do this: type(self).__name__
        
    def update(self):
        self.rect.x = pygame.mouse.get_pos()[0]     #!!! mouse should return coordinate object: Coordinate(pygame.mouse.get_pos()).x
        self.rect.y = STICK_Y_POSITION
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH #- STICK_LENGHT
         
    pass                                            #!!! make some research when is correct to return None and when to pass.
                                                    #!!! this should be identical at all
 
 
class BallColision():
    def __init__(self):
        self.all_balls = Group()
        self.ball = Ball()
        self.all_balls.add(self.ball)               #!!! is this be always one object of ball? 
        self.tolerance = 4
      
    def detect(self):    
        for visual_object in game.all_visual_objects:   #!!! unacceptable! game is no place here
            if self.ball.rect.colliderect(visual_object.rect):
                #!!! extract ifs as separate method for now
                if abs( visual_object.rect.top - self.ball.rect.bottom) < self.tolerance and self.ball.y_speed > 0:
                    self.ball.y_speed *= -1
                if abs( visual_object.rect.bottom - self.ball.rect.top) < self.tolerance and self.ball.y_speed < 0:
                    self.ball.y_speed *= -1 
                if abs(visual_object.rect.right - self.ball.rect.left) < self.tolerance and self.ball.x_speed < 0:  
                    self.ball.x_speed *= -1   
                if abs(visual_object.rect.left - self.ball.rect.right) < self.tolerance and self.ball.x_speed > 0:  
                    self.ball.x_speed *= -1
                if visual_object.type_of_object == 'brick': #!!! always use build in functions to do this: type(self).__name__
                    if visual_object.brick_hardnes == 1:    
                        visual_object.kill() 
                    if visual_object.brick_hardnes > 1 and visual_object.brick_hardnes < 4: #!!! if 1 <= visual_object.brick_hardnes <= 4:
                        visual_object.brick_hardnes -= 1
                        visual_object.paint(visual_object.brick_hardnes) 
                    print(visual_object.brick_hardnes)
                    print(len(game.all_bricks))
                 
                if len(game.all_visual_objects) == 15:      #!!! avoid magic numbers
                    game.level.current_level += 1           #!!! unacceptable! game and level logic is no place here
                    game.load_next_level() 
                    game.load_all_visual_object()
                print(visual_object.type_of_object)    
                return visual_object.rect
    
                
    pass                
class BaseGameObject():
    pass
class Game():
    def __init__(self):
        #self.current_level = 0
        self.level = Level()
        self.border = Border()
        self.border = [Border() for i in range(BORDER_LOCATION.__len__())]
        self.border[2].image =Surface((SCREEN_WIDTH,35))                        #!!! avoid magic numbers
        self.border[2].rect = self.border[2].image.get_rect()#TODO tthink something else
        self.border[2].image.fill(COLOR_GREEN)                                  #!!! avoid magic numbers
        self.all_borders = Group()                                              #!!! avoid magic numbers
        self.stick = Stick()
        self.all_sticks = Group()
        self.all_sticks.add(self.stick)
        for i in range(BORDER_LOCATION.__len__()):
            self.all_borders.add(self.border[i])
            self.border[i].rect.topleft = BORDER_LOCATION[i]
        self.all_visual_objects = Group() 
        self.all_visual_objects.add(self.all_sticks)   
        self.all_visual_objects.add(self.all_borders)  
    def load_next_level(self):                                                  #!!! use camelCase for method names
        self.level.load(self.level.current_level)
        self.all_bricks = Group()                                               #!!! refactor this to single responsibility 
    
        self.brick = [Brick() for i in range(self.level.brick_x.__len__())]
        for i in range(self.level.brick_x.__len__()):
            self.all_bricks.add(self.brick[i])
            self.all_visual_objects.add(self.all_bricks)
            self.brick[i].rect.x = self.level.brick_x[i]
            self.brick[i].rect.y = self.level.brick_y[i]
            self.brick[i].brick_hardnes = self.level.brick_break[i]
            self.brick[i].paint(self.brick[i].brick_hardnes)
        pass    
    def load_all_visual_object(self):                                           #!!! use camelCase for method names
                                                                                #!!! this method should have array of sprite objects?
        for _border in self.all_borders:
            self.all_bricks.add(_border)                                        #!!! all_bricks but border?
        self.all_bricks.add(self.stick)                                         #!!! all_bricks but stick?
        pass
    
    pass    
game = Game()
game.load_next_level()              #!!! why next level?
game.load_all_visual_object()
  
ball_colision = BallColision() 
# Game loop
running = True
 
while running:
     
    clock.tick(FPS)                 #!!! is FPS is frame per second?
     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                game.brick[game.all_bricks.__len__()-1].kill()
                game.brick[game.all_bricks.__len__()-1].remove()
        
    ball_colision.detect()        
    # Draw / render
    #!!! above code smells. Looks like procedure approach. Something is NotImplemented maybe...
    screen.fill(COLOR_BLACK)
    game.all_bricks.draw(brick_screen)
    ball_colision.all_balls.draw(screen)
    game.all_borders.update()
    ball_colision.all_balls.update()
    game.all_sticks.update()
    pygame.display.flip()

pygame.quit()