from utils.algorithms import dijkstra
from utils.solver import Solver
from utils.input import read_input
from utils.structures import Vector2D
from enum import Enum
from collections import defaultdict
from itertools import product

class UnitDirection(Enum):
    NORTH = Vector2D(0, 1)
    EAST = Vector2D(1, 0)
    SOUTH = Vector2D(0, -1)
    WEST = Vector2D(-1, 0)


MazeNode = tuple[Vector2D, UnitDirection]
Maze = dict[MazeNode, dict[MazeNode, int]]


def turns(
    direction: UnitDirection, 
    other_direction: UnitDirection
) -> int:
    if direction.value == other_direction.value:
        return 0
    elif direction.value == -1 * other_direction.value:
        return 2
    else:
        return 1


class Day16(Solver):
    def setup_maze(
            self, input_grid: list[list[str]]
    ) -> tuple[Maze, MazeNode, MazeNode]:
        grid = {
            Vector2D(x, y): input_grid[y][x]
            for x in range(len(input_grid[0])) 
            for y in range(len(input_grid))
        }
        maze, start, end = defaultdict(dict), None, None
        
        for position, char in grid.items():
            if char == "#":
                    continue
            elif char in ['.', 'S', 'E']:
                for facing_direction, neighbour_direction in product(UnitDirection, UnitDirection):
                    if grid[position + neighbour_direction.value] not in ['.', 'S', 'E']:
                        continue
                    
                    node = (position, facing_direction)    
                    other_node = (position + neighbour_direction.value, neighbour_direction)
                    distance = 1000 * turns(facing_direction, neighbour_direction) + 1
                    maze[node][other_node] = distance
                    maze[other_node][node] = distance

                if char == 'S':
                    # We start facing East
                    start = (position, UnitDirection.EAST)
                elif char == 'E':
                    # it doesn't actually matter what direction we're facing
                    # when we reach the end; we'll handle this by adding some
                    # zero distances.
                    end = (position, UnitDirection.EAST)
                    maze[(position, UnitDirection.NORTH)][position, UnitDirection.EAST] = 0
                    maze[(position, UnitDirection.EAST)][position, UnitDirection.SOUTH] = 0
                    maze[(position, UnitDirection.SOUTH)][position, UnitDirection.WEST] = 0
                    maze[(position, UnitDirection.WEST)][position, UnitDirection.NORTH] = 0
            else:
                raise ValueError("Unexpected character in input")

        assert start
        assert end

        return maze, start, end

    @read_input("grid")
    def part1(self, input_grid: list[list[str]]) -> int:
        maze, start, end = self.setup_maze(input_grid)
        distances = dijkstra(maze, end)
        return distances[start]


    @read_input("lines")
    def part2(self, input_grid: list[list[str]]) -> int:
        maze, start, end = self.setup_maze(input_grid)
        
        # Tiles on an optimal path are those for whom the distance from 
        # the start to the tile plus the distance from the end to the 
        # tile equals the length of the optimal path.
        distances_from_start = dijkstra(maze, start)
        distances_from_end = dijkstra(maze, end)
        tiles_on_a_best_path = set([
            node[0] for node in maze
            if distances_from_start[node] + distances_from_end[node] == distances_from_start[end]
        ])
        
        return len(tiles_on_a_best_path)
    

if __name__=="__main__":
    solver = Day16("input16.txt")
    print(solver.part1()) # type: ignore
    print(solver.part2()) # type: ignore