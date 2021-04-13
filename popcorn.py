import pygame
from pygame.sprite import Group
from pygame.time import Clock
from Config import *
from Level import Level
from BaseGameObject import BaseGameObject, Border,Ball,Brick
from Brick import Brick
from Stick import Stick, Luck
from CollisionInfo import CollisionInfo

class Game(BaseGameObject):
    def __init__(self):
        super().__init__()
        self.clock = Clock()
        self.__initializeGraphics(SCREEN_WIDTH, SCREEN_HEIGHT)
        # create instances of core game objects
        self.level = Level()
        self.border = Border()
        self.border.initializeBorderFrame()
        self.ball = Ball()
        self.ball.initializeBalls(DEFAULT_NUMBER_OF_BALLS)
        self.stick = Stick(self.screen)
        #self.luck = Luck()
        self.all_lucks = Group()
        self.points = 0
        self.points_per_brick = POINTS_PER_BRICK
        # initialize core game objects
        #self.__initializeBorderFrame()
         
        #self.__initStick()
        self.lives = DEFAULT_NUMBER_OF_LIVES
        self.tolerance = COLISION_TOLERANCE
        self.collisionInfo = None
    
    #def __initStick(self) -> None:
    #DONE    # това трябва да се промени навсякъде - ще работим само с един стик за сега
    #    self.all_sticks = Group()
    #    self.all_sticks.add(self.stick)
            
    def __initializeGraphics(self, screen_width: int, screen_height: int) -> None:
            pygame.init()
            pygame.mixer.init()
            self.screen = pygame.display.set_mode((screen_width, screen_height))
            self.brick_screen = pygame.display.set_mode((screen_width, screen_height))
            pygame.display.set_caption("My Game")
            self.font = pygame.font.SysFont(None, FONT_SIZE)

    # това трябва да се изнесе в отделен клас
    def printItemBar(self, points: int = 0) -> None:
        self.points = points
        #DONE използвай този метод за билдване на стринг https://docs.python.org/3.6/whatsnew/3.6.html#whatsnew36-pep498
        bar_text = f"POINTS {self.points} LIVES {self.lives} LEVEL  {self.level.current_level+1}"
        if self.lives == 0 and len(self.all_balls) == 0:
            bar_text = 'G A M E   O V E R'
            self.font = pygame.font.SysFont(None, FONT_SIZE*4)
        self.text = self.font.render( bar_text, True, COLOR_GREEN, COLOR_RED)
        self.textRect = self.text.get_rect()
        self.textRect.midtop = (SCREEN_WIDTH//2,UP_WALL_Y)
        self.screen.blit(self.text,self.textRect)      
       
    
        
    def ballCollideDetect(self):    
        for visual_object in self.all_visual_objects:
            for ball in self.ball.all_balls:
                if ball.rect.bottom >= SCREEN_HEIGHT:
                    ball.kill()
                if ball.rect.colliderect(visual_object.rect): 
                    return CollisionInfo(ball, visual_object)
    def ballPeelOff(self) -> None:
        for ball in self.ball.all_balls:
            if ball.glued: 
                ball.glued = False
                ball.rect.x += COLISION_TOLERANCE 
                ball.rect.y -= COLISION_TOLERANCE
                ball.x_speed = BALL_X_SPEED * ball.correct_glue_direction
                ball.y_speed = BALL_Y_SPEED

    def collisionReaction(self) -> None:
        self.points += self.points_per_brick
        if self.collisionInfo.visual_object.brick_hardness == min(self.level.brick_break):    
            self.collisionInfo.visual_object.kill()
            if len(self.level.all_bricks) == self.level.number_of_unbreakable_bricks:
                self.level.current_level += 1
                self.level.loadCurrentLevel()
                self.getAllVisualObjects()
        else:
            if self.collisionInfo.visual_object.brick_hardness < max(self.level.brick_break):
                self.collisionInfo.visual_object.brick_hardness -= 1
                lucks = Luck(self.collisionInfo.visual_object.rect.midbottom)
                if lucks.number in range(len(lucks.images)):
                    self.all_lucks.add(lucks)
        self.collisionInfo.visual_object.paint(self.collisionInfo.visual_object.brick_hardness)
        
game = Game()
game.level.loadCurrentLevel()               
game.getAllVisualObjects()

running = True
# Game loop
while running:
     
    game.clock.tick(FPS)
     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            #DONE нов метод за това с лепилото
            game.ballPeelOff()
            
            if game.stick.shoot:
                
                pygame.mixer.Sound.play(pygame.mixer.Sound('dum.wav'))  
                bullet =  game.stick.shot();
    
    game.collisionInfo = game.ballCollideDetect()  # type: ignore
    
    #DONE 2-те метода които са bulletCollideDetect и luckCollideDetect трябва да са в базовия клас
    if len(game.stick.bullets) > 0:
        game.bulletCollideDetect(game.level.all_bricks ,game.stick.bullets)
    game.luckCollideDetect(game.stick ,game.all_lucks)
       
    if game.collisionInfo is not None:
        # нов метод в базовия клас който се казва changeDirection, от него трябва да се извади логиката която не е за смяна на посоката
        # смяна на нивово, точки, kill, смяна на hardness, късмети
        # DONE тези неща трябва да се напишат в метод който се казва collisionReaction
        
        game.changeDirection(game.collisionInfo.ball, game.collisionInfo.visual_object)
        if isinstance(game.collisionInfo.visual_object, Brick):
            game.collisionReaction()
            
    # нов метод в game
    if len(game.ball.all_balls) == 0:
        if game.lives > 0:
            game.lives -= 1
            game.ball.initializeBalls(DEFAULT_NUMBER_OF_BALLS)
             
    # Draw / render
    game.screen.fill(COLOR_BLACK)
    game.all_visual_objects.draw(game.brick_screen)
    
    game.ball.all_balls.draw(game.screen)
    game.ball.all_balls.update(game.stick.rect.x)
    game.stick.update()
    game.all_lucks.draw(game.screen)
    game.all_lucks.update()
    game.printItemBar(game.points)
 
    pygame.display.flip()

pygame.quit()
