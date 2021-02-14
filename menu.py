import pygame
import pygame_menu

pygame.init()
surface = pygame.display.set_mode((600, 400))
 

'''def set_difficulty(value, difficulty):
    # Do the job here !
    pass

def start_the_game():
    # Do the job here !
    exec(open('popcorn.py').read())
    pass

menu = pygame_menu.Menu(300, 400, 'Welcome',
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add_text_input('Name :', default='John Doe')
menu.add_selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add_button('Play', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface)'''
class Menu():
     
        

    
    def show(self):
         
        def set_difficulty(value, difficulty):
            #print('# Do the job here !')
            pass

        def start_the_game():
            # Do the job here !
            #exec(open('popcorn.py').read())
            pass
        self.menu = pygame_menu.Menu(300, 400, 'Welcome',
                       theme=pygame_menu.themes.THEME_BLUE)
        self.menu.add_text_input('Name :', default='John Doe')
        self.menu.add_selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
        self.menu.add_button('Play', start_the_game)
        self.menu.add_button('Quit', pygame_menu.events.EXIT)
        self.menu.mainloop(surface) 

#menu = Menu() 
#menu.show()      