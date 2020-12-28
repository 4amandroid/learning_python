import pygame
from pygame.constants import KEYDOWN, K_c, K_q, K_x, K_z, QUIT
from Stick import Stick
from Config import *
from Brick import Brick
from Coordinate import Coordinate
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
        self.icon = self.my_pygame.image.load(STICK_TEXTURE)
        self.my_pygame.display.set_icon(self.icon)
        self.stick_img = self.my_pygame.image.load(STICK_TEXTURE)
        
    def get_mouse(self)-> Coordinate: 
        return Coordinate(game.my_pygame.mouse.get_pos())

    def begin_update(self, screen: pygame.Surface):
        screen.fill((95, 222, 146))
        return True

    def end_update(self, my_pygame: pygame):
        my_pygame.display.update()
        return True

game = Game()
bricks = Brick()
stick = Stick()
clock = pygame.time.Clock()
 
while game.running:
    game.begin_update(game.screen)
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
                
    bricks.draw(game.screen, pygame)
    
    stick.move(game.screen) 
    game.end_update(game.my_pygame)
    clock.tick(200)