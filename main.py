from typing import List, Tuple
import pygame

POPCORN_GREEN_BAR_PNG = "greenbar.png"
pygame.init()
STEP_X = 1
STEP_Y = 1
DARK_GREEN = (2, 62, 16)
GREEN = (0, 255, 0)
LIGHT_GREEN = (250, 248, 0)
PURPLE: pygame.Color = pygame.Color(128, 0, 128, 0)
BLUE = (0, 0, 255, 0)
RED = (255, 0, 0, 0)
WHITE = (255, 255, 255)
LEVEL1_X_BRICK = [10, 60, 110, 160, 210, 260, 310, 360, 410, 460, 510, 560, 610, 660, 710, 760, 810, 860, 910 /
                  10, 60, 110, 160, 210, 260, 310, 360, 410, 460, 510, 560, 610, 660, 710, 760, 810, 860, 910]
LEVEL1_Y_BRICK = [50, 50, 50,  50,  50,  50,  50,  50,  50,  50, 50,  50,  50,  50,  50, 50, 50,  50,  50 /
                  160, 160, 160, 160, 160, 160, 160, 160,  160,  160, 160,  160,  160,  160,  160,  160, 160, 160, 160]
LVEL1_BREAKABLE_BRICK = [6, 6, 6, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 7, 6, 6, 6, 6, 6 /
                         6, 6, 6, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 7, 6, 6, 6, 6, 6]
BRICK_OFFSET_X = 50
BRICK_OFFSET_Y = 40
UP_WALL_Y = 0
DOWN_WALL_Y = 600
LEFT_WALL_X = 0
RIGHT_WALL_X = 1000
STICK_LENGHT = 107
STICK_Y_POS = 550


class Coordinate:
    x: int = 0
    y: int = 0

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y
        pass


class Make_level:

    def make(self):
        global LEVEL1_X_BRICK
        global LEVEL1_Y_BRICK
        global LVEL1_BREAKABLE_BRICK
        LEVEL1_X_BRICK = []
        LEVEL1_Y_BRICK = []
        LVEL1_BREAKABLE_BRICK = []
        _count = -20
        _y = 40
        for _i in range(112):
            _count += 60
            if _count > 950:
                _count = 40
                _y += 60
            LEVEL1_X_BRICK.insert(_i, _count)
            LEVEL1_Y_BRICK.insert(_i, _y)
            LVEL1_BREAKABLE_BRICK.insert(_i, 4)

    pass


make_new_level = Make_level()
# make_new_level.make()


