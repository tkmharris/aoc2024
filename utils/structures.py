from dataclasses import dataclass

@dataclass
class Vector2D:
    x: int
    y: int

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __rmul__(self, number):
        return Vector2D(self.x * number, self.y * number)
    
    def __eq__(self, other):
        return isinstance(other, Vector2D) and (self.x == other.x) and (self.y == other.y)

    def __hash__(self):
        # overriding __eq__ forces us to override __hash__
        # if we want to hash
        return hash((self.x, self.y))


UNIT_DIRECTIONS = [
    Vector2D(1, 0),
    Vector2D(-1, 0),
    Vector2D(0, 1),
    Vector2D(0, -1),
]
