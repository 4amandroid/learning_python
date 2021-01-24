#test branch
import pygame
from pygame.sprite import Sprite, Group
from pygame.time import Clock
from pygame.color import Color
from pygame import Surface

from Config import *
from Level import Level
 
FPS = 100

#define colors
TOP_LEFT_SURFACE = (0,0) 
BACKGROUND_COLOR = (0, 0, 0)                         
BRICK_IMAGE = ['brick.png','brick1.png','brick2.png','brick3.png']      #!!! use function to load names e.g. brick+level+.png
SIDE_BORDER_WIDTH = 20
BORDER_LOCATION = [TOP_LEFT_SURFACE,(SCREEN_WIDTH-SIDE_BORDER_WIDTH, UP_WALL_Y),TOP_LEFT_SURFACE]  
UP_BORDER_NUMBER = 2
UP_BORDER_HEIGHT = 35

BALL_X_SPEED = 2
BALL_Y_SPEED = 2.3 #TODO make speed random
DEFAULT_NUMBER_OF_BALLS = 5
COLISION_TOLERANCE = 4


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
        self.image = Surface((SIDE_BORDER_WIDTH, SCREEN_WIDTH))  
        self.rect = self.image.get_rect()
        self.image.fill(COLOR_GREEN)
        
         
   
class Brick(Sprite):
    def __init__(self):
        super().__init__()
        self.brick_hardness :int= 0
        self.image = Surface((BRICK_OFFSET_X, BRICK_OFFSET_Y))
        #self.brick_image = pygame.image.load('brick.png')
        self.image.set_colorkey(BACKGROUND_COLOR)   
        self.rect = self.image.get_rect()           
           
    def paint(self,brick_hardness:int):               
        self.brick_hardness = brick_hardness           
        self.brick_image = pygame.image.load(BRICK_IMAGE[brick_hardness-1])
        self.image.blit(self.brick_image,TOP_LEFT_SURFACE)      
        pass
    
    
class Ball(Sprite):
    
    def __init__(self):
        super().__init__()
        self.x_speed = BALL_X_SPEED           
        self.y_speed = BALL_Y_SPEED          
        self.color = COLOR_RED
        self.ball_radius = BALL_RADIUS         
        self.image = Surface((self.ball_radius*2, self.ball_radius*2))
        self.image.set_colorkey(BACKGROUND_COLOR)
        
        pygame.draw.circle(self.image, self.color, (self.ball_radius,self.ball_radius), self.ball_radius)
        self.rect = self.image.get_rect()
        self.rect.center = (self.ball_radius, self.ball_radius)
        self.rect.y = STICK_Y_POSITION         
    def update(self) -> None:
        self.rect.x += int(self.x_speed) #!!! coordinate += speed :) time-space continuum? :)
        self.rect.y += int(self.y_speed)  
        if self.rect.bottom >= SCREEN_HEIGHT or self.rect.top <= 0:
            self.y_speed *= -1 # will be removed
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.x_speed *= -1    
         
        