class Ball:
    def __init__(self):
        self.ball_x = 600
        self.ball_y = 500
        self.ball_radius = 5
        self.object_blowed = False
        self.up_wall_blowed = False
        self.down_wall_blowed = False
        self.left_wall_blowed = False
        self.right_wall_blowed = False
        self.move_down_right = False
        self.move_down_left = False
        self.move_up_right = False
        self.move_up_left = False
        self.color = RED

    def kill(self):
        self.move_down_right = False
        self.move_down_left = False
        self.move_up_right = False
        self.move_up_left = False

    def move(self, screen: pygame.Surface):
        stick_left_point = Coordinate()
        stick_left_point.x = Player.move_stick(self, game.screen)
        brick_left_point = Coordinate()
        brick_right_point = Coordinate()

        if (self.ball_x > stick_left_point.x) and (self.ball_x < (stick_left_point.x+STICK_LENGHT)):
            if (self.ball_y + self.ball_radius) == STICK_Y_POS:  # TODO: Replace number with const
                if self.move_down_right:
                    self.move_down_right = False
                    self.move_up_right = True
                if self.move_down_left:
                    self.move_down_left = False  # TODO blow y wall of stick change direction
                    self.move_up_left = True

        for i in range(LEVEL1_X_BRICK.__len__()):
            brick_left_point.x = int(LEVEL1_X_BRICK[i])
            # Brick_offset_x & Y must be taken from
            brick_left_point.y = int(LEVEL1_Y_BRICK[i])
            # Brick class to work when resize screen
            brick_right_point.x = (brick_left_point.x + BRICK_OFFSET_X)
            brick_right_point.y = (brick_left_point.y + BRICK_OFFSET_Y)
            # TODO ball blew in corner bugg
            if (self.ball_x >= brick_left_point.x) and (self.ball_x <= brick_right_point.x):
                if (self.ball_y == brick_left_point.y):
                    self.down_wall_blowed = True
                    self.up_wall_blowed = False
                    self.left_wall_blowed = False
                    self.right_wall_blowed = False
                if (self.ball_y == brick_right_point.y):
                    self.up_wall_blowed = True
                    self.down_wall_blowed = False
                    self.left_wall_blowed = False
                    self.right_wall_blowed = False
            if (self.ball_y >= brick_left_point.y) and (self.ball_y <= brick_right_point.y):
                if (self.ball_x == brick_left_point.x):
                    self.right_wall_blowed = True
                    self.up_wall_blowed = False
                    self.down_wall_blowed = False
                    self.left_wall_blowed = False
                if (self.ball_x == brick_right_point.x):
                    self.left_wall_blowed = True
                    self.up_wall_blowed = False
                    self.right_wall_blowed = False
                    self.down_wall_blowed = False

        if self.ball_y <= UP_WALL_Y + self.ball_radius:
            self.up_wall_blowed = True
            self.down_wall_blowed = False
            self.left_wall_blowed = False
            self.right_wall_blowed = False
        elif self.ball_x <= 0 + self.ball_radius:
            self.left_wall_blowed = True
            self.up_wall_blowed = False
            self.down_wall_blowed = False
            self.right_wall_blowed = False
        elif self.ball_y >= 600 - self.ball_radius:
            self.down_wall_blowed = True
            self.up_wall_blowed = False
            self.left_wall_blowed = False
            self.right_wall_blowed = False
        elif self.ball_x >= 1000 - self.ball_radius:
            self.right_wall_blowed = True
            self.up_wall_blowed = False
            self.down_wall_blowed = False
            self.left_wall_blowed = False

        if self.move_down_right:
            if self.down_wall_blowed:
                self.move_down_right = False
                self.move_up_right = True
                self.down_wall_blowed = False
            elif self.right_wall_blowed:
                self.move_down_right = False
                self.move_down_left = True
                self.right_wall_blowed = False
            self.ball_x += STEP_X
            self.ball_y += STEP_Y
        elif self.move_down_left:
            if self.left_wall_blowed:
                self.move_down_left = False
                self.move_down_right = True
                self.left_wall_blowed = False
            elif self.down_wall_blowed:
                self.move_down_left = False
                self.move_up_left = True
                self.down_wall_blowed = False
            self.ball_x += -STEP_X
            self.ball_y += STEP_Y
        elif self.move_up_right:
            if self.right_wall_blowed:
                self.move_up_right = False
                self.move_up_left = True
                self.right_wall_blowed = False
            elif self.up_wall_blowed:
                self.move_up_right = False
                self.move_down_right = True
                self.up_wall_blowed = False
            self.ball_x += STEP_X
            self.ball_y += -STEP_Y
        elif self.move_up_left:
            if self.left_wall_blowed:
                self.move_up_left = False
                self.move_up_right = True
                self.left_wall_blowed = False
            elif self.up_wall_blowed:
                self.move_up_left = False
                self.move_down_left = True
                self.up_wall_blowed = False
            self.ball_x += -STEP_X
            self.ball_y += -STEP_Y

        pygame.draw.circle(screen, self.color, (self.ball_x,
                                                self.ball_y), self.ball_radius)
        coords = (self.ball_x, self.ball_y)
        return coords
        pass


class Base_game_object():
    def __init__(self):
        pass
    pass


class Text:
    def __init__(self, points):
        self.points = points
        pass

    def prnt_text(self, screen: pygame.Surface):
        # pygame.font.init()
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(('Points ' + str(self.points)) +
                           ' LIVES ', True, GREEN, BLUE)
        textRect = text.get_rect()
        # set the center of the rectangular object.
        #X = 250
        #Y = 32
        #textRect.center = (X // 2, Y // 2)
        # that was returned by pygame.event.get() method.
        screen.blit(text, textRect)


class Prnt_lives(Text):
    pass


class Stick:
    pass


