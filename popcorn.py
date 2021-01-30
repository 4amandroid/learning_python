from typing import Any
import pygame
from pygame.sprite import Sprite, Group
from pygame.time import Clock
from pygame.color import Color
from pygame import Surface
from Config import *
from Level import Level
from Coordinate import Coordinate 
from Border import Border
from Brick import Brick
from Ball import Ball
from Stick import Stick
from CollisionInfo import CollisionInfo

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
        self.border[UP_BORDER_NUMBER].rect = self.border[UP_BORDER_NUMBER].image.get_rect() 
        self.border[UP_BORDER_NUMBER].image.fill(COLOR_GREEN)  
        self.all_borders = Group()
        border_location = Coordinate()    
        for i in range(BORDER_LOCATION.__len__()):
            self.all_borders.add(self.border[i])
            border_location.x , border_location.y = BORDER_LOCATION[i] 
            self.border[i].rect.topleft = (border_location.x , border_location.y) 
        self.all_borders.add(self.border)
    
    def __initializeBalls(self, number_of_balls: int) -> None:
        self.number_of_balls = DEFAULT_NUMBER_OF_BALLS
        self.all_balls = Group()
        self.ball = [Ball() for i in range(number_of_balls)]  
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
        
    
        
    def getAllVisualObject(self) -> None:        
        self.all_visual_objects = Group() 
        self.all_visual_objects.add(self.level.all_bricks)
        self.all_visual_objects.add(self.stick)  
        self.all_visual_objects.add(self.all_borders)
        
    def changeDirection(self, ball, visual_object):
        #print(ball,visual_object)
        
        if abs(visual_object.rect.top - ball.rect.bottom) < self.tolerance and ball.y_speed > 0:
            ball.y_speed *= -1
            if isinstance(visual_object, Stick):
                if (ball.rect.x-visual_object.rect.x) < STICK_LENGTH//3: 
                    if ball.x_speed > 0: ball.x_speed *= -1
                elif (ball.rect.x-visual_object.rect.x)> STICK_LENGTH - STICK_LENGTH//3:
                    if ball.x_speed < 0: ball.x_speed *= -1
                 
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
                    
        
game = Game()
game.level.loadCurrentLevel()              #!!! why next level?
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
        game.changeDirection(game.collisionInfo.ball, game.collisionInfo.visual_object)
        if isinstance(game.collisionInfo.visual_object, Brick):  
            if game.collisionInfo.visual_object.brick_hardness == min(game.level.brick_break):    
                game.collisionInfo.visual_object.kill()
                if len(game.level.all_bricks) == game.level.number_of_unbreakable_bricks:
                    game.level.current_level += 1
                    game.level.loadCurrentLevel()
                    game.getAllVisualObject()
            else:
                if game.collisionInfo.visual_object.brick_hardness < max(game.level.brick_break):
                    game.collisionInfo.visual_object.brick_hardness -= 1
            game.collisionInfo.visual_object.paint(game.collisionInfo.visual_object.brick_hardness)
     
    
    # Draw / render
    game.screen.fill(COLOR_BLACK)
    game.all_visual_objects.draw(game.brick_screen)
    game.all_balls.draw(game.screen)
    game.all_balls.update()
    game.all_sticks.update()
    pygame.display.flip()

pygame.quit()