from typing import Tuple
class Coordinate:
    """
    Represents coordinate id 2d surface
    
    x: int = 0
    y: int = 0
    
    Tuple[int, int] = (0, 0)
    """
    x: int = 0
    y: int = 0
    
    def __init__(self, x: int = 0, y: int = 0, coordinates: Tuple[int, int] = (0, 0)):
        
        if coordinates == (0, 0):
            self.x: int = x
            self.y: int = y
        else:
            self.x, self.y = coordinates
        
