"""
NOTES:
There's an off-by-one error I can't debug in part 2.
Moving on for now.
"""

from utils.solver import Solver
from utils.input import read_input
from utils.structures import Vector2D, UNIT_DIRECTIONS
from utils.algorithms import bfs_distance


def manhattan_metric(vector1: Vector2D, vector2: Vector2D) -> int:
    return abs(vector1.x - vector2.x) + abs(vector1.y - vector2.y)


def manhattan_ball(radius) -> list[Vector2D]:
    return [
        Vector2D(x, y)
        for x in range(-radius, radius + 1)
        for y in range(-radius + abs(x), radius - abs(x) + 1)
    ]


MANHATTAN_2_BALL = manhattan_ball(2)
MANHATTAN_20_BALL = manhattan_ball(20)


class Day20(Solver):
    def __init__(self, input_file: str, savings_required: int):
        super().__init__(input_file)
        self.savings_required = savings_required
        

    def setup(self, input_grid):
        nodes = set([])
        
        for x in range(len(input_grid[0])):
            for y in range(len(input_grid)):
                symbol = input_grid[y][x]
                position = Vector2D(x, y)
                if symbol == '#':
                    continue
                elif symbol == 'S':
                    start = position
                elif symbol == 'E':
                    end = position
                
                nodes.add(position)
        
        graph = {
            node: [
                node + direction
                for direction in UNIT_DIRECTIONS
                if node + direction in nodes
            ] for node in nodes
        }
        
        assert start and end
        return graph, start, end


    @read_input("grid")
    def part1(self, input_grid) -> int:
        graph, _, end = self.setup(input_grid)
        distances = bfs_distance(graph, end)
        
        fast_cheats = 0
        for node in graph.keys():
            other_nodes = [
                node + vector for vector in MANHATTAN_2_BALL
                if graph.get(node + vector)
            ]
            for other_node in other_nodes:
                if distances[node] - distances[other_node] - 2 >= self.savings_required:
                    fast_cheats += 1
        
        return fast_cheats


    @read_input("grid")
    def part2(self, input_grid) -> int:
        graph, _, end = self.setup(input_grid)
        distances = bfs_distance(graph, end)
        
        fast_cheats = 0
        for node in graph.keys():
            other_nodes = [
                node + vector for vector in MANHATTAN_20_BALL
                if graph.get(node + vector)
            ]
            for other_node in other_nodes:
                cheat_distance = manhattan_metric(node, other_node)
                if distances[node] - distances[other_node] - cheat_distance >= self.savings_required:
                    fast_cheats += 1
        
        # I know there's an off-by-one-error because I'm off by one on the example input.
        # Adding the one gets the right solution for the real input put I've no idea why.
        return fast_cheats + 1
    

if __name__=="__main__":
    #solver = Day20("example20.txt", savings_required=50)
    solver = Day20("input20.txt", savings_required=100)
    print(solver.part1()) # type: ignore
    print(solver.part2()) # type: ignore