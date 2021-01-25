from typing import Any
import pygame
from pygame.sprite import Sprite, Group
from pygame.time import Clock
from pygame.color import Color
from pygame import Surface
from Config import *
from Level import Level

class Border(Sprite):
    def __init__(self) -> None: 
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
           

    def paint(self,brick_hardness:int) -> None:               
        self.brick_hardness = brick_hardness           
        self.brick_image = pygame.image.load(BRICK_IMAGE[brick_hardness-1])
        self.image.blit(self.brick_image,TOP_LEFT_SURFACE)      
        
    
class Ball(Sprite):
    
    def __init__(self) -> None:
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
        
    def update(self) -> None:
        self.rect.x = pygame.mouse.get_pos()[0]     #!!! mouse should return coordinate object: Coordinate(pygame.mouse.get_pos()).x
        self.rect.y = STICK_Y_POSITION
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH  

class CollisionInfo:
    def __init__(self, ball, visual_object):
        self.ball = ball
        self.visual_object = visual_object
        
class Game():
    def __init__(self):
        # create instances of core game objects
        self.level = Level()
        self.border = Border()
        self.ball = Ball()
        self.stick = Stick()
        
        # initialize core game objects
        self.__initializeBorderFrame()
        self.__initializeBalls(DEFAULT_NUMBER_OF_BALLS)
        self.__initSticks()
        
        
        self.tolerance = COLISION_TOLERANCE
        self.clock = Clock()
        self.__initializeGraphics(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        self.collisionInfo = None
        
    def __initializeBorderFrame(self) -> None:
        self.border = [Border() for i in range(BORDER_LOCATION.__len__())]
        self.border[UP_BORDER_NUMBER].image =Surface((SCREEN_WIDTH, UP_BORDER_HEIGHT))                        
        self.border[UP_BORDER_NUMBER].rect = self.border[UP_BORDER_NUMBER].image.get_rect()#TODO think something else
        self.border[UP_BORDER_NUMBER].image.fill(COLOR_GREEN)  
        self.all_borders = Group()    
        for i in range(BORDER_LOCATION.__len__()):
            self.all_borders.add(self.border[i])
            self.border[i].rect.topleft = BORDER_LOCATION[i]  
        self.all_borders.add(self.border)
    
    def __initializeBalls(self, number_of_balls: int) -> None:
        self.number_of_balls = DEFAULT_NUMBER_OF_BALLS
        self.all_balls = Group()
         
        self.ball = [Ball() for i in range(number_of_balls)]  
        for i in range(number_of_balls):
            self.ball[i].rect.x = i*10  # this will be removed
        self.all_balls.add(self.ball) 
        
    
    def __initSticks(self) -> None:
        self.all_sticks = Group()
        self.all_sticks.add(self.stick)
            
    def __initializeGraphics(self, screen_width: int, screen_height: int) -> None:
            pygame.init()
            pygame.mixer.init()
            self.screen = pygame.display.set_mode((screen_width, screen_height))
            self.brick_screen = pygame.display.set_mode((screen_width, screen_height))
            pygame.display.set_caption("My Game")    
        
    def loadNextLevel(self):                                                  
        self.level.load(self.level.current_level)
        self.all_bricks = Group()                                              
    
        self.brick = [Brick() for i in range(self.level.brick_x.__len__())]
        for i in range(self.level.brick_x.__len__()):
            self.all_bricks.add(self.brick[i])
            #self.all_visual_objects.add(self.all_bricks)
            self.brick[i].rect.x = self.level.brick_x[i]
            self.brick[i].rect.y = self.level.brick_y[i]
            self.brick[i].brick_hardness = self.level.brick_break[i]
            self.brick[i].paint(self.brick[i].brick_hardness)
    
    def getAllVisualObject(self) -> None:        
        self.all_visual_objects = Group() 
        self.all_visual_objects.add(self.all_bricks)
        self.all_visual_objects.add(self.stick)  
        self.all_visual_objects.add(self.all_borders)
        
    def changeDirection(self, ball, visual_object):
        if abs(visual_object.rect.top - ball.rect.bottom) < self.tolerance and ball.y_speed > 0:
          ball.y_speed *= -1
        if abs(visual_object.rect.bottom - ball.rect.top) < self.tolerance and ball.y_speed < 0:
            ball.y_speed *= -1 
        if abs(visual_object.rect.right - ball.rect.left) < self.tolerance and ball.x_speed < 0:  
            ball.x_speed *= -1   
        if abs(visual_object.rect.left - ball.rect.right) < self.tolerance and ball.x_speed > 0:  
            ball.x_speed *= -1
        pass

    def collideDetect(self):    
        for visual_object in self.all_visual_objects:   #!!! unacceptable! game is no place here
            for ball in self.all_balls:
                if ball.rect.colliderect(visual_object.rect):#!!! extract ifs as separate method for now
                    return CollisionInfo(ball, visual_object)
                    
                else:
                    self.collisionInfo = None
                    
        
                    
                    # self.changeDirection(ball, visual_object)
                    # if isinstance(visual_object, Brick):  
                    #     if visual_object.brick_hardness == min(game.level.brick_break):    
                    #         visual_object.kill() 
                    #     else:
                    #         visual_object.brick_hardness -= 1
                    #     visual_object.paint(visual_object.brick_hardness) 
                        # print(visual_object.brick_hardness)
                        # if len(game.all_visual_objects) == 5:      #num_of_bricks - unbrakeble_bricks
                        #    game.level.current_level += 1           #!!! unacceptable! game and level logic is no place here
                        #    game.loadNextLevel() 
                        #    game.getAllVisualObject()
                        

game = Game()
game.loadNextLevel()              #!!! why next level?
game.getAllVisualObject()
# Game loop
running = True
 
while running:
     
    game.clock.tick(FPS)                 #!!! is FPS is frame per second?
     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    game.collisionInfo = game.collideDetect()
    if game.collisionInfo is not None:
        
        if isinstance(game.collisionInfo.visual_object, Brick): #!!! tuk nikoga ne e instancia na brick - triabva da se oprawi
            if game.collisionInfo.visual_object.brick_hardness == min(game.level.brick_break):    
                game.collisionInfo.visual_object.kill() 
            else:
                game.collisionInfo.visual_object.brick_hardness -= 1
            game.collisionInfo.visual_object.paint(game.collisionInfo.visual_object.brick_hardness)
    # Draw / render
    
    game.screen.fill(COLOR_BLACK)
    game.all_visual_objects.draw(game.brick_screen)
    game.all_balls.draw(game.screen)
    #game.all_visual_objects.update()
    game.all_balls.update()
    game.all_sticks.update()
    pygame.display.flip()

pygame.quit()