from utils.solver import Solver
import re

class Day3(Solver):
    def part1(self, input_file: str = None) -> int:
        if input_file is None:
            input_file = self.input_file

        with open(input_file, 'r') as file:
            input_string = file.read()
            file.close()
        
        matches = re.finditer(r'mul\((\d+),(\d+)\)', input_string)
        return sum(
            int(match.group(1)) * int(match.group(2))
            for match in matches
        )


    def part2(self, input_file: str = None) -> int:
        if input_file is None:
            input_file = self.input_file

        with open(input_file, 'r') as file:
            input_string = file.read()
            file.close()
        
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
    solver = Day3("input03.txt")
    print(solver.part1())
    print(solver.part2())
