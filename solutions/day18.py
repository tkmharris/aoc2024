"""
NOTES:
Dissatisfied with this. The problem seemed quite easy for this late
in the month. For the first part I used BFS to get the distance.
For the second part I thought before trying something clever I might
as well try the naive thing: iteratively update the graph and check
whether the BFS can complete at each step, halting when it can't. 
I thought that would run forever but to my surprise it returned the 
correct answer after about 20s.
"""

import re
from utils.solver import Solver
from utils.input import read_input
from utils.algorithms import bfs_distance
from utils.structures import Vector2D, UNIT_DIRECTIONS
from dataclasses import dataclass


@dataclass
class Grid:
    width: int
    height: int


class Day18(Solver):
    def setup(
        self, lines: list[str], grid: Grid, time: int
    ) -> dict[Vector2D, list[Vector2D]]:
        blocked = set()
        for line in lines[:time]:
            match = re.match(r'(\d+)\,(\d+)', line)
            x, y = int(match.group(1)), int(match.group(2))
            blocked.add(Vector2D(x, y))

        graph = {}
        for x in range(grid.height):
            for y in range(grid.height):
                if (vector := Vector2D(x, y)) not in blocked:        
                    graph[vector] = []

        for vector in graph.keys():
            for direction in UNIT_DIRECTIONS:
                neighbour = vector + direction
                if graph.get(neighbour) is not None:
                    graph[vector].append(neighbour)

        start = Vector2D(0, 0)
        end = Vector2D(grid.width - 1, grid.height - 1)

        assert(graph[start])
        assert(graph[end])

        return graph, start, end


    @read_input("lines")
    def part1(self, lines: list[str], grid: Grid, time: int) -> int:
        graph, start, end = self.setup(lines, grid, time)
        distance = bfs_distance(graph, start, end)
        return distance       


    @read_input("lines")
    def part2(self, lines: list[str], grid: Grid) -> str | None:
        graph, start, end = self.setup(lines, grid, 0)
        for line in lines:
            # update graph
            match = re.match(r'(\d+)\,(\d+)', line)
            x, y = int(match.group(1)), int(match.group(2))
            vector = Vector2D(x, y)
            del graph[vector]
            for direction in UNIT_DIRECTIONS:
                if graph.get(vector + direction) is not None:
                    graph[vector + direction].remove(vector)
            
            # check if we can reach the end
            if not bfs_distance(graph, start, end):
                return f"{x},{y}"
    

if __name__=="__main__":
    solver = Day18("input18.txt")
    print(solver.part1(grid=Grid(71, 71), time=1024)) # type: ignore
    print(solver.part2(grid=Grid(71, 71))) # type: ignore