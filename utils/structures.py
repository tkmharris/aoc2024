from dataclasses import dataclass

@dataclass
class Vector2D:
    x: int
    y: int

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __hash__(self):
        # overriding __eq__ forces us to override __hash__
        # if we want to hash
        return hash((self.x, self.y)) 