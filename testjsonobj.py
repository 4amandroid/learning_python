import json
from types import SimpleNamespace

class Level:
    brick_y = []
    brick_break = []
    brick_x = []

    def Load(self, level_number: int):
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
                # set value for self instance and attibute by name
                # remove this nosence when find a better way to do this :), it works
                # here you may do some checks for equality between json file and level object
                # and throws exception in case they not equal 
                object.__setattr__(self, atribute_name, level.__dict__[atribute_name])
            pass
        
        
l = Level()
l.Load(0)

print('----------------brick_break------------')
print(l.brick_break)
print('----------------brick_x------------')
print(l.brick_x)
print('----------------brick_y------------')
print(l.brick_y)