from Level import Level
class BaseGameObject:

    def __init__(self):
        self.level = Level()
        self.level.load(self.level.current_level)
        

    pass
