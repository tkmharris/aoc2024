"""
NOTES:
This is horrible, both as a solution and as expressed in code. 
I can't be bothered to tidy it up now.
Part 1 is pretty good but I couldn't easily extend it to part 2
and ended up doing some horrible hacking shit counting internal
and external corners and the subtracting off the double-counted Xs.
Kill me. I'm convinced that the change in the number of sides as the 
region grows is a function only of whether each of the 8 immediate 
neighbours are already in the region, so the approach of part 1 
should be extendable so long as I can bear treating the 256 cases
separately. Perhaps I can write a script to write the code.
"""

from collections import deque
from dataclasses import dataclass, field
from utils.solver import Solver
from utils.input import read_input
from utils.structures import Vector2D

DIRECTIONS = [
    Vector2D(1, 0),
    Vector2D(0, 1),
    Vector2D(-1, 0),
    Vector2D(0, -1),
]

def neighbours(vector: Vector2D) -> list[Vector2D]:
    return [
        vector + direction
        for direction in DIRECTIONS
    ]

@dataclass
class Region:
    symbol: str
    area: int = 0
    perimeter: int = 0
    members: set[Vector2D] = field(default_factory=set)

    def add(self, square):
        if square in self.members:
            return

        self.members.add(square)
        self.area += 1

        # updating the perimeter is a little harder
        number_of_neighbours = len(
            set(neighbours(square)).intersection(self.members)
        )
        # this formula only holds when we're counting neighbours that are 
        # adjacent in one of the four cardinal directions
        self.perimeter += (4 - 2 * number_of_neighbours)

    def external_corners(self):
        corner_test_directions = [
            [DIRECTIONS[0], DIRECTIONS[1]],
            [DIRECTIONS[1], DIRECTIONS[2]],
            [DIRECTIONS[2], DIRECTIONS[3]],
            [DIRECTIONS[3], DIRECTIONS[0]],
        ]
        
        return sum(
            all(
                square + direction not in self.members
                for direction in test
            )
            for test in corner_test_directions
            for square in self.members
        )

    def internal_corners(self):
        corner_test_directions = [
            [DIRECTIONS[0], DIRECTIONS[1]],
            [DIRECTIONS[1], DIRECTIONS[2]],
            [DIRECTIONS[2], DIRECTIONS[3]],
            [DIRECTIONS[3], DIRECTIONS[0]],
        ]

        external_neighbours = set().union(
            *[neighbours(square) for square in self.members]
        ) - self.members

        return sum(
            all(
                square + direction in self.members
                for direction in test
            )
            for test in corner_test_directions
            for square in external_neighbours
        )
    
    def x_cross(self):
        corner_test_directions = [
            [DIRECTIONS[0], DIRECTIONS[1]],
            [DIRECTIONS[1], DIRECTIONS[2]],
            [DIRECTIONS[2], DIRECTIONS[3]],
            [DIRECTIONS[3], DIRECTIONS[0]],
        ]

        return sum(
            all(
                square + direction not in self.members
                for direction in test
            ) and (square + test[0] + test[1]) in self.members
            for test in corner_test_directions
            for square in self.members
        )

    
    def sides(self):
        # number of sides is numbers of corners
        return self.internal_corners() + self.external_corners() - self.x_cross()

    def fence_cost(self):
        return self.area * self.perimeter
    
    def fence_cost_discounted(self):
        return self.area * self.sides()


def find_regions(grid: dict[Vector2D, str]):
    regions: list[Region] = []
    region_identified = set()

    for square in grid:
        if square in region_identified:
            continue
        
        region = Region(symbol = grid[square])
        queue = deque([square])
        
        while queue:
            current_square = queue.popleft()
            region.add(current_square)
            region_identified.add(current_square)

            for neighbour in neighbours(current_square):
                if (
                    grid.get(neighbour) == region.symbol and
                    neighbour not in region_identified and
                    neighbour not in queue
                ):
                    queue.append(neighbour)
            
        regions.append(region)
    
    return regions


class Day12(Solver):
    @read_input("grid")
    def part1(self, input_grid: list[list[str]]) -> int: 
        grid = {
            Vector2D(x, y): input_grid[y][x]
            for x in range(len(input_grid[0])) 
            for y in range(len(input_grid))
        }
        regions = find_regions(grid)
        return sum(region.fence_cost() for region in regions)

    @read_input("grid")
    def part2(self, input_grid: list[list[str]]) -> int: 
        grid = {
            Vector2D(x, y): input_grid[y][x]
            for x in range(len(input_grid[0])) 
            for y in range(len(input_grid))
        }
        regions = find_regions(grid)
        return sum(region.fence_cost_discounted() for region in regions)

if __name__=="__main__":
    solver = Day12("input12.txt")
    print(solver.part1())
    print(solver.part2())