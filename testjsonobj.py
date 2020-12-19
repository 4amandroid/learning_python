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
            level = Level()
            level = json.loads(json_file.read(), object_hook=lambda d: SimpleNamespace(**d))
            # the problem is understanding the lambda expressions and what is SimpleNamespace, 
            # but isn't important at this stage. just assume as working blackbox
            return level[level_number]
        
        
l = Level()

# this is ugly shortcut for assigning all atributes at one line instead of one by one
# should be refactored later, not importatnt for now
l: Level = l.Load(0)
print('----------------brick_break------------')
print(l.brick_break)
print('----------------brick_x------------')
print(l.brick_x)
print('----------------brick_y------------')
print(l.brick_y)