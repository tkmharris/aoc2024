from utils.solver import Solver
from utils.input import read_input

def safe(levels: list[int]) -> bool:
    if levels == []:
        raise ValueError
    if len(levels) == 1:
        return True
    
    diffs = [levels[i+1] - levels[i] for i in range(0, len(levels) - 1)]
    safe_diffs = [1, 2, 3]

    return all(
        (diff in safe_diffs) for diff in diffs
    ) or all(
        (-diff in safe_diffs) for diff in diffs
    )

class Day02(Solver):
    @read_input(lines=True)
    def part1(self, lines) -> int:
        safe_reports = 0
        
        for line in lines:
            levels = list(map(int, line.strip().split()))
            if safe(levels):
                safe_reports += 1

        return safe_reports

    @read_input(lines=True)
    def part2(self, lines) -> int:
        def safe_with_dampener(levels):
            if safe(levels):
                return True
            
            return any(
                safe(levels[:i] + levels[i+1:])
                for i in range(len(levels))
            )

        safe_reports = 0
        for line in lines:
            levels = list(map(int, line.strip().split()))
            if safe_with_dampener(levels):
                safe_reports += 1
        
        return safe_reports

if __name__=="__main__":
    solver = Day02("input02.txt")
    print(solver.part1())
    print(solver.part2())
