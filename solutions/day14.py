from utils.solver import Solver
from utils.input import read_input
from dataclasses import dataclass
from collections import defaultdict
from enum import Enum
from math import prod
import re


@dataclass
class Grid:
    width: int
    height: int

    class Quadrant(Enum):
        UPPER_LEFT = "upper_left"
        UPPER_RIGHT = "upper_right"
        LOWER_LEFT = "lower_left"
        LOWER_RIGHT = "lower_right"

@dataclass
class Robot:
    position_x: int
    position_y: int
    velocity_x: int
    velocity_y: int

    def move(self, steps: int, grid: Grid):
        self.position_x = (self.position_x + steps * self.velocity_x) % grid.width
        self.position_y = (self.position_y + steps * self.velocity_y) % grid.height


    def quadrant(self, grid: Grid) -> Grid.Quadrant | None:
        # increasing y coordinate moves robots "down" the grid 
        if self.position_x < grid.width // 2:
            if self.position_y < grid.height // 2:
                return Grid.Quadrant.UPPER_LEFT
            elif self.position_y > grid.height // 2:
                return Grid.Quadrant.LOWER_LEFT
        elif self.position_x > grid.width // 2:
            if self.position_y < grid.height // 2:
                return Grid.Quadrant.UPPER_RIGHT
            elif self.position_y > grid.height // 2:
                return Grid.Quadrant.LOWER_RIGHT


def show(grid: Grid, robots: list[Robot]):
    robots_by_square = defaultdict(int)
    for robot in robots:
        robots_by_square[(robot.position_x, robot.position_y)] += 1
    
    lines = []
    for j in range(grid.height):
        line = ''
        for i in range(grid.width):
            if robots_by_square[(i,j)]:
                line += "*"
            else:
                line += '.'
        lines.append(line)
    print('\n'.join(lines))


def chi_squared_test(
        actuals: list[int], 
        expecteds: list[int | float]
    ) -> bool:

    # No science to this, just pick a threshold high enough that paging through
    # configurations goes quickly without stopping at too many false positives.
    CHI_SQUARED_THRESHOLD = 50
    
    if len(actuals) != len(expecteds):
        raise ValueError("Actual values must be same length as expected")
    statistic = sum(
        (actual - expected)**2 / expected
        for actual, expected in zip(actuals, expecteds)
    )

    if statistic > CHI_SQUARED_THRESHOLD:
        return False
    
    return True


class Day14(Solver):
    def __init__(self, input_file, grid: Grid):
        super().__init__(input_file)
        self.grid = grid
    
    def get_robots(self, lines: list[str]) -> list[Robot]:
        return [
            Robot(*tuple(map(int, re.findall(r'(\d+|\-\d+)', line))))
            for line in lines
        ]


    @read_input("lines")
    def part1(self, lines: list[str]) -> int:
        robots = self.get_robots(lines)

        for robot in robots:
            robot.move(steps=100, grid=self.grid)

        robots_by_quadrant = defaultdict(list)
        for robot in robots:
            if quadrant := robot.quadrant(self.grid):
                robots_by_quadrant[quadrant].append(robot)

        return prod(
            len(robots) for _, robots in robots_by_quadrant.items()
        )


    @read_input("lines")
    def part2(self, lines: list[str]):
        robots = self.get_robots(lines)
        expected_count = len(robots) * (50 * 51) / (101 * 103)

        def get_next(initial=False) -> bool:
            if initial:
                input_string = 'Press Enter to begin search for Christmas tree or type "exit" to stop: '
            else:
                input_string = 'Press Enter to continue or type "exit" to stop: '
            user_input = input(input_string)
            if user_input.lower() == "exit":
                return False
            return True
        
        generation = 0
        get_next()
        while True:
            generation += 1
            for robot in robots:
                robot.move(steps=1, grid=self.grid)

            robots_by_quadrant = defaultdict(list)
            for robot in robots:
                if quadrant := robot.quadrant(self.grid):
                    robots_by_quadrant[quadrant].append(robot)
            
            actual_counts = [
                int(len(robots)) for _, robots in robots_by_quadrant.items()
            ]
            if not chi_squared_test(actual_counts, [expected_count] * 4):
                show(self.grid, robots)
                print(generation)
                if not get_next():
                    exit(0)
    

if __name__=="__main__":
    solver = Day14("input14.txt", grid=Grid(101, 103))
    print(solver.part1())
    print(solver.part2())