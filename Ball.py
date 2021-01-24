import pygame
from Config import *
from Coordinate import Coordinate 
from Stick import Stick
class Ball:
    def __init__(self,level_brick_x =[],level_brick_y = []):
        self.level_brick_x = level_brick_x
        self.level_brick_y = level_brick_y
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
        self.color = COLOR_RED

    def kill(self):
        self.move_down_right = False
        self.move_down_left = False
        self.move_up_right = False
        self.move_up_left = False

    def move(self, screen: pygame.Surface):
        stick_left_point = Coordinate()
        stick_left_point.x = Stick.move(screen)
        brick_left_point = Coordinate()
        brick_right_point = Coordinate()

        if (self.ball_x > stick_left_point.x) and (self.ball_x < (stick_left_point.x+STICK_LENGHT)):
            if (self.ball_y + self.ball_radius) == STICK_Y_POSITION:  # TODO: Replace number with const
                if self.move_down_right:
                    self.move_down_right = False
                    self.move_up_right = True
                if self.move_down_left:
                    self.move_down_left = False  # TODO blow y wall of stick change direction
                    self.move_up_left = True

        for i in range(self.level_brick_x.__len__()):
            brick_left_point.x = int(self.level_brick_x[i])
            # Brick_offset_x & Y must be taken from
            brick_left_point.y = int(self.level_brick_y[i])
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
