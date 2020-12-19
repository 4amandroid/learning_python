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
            return level[level_number]
l = Level()
l: Level = l.Load(0)
print('----------------brick_break------------')
print(l.brick_break)
print('----------------brick_x------------')
print(l.brick_x)
print('----------------brick_y------------')
print(l.brick_y)
        
     

    



# Parse JSON into an object with attributes corresponding to dict keys.
# x = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
# print(x.name, x.hometown.name, x.hometown.id)