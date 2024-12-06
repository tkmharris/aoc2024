from utils.solver import Solver
from utils.input import read_input
from dataclasses import dataclass

@dataclass
class Vector:
    x: int
    y: int

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __hash__(self):
        # overriding __eq__ forces us to override __hash__
        # if we want to hash
        return hash((self.x, self.y)) 

DIRECTION_POINTERS = {
    # ^ and v look like they're the wrong way around but they're not:
    # the grid is y-indexed from top to bottom.
    '^': Vector(0, -1),
    '>': Vector(1, 0),
    'v': Vector(0, 1),
    '<': Vector(-1, 0),
}

class Guard:
    def __init__(self, init_position, init_direction):
        self.init_position = init_position
        self.init_direction = init_direction
        self.position = init_position
        self.direction = init_direction

    def ahead(self):
        return self.position + self.direction
    
    def turn(self):
        if self.direction == Vector(0, -1):
            self.direction = Vector(1, 0)
        elif self.direction == Vector(1, 0):
            self.direction = Vector(0, 1)
        elif self.direction == Vector(0, 1):
            self.direction = Vector(-1, 0)
        elif self.direction == Vector(-1, 0):
            self.direction = Vector(0, -1)
    
    def step(self):
        self.position += self.direction

    def restore_initial_configuration(self):
        self.position = self.init_position
        self.direction = self.init_direction
    
    
class Day06(Solver):
    def setup_grid_guard(self, input_grid):
        grid = {
            Vector(x, y): input_grid[y][x]
            for x in range(len(input_grid[0])) 
            for y in range(len(input_grid))
        }

        for position, pointer in grid.items():
            if direction := DIRECTION_POINTERS.get(pointer, None):
                guard = Guard(position, direction)

        assert guard

        return grid, guard

    @read_input("grid")
    def part1(self, input_grid) -> int:
        grid, guard = self.setup_grid_guard(input_grid)

        visited = {guard.position}
        while next_location := grid.get(guard.ahead(), None):
            if next_location == '#':
                guard.turn()
            else:
                guard.step()
                visited.add(guard.position)
        return len(visited)


    @read_input("grid")
    def part2(self, input_grid) -> int:
        grid, guard = self.setup_grid_guard(input_grid)

        # get possible obstruction positions
        potential_obstructions = set()
        while next_location := grid.get(guard.ahead(), None):
            if next_location == '#':
                guard.turn()
            else:
                guard.step()
                potential_obstructions.add(guard.position)
        potential_obstructions.discard(guard.init_position)
        
        # Just try adding each loop obstruction and see if the 
        # guard escapes or enters a loop.
        loop_obstructions = 0
        for obstruction in potential_obstructions:
            adjusted_grid = grid.copy() | {obstruction: '#'}
            
            guard.restore_initial_configuration()
            seen_configurations = {(guard.position, guard.direction)}
            
            while next_location := adjusted_grid.get(guard.ahead(), None):
                if next_location == '#':
                    guard.turn()
                    seen_configurations.add((guard.position, guard.direction))
                else:
                    guard.step()
                    if (guard.position, guard.direction) in seen_configurations:
                        loop_obstructions += 1
                        break
                    
                    seen_configurations.add((guard.position, guard.direction))
        
        return loop_obstructions

if __name__=="__main__":
    solver = Day06("input06.txt")
    print(solver.part1())
    print(solver.part2())