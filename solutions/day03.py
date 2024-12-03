import re
from utils.solver import Solver
from utils.input import read_input

class Day03(Solver):
    @read_input(lines=False)
    def part1(self, input_string) -> int:
        matches = re.finditer(r'mul\((\d+),(\d+)\)', input_string)
        return sum(
            int(match.group(1)) * int(match.group(2))
            for match in matches
        )

    @read_input(lines=False)
    def part2(self, input_string) -> int:
        matches = re.finditer(r'do\(\)|don\'t\(\)|mul\((\d+),(\d+)\)', input_string)
        result = 0
        enabled = True
        
        for match in matches:
            if match.group(0) == "do()":
                enabled = True
            elif match.group(0) == "don't()":
                enabled = False
            elif enabled:
                result += int(match.group(1)) * int(match.group(2))
        
        return result

if __name__=="__main__":
    solver = Day03("input03.txt")
    print(solver.part1())
    print(solver.part2())
