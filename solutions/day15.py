"""
NOTES:
Not entirely happy with this. 
For part 2 it should be possible to recursively move the 
boxes without having to do the check ahead that the move 
is possible, but this way seemed easiest and completes
quickly enough.
"""

from utils.solver import Solver
from utils.input import read_input
from utils.structures import Vector2D

Grid = dict[Vector2D, str]
DIRECTION_POINTERS = {
    # ^ and v look like they're the wrong way around but they're not:
    # the grid is y-indexed from top to bottom.
    '^': Vector2D(0, -1),
    '>': Vector2D(1, 0),
    'v': Vector2D(0, 1),
    '<': Vector2D(-1, 0),
}


NEIGHBOUR_DIRECTIONS = {
    '[': Vector2D(1, 0),
    ']': Vector2D(-1, 0),
}


def ahead(position: Vector2D, direction: str, steps: int = 1) -> Vector2D:
    unit_direction = DIRECTION_POINTERS[direction]
    return position + steps * unit_direction


def move(grid: Grid, position: Vector2D, instruction: str):
    if grid[ahead(position, instruction)] != '.':
        raise ValueError("Something is in the way")
    grid[ahead(position, instruction)] = grid[position]
    grid[position] = '.'


class Day15(Solver):
    def setup_part1(self, lines: list[str]) -> tuple[Grid, Vector2D, list[str]]:
        reading_instructions = False
        grid = {}
        instructions = []
        initial_position = None
        
        for y, line in enumerate(lines):
            if not line:
                reading_instructions = True
            
            if reading_instructions:
                instructions.extend(list(line))
            else:
                for x, symbol in enumerate(line):
                    grid[Vector2D(x, y)] = symbol
                    if symbol == '@':
                        initial_position = Vector2D(x, y)
        
        if initial_position is None:
            raise ValueError("Initial position not specified")

        return grid, initial_position, instructions
    

    def setup_part2(self, lines: list[str]) -> tuple[Grid, Vector2D, list[str]]:
        reading_instructions = False
        grid = {}
        instructions = []
        initial_position = None
        
        for y, line in enumerate(lines):
            if not line:
                reading_instructions = True
            
            if reading_instructions:
                instructions.extend(list(line))
            else:
                for x, symbol in enumerate(line):
                    match symbol:
                        case '#' | '.':
                            grid[Vector2D(2*x, y)] = symbol        
                            grid[Vector2D(2 * x + 1, y)] = symbol
                        case 'O':
                            grid[Vector2D(2 * x, y)] = '['        
                            grid[Vector2D(2 * x + 1, y)] = ']'
                        case '@':
                            grid[Vector2D(2 * x, y)] = '@'        
                            grid[Vector2D(2 * x + 1, y)] = '.'
                            initial_position = Vector2D(2 * x, y)
                        case _:
                            raise ValueError("Invalid map symbol")
        
        if initial_position is None:
            raise ValueError("Initial position not specified")

        return grid, initial_position, instructions

    
    @read_input("lines")
    def part1(self, lines: list[str]) -> int:
        grid, initial_position, instructions = self.setup_part1(lines)
        
        def boxes_to_push(position: Vector2D, instruction: str) -> int | None:
            next_item = grid[ahead(position, instruction)]
            if next_item == '.':
                return 0
            elif next_item == 'O':
                further_boxes = boxes_to_push(ahead(position, instruction), instruction)
                if further_boxes is not None:
                    return 1 + further_boxes
            return None
        
        position = initial_position
        for instruction in instructions:
            boxes = boxes_to_push(position, instruction)
            if boxes is None:
                continue

            if boxes > 0:
                grid[ahead(position, instruction, steps = boxes + 1)] = 'O'

            grid[position] = '.'
            position = ahead(position, instruction)
            grid[position] = '@'
        
        return sum(
            position.x + 100 * position.y
            for position, item in grid.items()
            if item == 'O'
        )
        

    @read_input("lines")
    def part2(self, lines: list[str]) -> int:
        grid, initial_position, instructions = self.setup_part2(lines)

        def can_move_horizontal(position: Vector2D, instruction: str) -> bool:
            next_item = grid[ahead(position, instruction)]
            match next_item:
                case '.':
                    return True
                case '#':
                    return False
                case '[' | ']':
                    return can_move_horizontal(
                        ahead(position, instruction, steps=2), 
                        instruction
                    )
                case _:
                    return False
        

        def can_move_vertical(position: Vector2D, instruction: str) -> bool:
            next_item = grid[ahead(position, instruction)]
            match next_item:
                case '.':
                    return True
                case '#':
                    return False
                case '[' | ']':
                    return can_move_vertical(
                        ahead(position, instruction), instruction
                    ) and can_move_vertical(
                        ahead(position + NEIGHBOUR_DIRECTIONS[next_item], instruction), 
                        instruction
                    )
                case _:
                    return False
        

        def move_horizontal(position: Vector2D, instruction: str):
            next_item = grid[ahead(position, instruction)]
            match next_item:
                case '.':
                    move(grid, position, instruction)
                    
                case '[' | ']':
                    move_horizontal(
                        ahead(position, instruction, steps=2),
                        instruction
                    )
                    move(grid, ahead(position, instruction), instruction)
                    move(grid, position, instruction)
                case _:
                    raise ValueError("This shouldn't happen")
        

        def move_vertical(position: Vector2D, instruction: str):
            next_item = grid[ahead(position, instruction)]
            match next_item:
                case '.':
                    grid[ahead(position, instruction)] = grid[position]
                    grid[position] = '.'
                case '[' | ']':
                    move_vertical(
                        ahead(position, instruction), instruction
                    )
                    move_vertical(
                        ahead(position + NEIGHBOUR_DIRECTIONS[next_item], instruction),
                        instruction
                    )
                    move(grid, position, instruction)
                case _:
                    raise ValueError("This shouldn't happen")
        

        position = initial_position
        for instruction in instructions:
            match instruction:
                case '<' | '>':
                    if can_move_horizontal(position, instruction):
                        move_horizontal(position, instruction)
                case '^' | 'v':
                    if can_move_vertical(position, instruction):
                        move_vertical(position, instruction)
                case _:
                    raise ValueError("This shouldn't happen")
            if grid[ahead(position, instruction)] == '@':
                position = ahead(position, instruction)
        return sum(
            position.x + 100 * position.y
            for position, item in grid.items()
            if item == '['
        )
    

if __name__=="__main__":
    solver = Day15("input15.txt")
    print(solver.part1()) # type: ignore
    print(solver.part2()) # type: ignore