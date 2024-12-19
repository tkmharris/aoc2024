from utils.solver import Solver
from utils.input import read_input
from functools import cache


class Day19(Solver):
    def setup(self, lines: list[str]) -> tuple[list[str], list[str]]:
        towels = []
        patterns = []
        for index, line in enumerate(lines):
            match index:
                case 0:
                    towels.extend(line.split(', '))
                case 1:
                    continue
                case _:
                    patterns.append(line)
        return towels, patterns


    @read_input("lines")
    def part1(self, lines: list[str]) -> int:
        towels, patterns = self.setup(lines)

        @cache
        def possible_pattern(pattern: str) -> bool:
            if pattern in towels or pattern == '':
                return True
            
            for towel in towels:
                if pattern.startswith(towel) and possible_pattern(pattern[len(towel):]):
                    return True
            return False
        
        return sum(
            possible_pattern(pattern)
            for pattern in patterns
        )


    @read_input("lines")
    def part2(self, lines: list[str]) -> int:
        towels, patterns = self.setup(lines)

        @cache
        def possible_arrangements(pattern: str) -> int:
            arrangements = 0
            if pattern in towels:
                arrangements += 1
            
            for towel in towels:
                if not pattern.startswith(towel):
                    continue

                arrangements += possible_arrangements(pattern[len(towel):])
            
            return arrangements
        
        return sum(
            possible_arrangements(pattern)
            for pattern in patterns
        )
    

if __name__=="__main__":
    solver = Day19("input19.txt")
    print(solver.part1()) # type: ignore
    print(solver.part2()) # type: ignore