# brick control game
class Brick:

    def __init__(self):
        self.offset_x = BRICK_OFFSET_X
        self.offset_y = BRICK_OFFSET_Y
        self.brick_x_wall_blew = False
        self.brick_y_wall_blew = False
        self.points = 0
        self.text = Text(0)

    def remove_from_ball(self, ball_coordinate: Coordinate):
        # define brick bounderies
        brick_left_point = Coordinate()
        brick_right_point = Coordinate()
        self.brick_x_wall_blew = False
        self.brick_y_wall_blew = False
        # check each brick
        for i in range(LEVEL1_X_BRICK.__len__()):
            brick_left_point.x = int(LEVEL1_X_BRICK[i])
            brick_left_point.y = int(LEVEL1_Y_BRICK[i])
            brick_right_point.x = (brick_left_point.x + self.offset_x)
            brick_right_point.y = (brick_left_point.y + self.offset_y)
            if (ball_coordinate.x >= brick_left_point.x) and \
                    (ball_coordinate.x <= brick_right_point.x) and \
                    (ball_coordinate.y >= brick_left_point.y) and \
                    (ball_coordinate.y <= brick_right_point.y):
                if LVEL1_BREAKABLE_BRICK[i] == 1:
                    LEVEL1_Y_BRICK.pop(i)
                    LEVEL1_X_BRICK.pop(i)
                    LVEL1_BREAKABLE_BRICK.pop(i)
                else:
                    if LVEL1_BREAKABLE_BRICK[i] < 7:
                        if LVEL1_BREAKABLE_BRICK[i] == 2:
                            # TODO  remove идиотското решение
                            LVEL1_BREAKABLE_BRICK.pop(i)
                            LVEL1_BREAKABLE_BRICK.insert(i, 1)
                        if LVEL1_BREAKABLE_BRICK[i] == 3:  # на проблема
                            LVEL1_BREAKABLE_BRICK.pop(i)
                            LVEL1_BREAKABLE_BRICK.insert(i, 2)
                        if LVEL1_BREAKABLE_BRICK[i] == 4:
                            LVEL1_BREAKABLE_BRICK.pop(i)
                            LVEL1_BREAKABLE_BRICK.insert(i, 3)
                        if LVEL1_BREAKABLE_BRICK[i] == 5:
                            LVEL1_BREAKABLE_BRICK.pop(i)
                            LVEL1_BREAKABLE_BRICK.insert(i, 4)
                        if LVEL1_BREAKABLE_BRICK[i] == 6:
                            LVEL1_BREAKABLE_BRICK.pop(i)
                            LVEL1_BREAKABLE_BRICK.insert(i, 5)
                        self.points += 1
                return True  # TODO: think about what happens if not goes here

    def draw_all(self, screen: pygame.Surface, pygame: pygame):
        color_brick = LIGHT_GREEN
        for i in range(LEVEL1_X_BRICK.__len__()):
            left_x = LEVEL1_X_BRICK[i]
            left_y = LEVEL1_Y_BRICK[i]
            _p = LVEL1_BREAKABLE_BRICK[i]
            if _p == 1:
                color_brick = LIGHT_GREEN
            elif _p == 2:
                color_brick = LIGHT_GREEN
            elif _p == 3:
                color_brick = GREEN
            elif _p == 4:
                color_brick = GREEN
            elif _p == 5:
                color_brick = DARK_GREEN
            elif _p == 6:
                color_brick = DARK_GREEN
            elif _p == 7:
                color_brick = WHITE
            pygame.draw.rect(screen, color_brick,
                             (left_x, left_y, self.offset_x, self.offset_y))


# Player control stick
class Player:
    def __init__(self, stick, ):
        pass

    def move_stick(self, screen: pygame.Surface):
        # remove hardcoded position
        x = game.my_pygame.mouse.get_pos()[0]
        if x > (RIGHT_WALL_X - STICK_LENGHT):
            x = (RIGHT_WALL_X - STICK_LENGHT)
        screen.blit(game.sick_img, (x, 550))
        return x

# global class


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

    def begin_update(self, screen: pygame.Surface):
        try:
            screen.fill((95, 222, 146, 0))
        except:
            return False
        else:
            return True

    def end_update(self, my_pygame: pygame):
        my_pygame.display.update()


game = Game()
brick = Brick()
ball = Ball()
ball2 = Ball()
ball3 = Ball()
ball3.move_up_right = True
ball3.color = PURPLE
ball2.color = BLUE
ball2.move_up_left = True
ball.move_down_right = True

clock = pygame.time.Clock()

while game.running:
    op = Text(brick.points)
    game.begin_update(game.screen)
    brick.draw_all(game.screen, game.my_pygame)
    for event in game.my_pygame.event.get():
        if event.type == game.my_pygame.QUIT:
            game.running = False
        if event.type == game.my_pygame.KEYDOWN:
            if event.key == game.my_pygame.K_q:
                game.running = False
            if event.key == game.my_pygame.K_z:
                ball2.kill()
                # ball3.kill()
            if event.key == game.my_pygame.K_x:
                ball.move_up_left = True
                ball2.move_up_right = True
            if event.key == game.my_pygame.K_c:
                ball.move_up_left = True
                #ball3.move_up_left = True
    ball2.move(game.screen)
    # ball3.move(game.screen)
    op.prnt_text(game.screen)
    ball.move(game.screen)
    if brick.remove_from_ball(game.get_ball()):
        brick.draw_all(game.screen, game.my_pygame)
    game.end_update(game.my_pygame)
    clock.tick(200)