from ooppopcorn import game
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
