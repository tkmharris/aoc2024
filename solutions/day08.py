from utils.solver import Solver
from utils.input import read_input
from utils.structures import Vector2D
from collections import defaultdict
import string
from itertools import combinations
from math import gcd
    
class Day08(Solver):
    @read_input("grid")
    def part1(self, input_grid) -> int: 
        grid = {
            Vector2D(x, y): input_grid[y][x]
            for x in range(len(input_grid[0])) 
            for y in range(len(input_grid))
        }
        antenna_locations = defaultdict(list)
        for vector, symbol in grid.items():
            if symbol.isalnum():
                antenna_locations[symbol].append(vector)

        antinodes = set()
        for symbol in list(string.ascii_letters + string.digits):
            for antenna1, antenna2 in combinations(antenna_locations[symbol], 2):
                diff = antenna2 - antenna1
                antinode1, antinode2 =  antenna1 - diff, antenna2 + diff
                
                if grid.get(antinode1, None):
                    antinodes.add(antinode1)
                if grid.get(antinode2, None):
                    antinodes.add(antinode2)
                    
        return len(antinodes)

    
    @read_input("grid")
    def part2(self, input_grid) -> int:
        grid = {
            Vector2D(x, y): input_grid[y][x]
            for x in range(len(input_grid[0])) 
            for y in range(len(input_grid))
        }
        antenna_locations = defaultdict(list)
        for vector, symbol in grid.items():
            if symbol.isalnum():
                antenna_locations[symbol].append(vector)

        antinodes = set()
        for symbol in list(string.ascii_letters + string.digits):
            for antenna1, antenna2 in combinations(antenna_locations[symbol], 2):
                diff = antenna2 - antenna1
                min_diff = Vector2D(
                    diff.x // gcd(diff.x, diff.y),
                    diff.y // gcd(diff.x, diff.y)
                )
                
                # all nodes in one direction along the line ...
                position = antenna1
                while grid.get(position, None):
                    antinodes.add(position)
                    position += min_diff
                
                # ... and in the other direction
                position = antenna1
                while grid.get(position, None):
                    antinodes.add(position)
                    position -= min_diff
                    
        return len(antinodes)


if __name__=="__main__":
    solver = Day08("input08.txt")
    print(solver.part1())
    print(solver.part2())