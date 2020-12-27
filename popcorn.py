import pygame
from Stick import Stick
from Config import *
from Brick import Brick
from Coordinate import Coordinate
pygame.init()

class Game:
    running = True
    mouse_coordinate = Coordinate()
    ball_coordinate = Coordinate()

    def __init__(self):
        self.my_pygame = pygame
        self.screen = self.my_pygame.display.set_mode((1000, 600))
        self.my_pygame.display.set_caption("")
        self.icon = self.my_pygame.image.load(POPCORN_GREEN_BAR_PNG)
        self.my_pygame.display.set_icon(self.icon)
        self.stick_img = self.my_pygame.image.load(POPCORN_GREEN_BAR_PNG)
        
    def get_mouse(self):
        coords = game.my_pygame.mouse.get_pos()
        self.mouse_coordinate.x = coords[0]
        self.mouse_coordinate.y = coords[1]
        return self.mouse_coordinate

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
        if event.type == game.my_pygame.QUIT:
            game.running = False
        if event.type == game.my_pygame.KEYDOWN:
            if event.key == game.my_pygame.K_q:
                game.running = False
                #s = Level()
                #s.save()
            if event.key == game.my_pygame.K_z:
                bricks.remove()
            if event.key == game.my_pygame.K_x:
                bricks.remove()
            if event.key == game.my_pygame.K_c:
                bricks.remove()
    bricks.draw(game.screen, pygame)
    stick.move(game.screen) 
    game.end_update(game.my_pygame)
    clock.tick(200)