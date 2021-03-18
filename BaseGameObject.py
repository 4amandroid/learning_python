from typing import Tuple, List, Any
import pygame
from Config import *
from pygame.sprite import Sprite
from pygame import Surface
from Coordinate import Coordinate
from Brick import Brick
from pygame.sprite import Sprite, Group
from Stick import Stick 

class BaseGameObject(Sprite):
    def __init__(self,surface_width :int = SIDE_BORDER_WIDTH, surface_height :int = SCREEN_WIDTH) -> None: 
        super().__init__()
        self.image = Surface((surface_width, surface_height))  
        self.rect = self.image.get_rect()
        #self.image.fill(COLOR_GREEN)
        self.image.set_colorkey(BACKGROUND_COLOR)
        
    def getAllVisualObjects(self) -> None:        
        self.all_visual_objects = Group() 
        self.all_visual_objects.add(self.level.all_bricks)
        self.all_visual_objects.add(self.stick)  
        self.all_visual_objects.add(self.border.all_borders)

    def luckCollideDetect(self, stick, lucks: List[Any]) -> None:  # TO DO change name
        self.images = STICK_IMAGES
        def resetLucks(stick, luck, luck_number):
            stick_lucks=[False] * len(self.images)
            stick_lucks[luck_number] = True
            stick.shoot, stick.glue, stick.longbar, stick.shortbar = stick_lucks
        for luck in lucks:
            if luck.rect.colliderect(stick.rect):
                if luck.number in range(len(self.images)):
                    resetLucks(stick, luck, luck.number)
                    stick.initChangedStick(stick, self.images[luck.number])
                luck.kill()
            elif luck.rect.bottom > SCREEN_HEIGHT:
                luck.kill()    
     #TODO kakvo ще стане ако подам брикса директно
    def bulletCollideDetect(self, bricks: List[Brick], bullets: List[Any]):
        for bullet in bullets:
            for brick in bricks:
                if bullet.rect.colliderect(brick.rect):
                    bullet.kill()
                    if brick.brick_hardness < 4:
                        brick.kill()
                elif bullet.rect.y < UP_BORDER_HEIGHT:
                    bullet.kill()   
    def changeDirection(self, ball, visual_object):
        if isinstance(visual_object, Stick):
            ball.x_correction = (ball.rect.x-visual_object.rect.x)
            if visual_object.glue:
                ball.glued = True 
                if visual_object.glue and ball.glued:
                    if ball.x_speed != 0:
                        if ball.x_speed < 0:
                            ball.correct_glue_direction = -1
                        else:
                            ball.correct_glue_direction = 1
                    ball.x_speed = 0
                    ball.y_speed = 0
                    ball.rect.top -=1
                    return
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
class Brick(BaseGameObject):
        
    def __init__(self):
        super().__init__(BRICK_OFFSET_X, BRICK_OFFSET_Y)
        self.brick_hardness :int= 0
        #self.image = Surface((BRICK_OFFSET_X, BRICK_OFFSET_Y))
        #self.image.set_colorkey(BACKGROUND_COLOR)   
        #self.rect = self.image.get_rect()     
              
    def paint(self,brick_hardness:int) -> None:               
        self.brick_hardness = brick_hardness           
        self.brick_image = pygame.image.load(BRICK_IMAGE[brick_hardness-1])
        self.image.blit(self.brick_image,TOP_LEFT_SURFACE)

class Ball(BaseGameObject):
    
    def __init__(self) -> None:
        super().__init__(BALL_RADIUS*2,BALL_RADIUS*2)
        self.x_speed =  BALL_X_SPEED
        self.y_speed =  BALL_Y_SPEED
        self.color = COLOR_RED
        self.ball_radius = BALL_RADIUS         
        #self.image = Surface((self.ball_radius*2, self.ball_radius*2))
        #self.image.set_colorkey(BACKGROUND_COLOR)
        pygame.draw.circle(self.image, self.color, (self.ball_radius,self.ball_radius), self.ball_radius)
        #self.rect = self.image.get_rect()
        self.rect.center = (self.ball_radius, self.ball_radius)
        self.rect.y = STICK_Y_POSITION - self.ball_radius
        self.rect.x = SCREEN_WIDTH//2
        self.glued = False
        self.glueXPos = 0
        self.x_correction = 0
        self.correct_glue_direction = 1

    def initializeBalls(self, number_of_balls: int=DEFAULT_NUMBER_OF_BALLS) -> None:
        self.number_of_balls = DEFAULT_NUMBER_OF_BALLS
        self.all_balls = Group()
        self.ball = [Ball() for i in range(number_of_balls)]  
        self.all_balls.add(self.ball) 

    def update(self, x) -> None:
        if self.glued:
            self.rect.x = x + self.x_correction
        else:
            self.rect.x += int(self.x_speed) #!!! coordinate += speed :) time-space continuum? :)
            self.rect.y += int(self.y_speed)  
        
        if self.rect.top <= 0:
            self.y_speed *= -1  
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.x_speed *= -1
        # TODO debug when colision bug ball to border
        if self.rect.top <= UP_BORDER_HEIGHT - COLISION_TOLERANCE:
            print("collision bug")
            self.y_speed *= -1  
        if self.rect.left <= SIDE_BORDER_WIDTH - COLISION_TOLERANCE or self.rect.right >= SCREEN_WIDTH-SIDE_BORDER_WIDTH+COLISION_TOLERANCE: 
            self.x_speed *= -1
            print("collision bug") 
class Border(BaseGameObject):
    def __init__(self) -> None:
        super().__init__()
        self.image.fill(COLOR_GREEN)
    def initializeBorderFrame(self) -> None:
        self.border = [Border() for i in range(BORDER_LOCATION.__len__())]
        self.border[UP_BORDER_NUMBER].image = Surface((SCREEN_WIDTH, UP_BORDER_HEIGHT))                        
        self.border[UP_BORDER_NUMBER].rect = self.border[UP_BORDER_NUMBER].image.get_rect()
        self.border[UP_BORDER_NUMBER].image.fill(COLOR_RED)  
        self.all_borders = Group()
        border_location = Coordinate()    
        for i in range(BORDER_LOCATION.__len__()):
            self.all_borders.add(self.border[i])
            border_location.x , border_location.y = BORDER_LOCATION[i] 
            self.border[i].rect.topleft = (border_location.x , border_location.y) 
        self.all_borders.add(self.border)


    