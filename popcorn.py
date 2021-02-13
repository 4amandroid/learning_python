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
from Stick import Stick,Bullet
from CollisionInfo import CollisionInfo
 
class Game():
    def __init__(self):
        # create instances of core game objects
        self.level = Level()
        self.border = Border()
        self.ball = Ball()
        self.stick = Stick()
        self.bullet = Bullet()
        self.all_bullets = Group()
        self.points=0
        self.points_per_brick = POINTS_PER_BRICK
        # initialize core game objects
        self.__initializeBorderFrame()
        self.__initializeBalls(DEFAULT_NUMBER_OF_BALLS)
        self.__initSticks()
        
        self.lives = DEFAULT_NUMBER_OF_LIVES
        self.tolerance = COLISION_TOLERANCE
        self.clock = Clock()
        self.__initializeGraphics(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        self.collisionInfo = None
        
    def __initializeBorderFrame(self) -> None:
        self.border = [Border() for i in range(BORDER_LOCATION.__len__())]
        self.border[UP_BORDER_NUMBER].image =Surface((SCREEN_WIDTH, UP_BORDER_HEIGHT))                        
        self.border[UP_BORDER_NUMBER].rect = self.border[UP_BORDER_NUMBER].image.get_rect() 
        self.border[UP_BORDER_NUMBER].image.fill(COLOR_RED)  
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
            self.font = pygame.font.SysFont(None, FONT_SIZE)
    def printItemBar(self,points = 0):
        self.points=points
        
        bar_text =('POINTS  ' + str(self.points) + '  LIVES  '+ str(self.lives)+'  LEVEL  ' + str(self.level.current_level+1))
        if self.lives == 0 and len(self.all_balls) == 0:
            bar_text = 'G A M E   O V E R'
            self.font = pygame.font.SysFont(None, FONT_SIZE*4)
        self.text = self.font.render( bar_text, True, COLOR_GREEN, COLOR_RED)
        self.textRect = self.text.get_rect()
        self.textRect.midtop = (SCREEN_WIDTH//2,UP_WALL_Y)
        self.screen.blit(self.text,self.textRect)      

    def getAllVisualObject(self) -> None:        
        self.all_visual_objects = Group() 
        self.all_visual_objects.add(self.level.all_bricks)
        self.all_visual_objects.add(self.stick)  
        self.all_visual_objects.add(self.all_borders)
        
     
        
   
    def changeDirection(self, ball, visual_object):
        if isinstance(visual_object, Stick):
            if (ball.rect.x-visual_object.rect.x) < STICK_LENGTH//3: 
                if ball.x_speed > 0: ball.x_speed *= -1
            elif (ball.rect.x-visual_object.rect.x)> STICK_LENGTH - STICK_LENGTH//3:
                if ball.x_speed < 0: ball.x_speed *= -1
            
        if (abs(visual_object.rect.top - ball.rect.bottom) < self.tolerance and ball.y_speed > 0) or \
               (abs(visual_object.rect.bottom - ball.rect.top) < self.tolerance and ball.y_speed < 0):
            ball.y_speed *= -1
        elif (abs(visual_object.rect.right - ball.rect.left) < self.tolerance and ball.x_speed < 0) or \
                 (abs(visual_object.rect.left - ball.rect.right) < self.tolerance and ball.x_speed > 0):
            ball.x_speed *= -1   
         
        
        pass

    def collideDetect(self):    
        for visual_object in self.all_visual_objects:
            for ball in self.all_balls:
                if ball.rect.bottom >= SCREEN_HEIGHT:
                    ball.kill()
                if ball.rect.colliderect(visual_object.rect): 
                    return CollisionInfo(ball, visual_object)
                    
                else:
                    self.collisionInfo = None
    def bulletCollideDetect(self):
        for bullet in self.all_bullets:
            for brick in self.level.all_bricks:
                if bullet.rect.colliderect(brick.rect):
                    bullet.kill()
                    if brick.brick_hardness < 4: 
                        brick.kill()
                elif bullet.rect.y < UP_BORDER_HEIGHT:
                    bullet.kill()     
game = Game()
game.level.loadCurrentLevel()               
game.getAllVisualObject()
# Game loop
running = True
 
while running:
     
    game.clock.tick(FPS)                 #!!! is FPS is frame per second?
     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.mixer.Sound.play(pygame.mixer.Sound('dum.wav'))  
            bullet=Bullet()
            game.all_bullets.add(bullet)
            print(game.all_bullets)
    game.collisionInfo = game.collideDetect()
    game.bulletCollideDetect()
    if game.collisionInfo is not None:
       
        game.changeDirection(game.collisionInfo.ball, game.collisionInfo.visual_object)
        if isinstance(game.collisionInfo.visual_object, Brick):
            game.points += game.points_per_brick
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
    if len(game.all_balls) == 0:
        if game.lives > 0:
            game.lives -= 1
            game.ball = [Ball() for i in range(DEFAULT_NUMBER_OF_BALLS)]  
            game.all_balls.add(game.ball) 
         
        
    # Draw / render
    game.screen.fill(COLOR_BLACK)
    game.all_visual_objects.draw(game.brick_screen)
    game.all_balls.draw(game.screen)
    game.all_balls.update()
    game.all_sticks.update()
    game.all_bullets.draw(game.screen)
    game.all_bullets.update()
    game.printItemBar(game.points)
    
    pygame.display.flip()

pygame.quit()
