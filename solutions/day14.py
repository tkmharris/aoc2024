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


def display(grid: Grid, robots: list[Robot]):
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


def variance(points: list[tuple[int, int]]) -> float:
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]

    x_bar = sum(xs) / len(xs)
    y_bar = sum(ys) / len(ys)

    return sum(
        (point[0] - x_bar)**2 + (point[1] - y_bar)**2
        for point in points
    ) / len(points)


class Day14(Solver):
    def __init__(self, input_file, grid: Grid):
        super().__init__(input_file)
        self.grid = grid
    

    def get_robots(self, lines: list[str]) -> list[Robot]:
        return [
            Robot(*tuple(map(int, re.findall(r'(\d+|\-\d+)', line))))
            for line in lines
        ]
    

    def move_robots(self, robots: list[Robot], steps=1):
        for robot in robots:
            robot.move(steps=steps, grid=self.grid)


    @read_input("lines")
    def part1(self, lines: list[str]) -> int:
        robots = self.get_robots(lines)

        self.move_robots(robots, steps=100)
        
        robots_by_quadrant = defaultdict(list)
        for robot in robots:
            if quadrant := robot.quadrant(self.grid):
                robots_by_quadrant[quadrant].append(robot)

        return prod(
            len(robots) for _, robots in robots_by_quadrant.items()
        )


    @read_input("lines")
    def part2(self, lines: list[str], show: bool = False):
        robots = self.get_robots(lines)
        
        def _get_robot_position_variance(robots: list[Robot]) -> float:
            return variance([
                (robot.position_x, robot.position_y)
                for robot in robots
            ])
        
        minimum_variance: float | None = None
        best_time: int = 0
        # velocities are constant so configuration repeats after at most
        # grid.width * grid.height iterations
        for seconds in range(self.grid.width * self.grid.height):
            robot_variance = _get_robot_position_variance(robots)
            
            if minimum_variance is None or robot_variance < minimum_variance:
                minimum_variance = robot_variance
                best_time = seconds
            
            self.move_robots(robots)
            
        if show:
            # robots are back in their initial configuration after
            # grid.width * grid.height steps
            self.move_robots(robots, steps=best_time)
            display(self.grid, robots)
        
        return best_time
    

if __name__=="__main__":
    solver = Day14("input14.txt", grid=Grid(101, 103))
    print(solver.part1()) # type: ignore
    print(solver.part2()) # type: ignore