import pygame
from pygame.constants import KEYDOWN, K_c, K_q, K_x, K_z, QUIT
from Stick import Stick
from Config import *
from Brick import Brick
from Coordinate import Coordinate
from Ball import Ball
import compileall
compileall.compile_dir("./")


class Game:
    running = True
    mouse_coordinate = Coordinate()
    ball_coordinate = Coordinate()
    
    def __init__(self):
        pygame.init()
        self.my_pygame = pygame
        self.screen: pygame.Surface = self.my_pygame.display.set_mode((1000, 600))
        self.screen1 = self.my_pygame.display.set_mode((1000, 600))
        self.icon = self.my_pygame.image.load(STICK_TEXTURE)
        self.my_pygame.display.set_icon(self.icon)
        self.stick_img = self.my_pygame.image.load(STICK_TEXTURE)
        
    def get_mouse(self)-> Coordinate: 
        return Coordinate(game.my_pygame.mouse.get_pos())

    def begin_update(self, screen: pygame.Surface):
        self.screen.fill((0, 0, 0))
        return True

    def end_update(self, my_pygame: pygame):
        my_pygame.display.update()
        return True
ball = Ball()
ball.move_up_right = True
game = Game()
bricks = Brick()
stick = Stick()
clock = pygame.time.Clock()
 
while game.running:
    game.begin_update(game.screen1)
    for event in game.my_pygame.event.get():
        if event.type == QUIT:
            game.running = False
        if event.type == KEYDOWN:
            if event.key == K_q:
                game.running = False
                #s = Level()
                #s.save()
            if event.key == K_z:
                bricks.remove()
            if event.key == K_x:
                bricks.remove()
            if event.key == K_c:
                bricks.remove()
    #ball.move(game.screen) 
    ball.level_brick_x = bricks.level.brick_x
    ball.level_brick_y = bricks.level.brick_y  
    ball.move(game.screen1) 
    bricks.draw(game.screen, pygame)
    
    """
    class collision_info:
        # https://docs.python.org/3/library/enum.html
        directionFrom : enum.up_left
                        enum.up_right
                        enum.down_left
                        enum.down.right
                        
        directionTo   : enum.up_left # може да мине без единия...
                        enum.up_right
                        enum.down_left
                        enum.down.right
                        
        object_type : wall/brick/stick
        
    
    ball.move_to(inital_direction)
    for brick in bricks:                                                        # обхожда тухла по тухла
        for visibleObject in (stick, brick, wall):                              # https://www.geeksforgeeks.org/polymorphism-in-python/
            if visibleObject.collision(ball.get_current_position()):            # всеки обект който наследява общия клас има метод collision
                collision_info = visibleObject.get_collision_info()             # информацията в един обект с полета които са за след колизията
                if collision_info.object_type = brick and brick.hardess = 1:
                    brick.kill()
            # save old data for collision_info to compare
            ball.move_to(collision_info)
            

                    
    """
    
    #stick.move(game.screen) 
    game.end_update(game.my_pygame)
    clock.tick(220)