class Stick(Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = Surface((107, 22))             #!!! avoid magic numbers
        self.stick_image = pygame.image.load(STICK_TEXTURE)
        self.image.blit(self.stick_image,TOP_LEFT_SURFACE)
        self.image.set_colorkey(BACKGROUND_COLOR)
        self.rect = self.image.get_rect()
         
        
    def update(self):
        self.rect.x = pygame.mouse.get_pos()[0]     #!!! mouse should return coordinate object: Coordinate(pygame.mouse.get_pos()).x
        self.rect.y = STICK_Y_POSITION
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH  
class Game():
    def __init__(self):
        #self.current_level = 0
        self.level = Level()
        self.border = Border()
        self.border = [Border() for i in range(BORDER_LOCATION.__len__())]
        self.border[UP_BORDER_NUMBER].image =Surface((SCREEN_WIDTH, UP_BORDER_HEIGHT))                        
        self.border[UP_BORDER_NUMBER].rect = self.border[UP_BORDER_NUMBER].image.get_rect()#TODO think something else
        self.border[UP_BORDER_NUMBER].image.fill(COLOR_GREEN)      
        self.all_borders = Group()    
        self.all_borders.add(self.border)
        self.stick = Stick()
        self.all_sticks = Group()
        self.all_sticks.add(self.stick)
        for i in range(BORDER_LOCATION.__len__()):
            self.all_borders.add(self.border[i])
            self.border[i].rect.topleft = BORDER_LOCATION[i]
            #self.all_borders.add(self.border[i])
        self.all_visual_objects = Group() 
        self.number_of_balls = DEFAULT_NUMBER_OF_BALLS
        self.all_balls = Group()
        self.ball = Ball()
        self.ball = [Ball() for i in range(self.number_of_balls)] #think to move num_of_ball in Game
        self.all_balls.add(self.ball)               #!!! is this be always one object of ball? 
        self.tolerance = COLISION_TOLERANCE
        
    def load_next_level(self):                                                  #!!! use camelCase for method names
        self.level.load(self.level.current_level)
        self.all_bricks = Group()                                               #!!! refactor this to single responsibility 
    
        self.brick = [Brick() for i in range(self.level.brick_x.__len__())]
        for i in range(self.level.brick_x.__len__()):
            self.all_bricks.add(self.brick[i])
            #self.all_visual_objects.add(self.all_bricks)
            self.brick[i].rect.x = self.level.brick_x[i]
            self.brick[i].rect.y = self.level.brick_y[i]
            self.brick[i].brick_hardness = self.level.brick_break[i]
            self.brick[i].paint(self.brick[i].brick_hardness)
        pass    
    def load_all_visual_object(self):                                           #!!! use camelCase for method names
                                                                                 
        #for _border in self.all_borders:
        #    self.all_bricks.add(_border)   
        self.all_visual_objects.add(self.all_bricks)                                     
        self.all_visual_objects.add(self.stick)  
        self.all_visual_objects.add(self.all_borders) 
        pass
    
    pass    

    def collideDetect(self):    
        for visual_object in game.all_visual_objects:   #!!! unacceptable! game is no place here
            for _ball in self.all_balls:
                if _ball.rect.colliderect(visual_object.rect):#!!! extract ifs as separate method for now
                    if abs(visual_object.rect.top - _ball.rect.bottom) < self.tolerance and _ball.y_speed > 0:
                        _ball.y_speed *= -1
                    if abs(visual_object.rect.bottom - _ball.rect.top) < self.tolerance and _ball.y_speed < 0:
                        _ball.y_speed *= -1 
                    if abs(visual_object.rect.right - _ball.rect.left) < self.tolerance and _ball.x_speed < 0:  
                        _ball.x_speed *= -1   
                    if abs(visual_object.rect.left - _ball.rect.right) < self.tolerance and _ball.x_speed > 0:  
                        _ball.x_speed *= -1
                    if isinstance(visual_object, Brick):  
                        if visual_object.brick_hardness == 1:    
                            visual_object.kill() 
                        if visual_object.brick_hardness > 1 and visual_object.brick_hardness < 4: #!!! if 1 <= visual_object.brick_hardnes <= 4:
                            visual_object.brick_hardness -= 1
                        visual_object.paint(visual_object.brick_hardness) 
                        print(visual_object.brick_hardness)
                        print(len(game.all_bricks))
                 
                        if len(game.all_visual_objects) == 15:      #num_of_bricks - unbrakeble_bricks
                           game.level.current_level += 1           #!!! unacceptable! game and level logic is no place here
                           game.load_next_level() 
                           game.load_all_visual_object()
                        print(type(visual_object))    
                        return visual_object.rect
    pass   

game = Game()
game.load_next_level()              #!!! why next level?
game.load_all_visual_object()
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
        
    game.collideDetect()        
    # Draw / render
    #!!! above code smells. Looks like procedure approach. Something is NotImplemented maybe...
    screen.fill(COLOR_BLACK)
    game.all_visual_objects.draw(brick_screen)
    game.all_balls.draw(screen)
    #game.all_visual_objects.update()
    game.all_balls.update()
    game.all_sticks.update()
    pygame.display.flip()

pygame.quit()