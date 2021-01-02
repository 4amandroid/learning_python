from enum import Enum
class Collision_info(Enum):
    
    up_left = False
    up_right = False
    down_left = False
    down_right = False

print(Collision_info.up_left.value)     