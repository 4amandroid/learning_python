import json
import pygame

pygame.init()
POPCORN_GREEN_BAR_PNG = "/home/ivan/Desktop/my_project/source/popcorn/greenbar.png"

class Coordinate:
    x = 0
    y = 0

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        pass


class Level:
    def __init__(self):
        self.left_x_brick = []
        self.up_y_brick = []
        self.brick_difficulty = []

    def load(self):
        with open('data2.txt') as json_file:
            data = json.load(json_file)
            for p in data['level4']:
                self.left_x_brick = p['brick_x']
                self.up_y_brick = p['brick_y']
                self.brick_difficulty = p['brick_break']


class BaseGameObject:

    def __init__(self):
        self.level = Level()
        self.level.load()
        # print(self.level.LEVEL1_Y_BRICK)
        pass

    pass


class Brick(BaseGameObject):
    def __init__(self):
        super().__init__()
        print(self.level.left_x_brick)
        print(self.level.up_y_brick)
        print(self.level.brick_difficulty)

    def print_massive(self):
        print(self.level.left_x_brick)


class Stick:
    pass       


class Player:
    def __init__(self, stick, ):
        pass

    def move_stick(self, screen: pygame.Surface):
        # remove hardcoded position
        x = game.my_pygame.mouse.get_pos()[0]
        if x > (RIGHT_WALL_X - STICK_LENGHT):
            x = (RIGHT_WALL_X - STICK_LENGHT)
        screen.blit(game.stick_img, (x, 550))
        return x


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
        self.screen.fill((95, 222, 146))
        self.sick_img = self.my_pygame.image.load(POPCORN_GREEN_BAR_PNG)
        self.stick = Stick()
        self.screen.blit(self.sick_img, (1, 550))
        self.player = Player(self.stick)
        self.level = Make_level()
        self.level.make()

    def get_ball(self):
        coords = ball.move(game.screen)
        self.ball_coordinate.x = coords[0]
        self.ball_coordinate.y = coords[1]
        return self.ball_coordinate

    def get_mouse(self):
        coords = game.my_pygame.mouse.get_pos()
        self.mouse_coordinate.x = coords[0]
        self.mouse_coordinate.y = coords[1]
        return self.mouse_coordinate

    def begin_update(self, screen):
        screen.fill((95, 222, 146))

    def end_update(self, my_pygame):
        my_pygame.display.update()


f = Brick()
f.print_massive()
