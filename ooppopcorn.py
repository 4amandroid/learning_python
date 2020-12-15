import json
import pygame

pygame.init()
POPCORN_GREEN_BAR_PNG = "/home/ivan/Desktop/my_project/source/popcorn/greenbar.png"
DARK_GREEN = (2, 62, 16)
GREEN = (0, 255, 0)
LIGHT_GREEN = (250, 248, 0)
PURPLE: pygame.Color = pygame.Color(128, 0, 128, 0)
BLUE = (0, 0, 255, 0)
RED = (255, 0, 0, 0)
WHITE = (255, 255, 255)
BRICK_OFFSET_X = 50
BRICK_OFFSET_Y = 40
RIGHT_WALL_X = 1000
STICK_LENGHT = 107
STICK_Y_POSITION = 550
class Coordinate:
    x: int = 0
    y: int = 0

    def __init__(self, x=0, y=0):
        self.x: int = x
        self.y: int = y
        pass


class Level:
    def __init__(self):
        self.left_x_brick = []
        self.up_y_brick = []
        self.brick_difficulty = []

    def load(self):
        y = []
        with open('data2.txt') as json_file:
            data = json.load(json_file)
            for p in data['level4']:
                self.left_x_brick = p['brick_x']
                self.up_y_brick = p['brick_y']
                self.brick_difficulty = p['brick_break']
            y = json.dumps('level1') 
            print(y)  


class BaseGameObject:

    def __init__(self):
        self.level = Level()
        self.level.load()
        pass

    pass


class Brick(BaseGameObject):
    
    def __init__(self):
        self.offset_x = BRICK_OFFSET_X
        self.offset_y = BRICK_OFFSET_Y
        super().__init__()
 
    def remove(self):
        self.level.left_x_brick.pop(0)
        self.level.up_y_brick.pop(0)
        self.level.brick_difficulty.pop(0)
        number_of_bricks = len(self.level.left_x_brick)
        return number_of_bricks
        
    def draw(self, screen: pygame.Surface, pygame: pygame):
        brick_coordinate = Coordinate()
        color_brick = LIGHT_GREEN
        for i in range(self.level.left_x_brick.__len__()):
            brick_coordinate.x = self.level.left_x_brick[i]
            brick_coordinate.y = self.level.up_y_brick[i]
            _p = self.level.brick_difficulty[i]
            if _p == 1 or _p == 2:
                color_brick = LIGHT_GREEN
            elif _p == 3 or _p == 4:
                color_brick = GREEN
            elif _p == 5 or _p == 6:
                color_brick = DARK_GREEN
            elif _p == 7:
                color_brick = WHITE
            pygame.draw.rect(screen, color_brick,
                             (brick_coordinate.x, brick_coordinate.y, self.offset_x, self.offset_y))
        return True

class Stick:
    
    def move(self, screen: pygame.Surface):
        stick_position = Coordinate()
        # remove hardcoded position
        stick_position.x = game.my_pygame.mouse.get_pos()[0]
        if stick_position.x > (RIGHT_WALL_X - STICK_LENGHT):
            stick_position.x = (RIGHT_WALL_X - STICK_LENGHT)
        screen.blit(game.stick_img, (stick_position.x, STICK_Y_POSITION))
        return stick_position.x
    pass       


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
            if event.key == game.my_pygame.K_z:
                bricks.remove()
            if event.key == game.my_pygame.K_x:
                bricks.remove()
            if event.key == game.my_pygame.K_c:
                bricks.remove()
                
    bricks.draw(game.screen, pygame)
    stick.move(game.screen)
    # ball3.move(game.screen)
     
    game.end_update(game.my_pygame)
    clock.tick(200)