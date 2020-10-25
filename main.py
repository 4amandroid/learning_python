#fist change

import pygame

pygame.init()

screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("The snake")
icon = pygame.image.load("C:\\Users\\hrisi\\Desktop\\popcorn\\greenbar.png")
pygame.display.set_icon(icon)

playerImg = pygame.image.load("C:\\Users\\hrisi\\Desktop\\popcorn\\greenbar.png")

class MooveCoor:
    def __init__(self, koorx=130, koory=130, radius=20, stepx=0.1, stepy=0.1,
                 move_down_left=True, move_down_right=False,
                 move_up_left=False, move_up_right=False, object_blowed=False,
                 x_position=300, y_position=550, accelerate=0, gaming=True):
        self.gaming = gaming
        self.accelerate = accelerate
        self.x_position = x_position
        self.y_position = y_position
        self.object_blowed = object_blowed
        self.stepx = stepx
        self.stepy = stepy
        self.radius = radius
        self.koorx = koorx
        self.koory = koory
        self.move_down_left = move_down_left
        self.move_down_right = move_down_right
        self.move_up_left = move_up_left
        self.move_up_right = move_up_right
    def get_data(self):
        if self.move_down_left:
            if self.koorx <= 0:
                self.move_down_left = False
                self.move_down_right = True
            if self.koory >= 600:
                self.move_down_left = False
                self.move_up_left = True
            self.koory += self.stepx
            self.koorx += -self.stepy
        elif self.move_up_left:
            if self.koory <= 0:
                self.move_up_left = False
                self.move_down_left = True
            if self.koorx <= 0:
                self.move_up_left = False
                self.move_up_right = True
            self.koorx += -self.stepx
            self.koory += -self.stepy
        elif self.move_down_right:
            if self.koorx >= 1000:
                self.move_down_right = False
                self.move_down_left = True
            if self.koory >= 600:
                self.move_down_right = False
                self.move_up_right = True
            self.koorx += self.stepx
            self.koory += self.stepy
        elif self.move_up_right:
            if self.koory <= 0:
                self.move_up_right = False
                self.move_down_right = True
            if self.koorx >= 1000:
                self.move_up_right = False
                self.move_up_left = True
            self.koorx += self.stepx
            self.koory += -self.stepy
        '''if self.koorx > self.x_position and self.koorx < self.x_position + 107 and self.koory > 550:
            self.object_blowed = True
            print(self.object_blowed)
            print(self.koory)
        else:
            self.object_blowed = False
            print(self.object_blowed)
            print(self.koory) '''

        pygame.draw.circle(screen, (190, 116, 130), (int(self.koorx), int(self.koory)), self.radius)
    def move_bar(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.QUIT:
                    self.gaming = False
                if event.key == pygame.K_q:
                    self.gaming = False
                if event.key == pygame.K_LEFT:
                    self.accelerate += -0.3
                if event.key == pygame.K_RIGHT:
                    self.accelerate += 0.3
            #if event.type == pygame.KEYUP:
            #    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            #        self.accelerate += 0
        self.x_position += self.accelerate
        if self.x_position < 0:
            self.accelerate = 0
            self.x_position = 1
        if self.x_position > 930:
            self.accelerate = 0
            self.x_position = 930

        screen.blit(playerImg, (int(self.x_position), int(self.y_position)))

    def ball_blowed_on_bar(self):

        if self.koorx - self.radius > self.x_position \
                and self.koorx < self.x_position + 107 and self.koory > 550 - self.radius:
            self.object_blowed = True
            #print(bar.object_blowed)
            #print(bar.koorx, bar.koory)
            #print(ball1.koorx, ball1.koory)
        else:
            self.object_blowed = False
            # print(bar.object_blowed)
            # print(bar.koorx, bar.koory)
            # print(ball1.koorx, ball1.koory)
        if self.object_blowed:
            if self.move_down_left:
                self.move_down_left = False
                self.move_up_left = True
                self.object_blowed = False
            if self.move_down_right:
                self.move_down_right = False
                self.object_blowed = False
                self.move_up_right = True

bar = MooveCoor()
ball1 = MooveCoor()
ball1.radius = 25
ball1.stepx = 0.1
ball1.stepy = 0.1
ball2 = MooveCoor(100, 100)
ball2.stepx = 0.1
ball2.stepy = 0.1
ball2.move_down_left = False
ball2.move_up_right = True
ball3 = MooveCoor(150, 200)
ball3.radius = 15
ball3.move_down_left = False
ball3.move_down_right = True
ball4 = MooveCoor()

balls = []

balls.append(ball4)

# some shit code
#more code

#pri natiskane na quit krai ili game over later

def not_game_over(gaming = True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gaming = False
    return gaming

while bar.gaming:
    screen.fill((95, 222, 146))

    bar.move_bar()
    ball2.ball_blowed_on_bar()
    for _ball in balls:
        if _ball.koorx - _ball.radius > bar.x_position \
                and _ball.koorx < bar.x_position + 107 and _ball.koory > 550 - _ball.radius:
            bar.object_blowed = True
            print(bar.object_blowed)
            print(bar.koorx, bar.koory)
            print(_ball.koorx, _ball.koory)
        else:
            bar.object_blowed = False
            #print(bar.object_blowed)
            #print(bar.koorx, bar.koory)
            #print(_ball.koorx, _ball.koory)
        if bar.object_blowed:
            if _ball.move_down_left:
                _ball.move_down_left = False
                _ball.move_up_left = True
                bar.object_blowed = False
            if _ball.move_down_right:
                _ball.move_down_right = False
                bar.object_blowed = False
                _ball.move_up_right = True


    if ball1.koory < 600:
        ball1.get_data()

    ball2.get_data()
    ball2.ball_blowed_on_bar()
    ball3.get_data()
    ball4.get_data()

    pygame.display.update()
