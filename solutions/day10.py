"""
NOTES:
I had the flu when I wrote this crap. 
It can be made more tidy.
"""

from utils.solver import Solver
from utils.input import read_input
from utils.structures import Vector2D
from collections import defaultdict, deque

DIRECTIONS = [
    Vector2D(1, 0),
    Vector2D(-1, 0),
    Vector2D(0, 1),
    Vector2D(0, -1),
]
    
class Day10(Solver):
    @read_input("grid")
    def part1(self, input_grid: str) -> int: 
        grid = {
            Vector2D(x, y): int(input_grid[y][x])
            for x in range(len(input_grid[0])) 
            for y in range(len(input_grid))
        }

        graph = {}
        for vector, elevation in grid.items():
            graph[vector] = [
                vector + direction
                for direction in DIRECTIONS
                if grid.get(vector + direction, -1) == elevation + 1
            ]

        queue = deque([
            vector for vector, elevation in grid.items()
            if elevation == 0
        ])
        accessible_from = defaultdict(set)
        for vector in queue:
            accessible_from[vector] = set([vector])
        while queue:
            vector = queue.popleft()
            for neighbour in graph[vector]:
                accessible_from[neighbour].update(accessible_from[vector])
                queue.append(neighbour)
        
        result = 0
        for vector, elevation in grid.items():
            if elevation == 9:
                result += len(accessible_from[vector])

        return result


    @read_input("grid")
    def part2(self, input_grid: str) -> int: 
        grid = {
            Vector2D(x, y): int(input_grid[y][x])
            for x in range(len(input_grid[0])) 
            for y in range(len(input_grid))
        }

        graph = {}
        for vector, elevation in grid.items():
            graph[vector] = [
                vector + direction
                for direction in DIRECTIONS
                if grid.get(vector + direction, -1) == elevation + 1
            ]

        queue = deque([
            vector for vector, elevation in grid.items()
            if elevation == 0
        ])
        distinct_paths = defaultdict(set)
        for vector in queue:
            distinct_paths[vector] = set([f"{vector.x}|{vector.y}|"])
        while queue:
            vector = queue.popleft()
            for neighbour in graph[vector]:
                paths = [
                    path + f"{neighbour.x}|{neighbour.y}|"
                    for path in distinct_paths[vector]
                ]
                distinct_paths[neighbour].update(paths)
                queue.append(neighbour)
        
        result = 0
        for vector, elevation in grid.items():
            if elevation == 9:
                result += len(distinct_paths[vector])

        return result


if __name__=="__main__":
    solver = Day10("input10.txt")
    print(solver.part1())
    print(solver.part2())