"""
NOTES:
I don't really like the difference in approach between part 1 and part 2 here.
Part 2 was easier so my part 1 is probably a bad approach. Iterating over all
starting locations and looking for XMASs starting in each direction felt hacky
though.
"""

from utils.solver import Solver
from utils.input import read_input

class Day04(Solver):
    @read_input("grid")
    def part1(self, grid) -> int:
        # Assume input is rectangular
        assert all(len(row) == len(grid[0]) for row in grid)

        def count_xmas(lines):
            return sum(line.count('XMAS') for line in lines)
        
        def count_xmas_reverse(lines):
            return sum(line.count('SAMX') for line in lines)
        
        def count_horizontal(grid):
            lines = [''.join(row) for row in grid]
            return count_xmas(lines) + count_xmas_reverse(lines)
        
        def count_vertical(grid):
            vertical_lines = [''.join(list(column)) for column in zip(*grid)]
            return count_xmas(vertical_lines) + count_xmas_reverse(vertical_lines)
        
        def count_diagonal(grid):
            height = len(grid)
            width = len(grid[0])

            diagonal_lines = []
            for d in range(height + width - 1):
                diagonal_lines.append(
                    ''.join(
                        grid[i][d - i]
                        for i in range(max(0, d - width + 1), min(d + 1, height))
                    )
                )
            for d in range(height + width - 1):
                diagonal_lines.append(
                    ''.join(
                        grid[i][width - 1 - (d - i)]
                        for i in range(max(0, d - width + 1), min(d + 1, height))
                    )
                )
            return count_xmas(diagonal_lines) + count_xmas_reverse(diagonal_lines)
        
        return count_horizontal(grid) + count_vertical(grid) + count_diagonal(grid)


    @read_input("grid")
    def part2(self, grid) -> int:
        # Assume input is rectangular
        assert all(len(row) == len(grid[0]) for row in grid)
        
        height, width = len(grid), len(grid[0])
        
        count = 0
        for i in range(1, height - 1):
            for j in range(1, width - 1):

                if grid[i][j] != 'A':
                    continue
                
                if (
                    grid[i - 1][j - 1], 
                    grid[i - 1][j + 1], 
                    grid[i + 1][j - 1], 
                    grid[i + 1][j + 1]
                ) in [
                    ('M', 'M', 'S', 'S'),
                    ('M', 'S', 'M', 'S'),
                    ('S', 'S', 'M', 'M'),
                    ('S', 'M', 'S', 'M'),
                ]:
                    count += 1
        
        return count

if __name__=="__main__":
    solver = Day04("input04.txt")
    print(solver.part1())
    print(solver.part2())