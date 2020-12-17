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


class Level():
    levels = ['level1', 'level2', 'level3', 'level4']
    def __init__(self):
        self.brick_x = []
        self.brick_y = []
        self.brick_break = []
        self.curtent_level = 0

    def load(self):
        #levels = ['level1', 'level2', 'level3', 'level4']
        with open('levels.json') as json_file:
            data = json.load(json_file)
            #levelFromfile: Level = Level()
            self.brick_x = data[self.levels[self.curtent_level]][0]['brick_x']
            self.brick_y = data[self.levels[self.curtent_level]][0]['brick_y']
            self.brick_break = data[self.levels[self.curtent_level]][0]['brick_break']
 
        pass
    def save(self):
        data = {}
        data[self.levels[self.curtent_level]].append({
            'brick_x': self.brick_x,
            'brick_y': self.brick_y,
            'brick_break': self.brick_break
        })
        with open('saved.json', 'w') as outfile:
            json.dump(data, outfile)
        pass

class BaseGameObject:

    def __init__(self):
        self.level = Level()
        self.level.load()
        

    pass


class Brick(BaseGameObject):
    
    def __init__(self):
        self.offset_x = BRICK_OFFSET_X
        self.offset_y = BRICK_OFFSET_Y
        super().__init__()
 
    def remove(self):
        self.level.brick_x.pop(0)
        self.level.brick_y.pop(0)
        self.level.brick_break.pop(0)
        number_of_bricks = len(self.level.brick_x)
        if number_of_bricks == 100: #replace with number_of_brick-unbreakable_brick
            self.level.curtent_level += 1
            self.level.load()
        return number_of_bricks
        
    def draw(self, screen: pygame.Surface, pygame: pygame):
        brick_coordinate = Coordinate()
        color_brick = LIGHT_GREEN
        for i in range(self.level.brick_x.__len__()):
            brick_coordinate.x = self.level.brick_x[i]
            brick_coordinate.y = self.level.brick_y[i]
            _p = self.level.brick_break[i]
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
    game.end_update(game.my_pygame)
    clock.tick(200)