import json
from types import SimpleNamespace

class Level():
    levels = ['level1', 'level2', 'level3', 'level4']
    def __init__(self):
        self.brick_x = []
        self.brick_y = []
        self.brick_break = []
        self.current_level = 0
        
    def load(self, level_number: int):
        """
        load level by number using self generated number from array
        """
        with open('data2.json') as json_file:
            # get arrays foreach object in json (all levels)
            levels_info = json.loads(json_file.read(), object_hook=lambda d: SimpleNamespace(**d))
            
            # get arrays for specific level
            level = levels_info[level_number]
            
            # extract an attite names from level collection (should be equivalent as a class attibutes)
            atribute_names = [a for a in dir(level) if not a.startswith('__') and not callable(getattr(level, a))]
            
            # foreach attribute
            for atribute_name in atribute_names:
  
                # here you may do some checks for equality between json file and level object
                # and throws exception in case they not equal 
                object.__setattr__(self, atribute_name, level.__dict__[atribute_name])
            pass
            
     
    def save(self):
        
        for i in self.levels: #don't works
            data = {}
            data[i] = [] #self.levels[self.curtent_level]
            data[i].append({
                'brick_x': self.brick_x, 
                'brick_y': self.brick_y,
                'brick_break': self.brick_break
            })
            with open('saved.json', 'w') as outfile:
                json.dump(data, outfile)
