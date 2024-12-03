from utils.solver import Solver

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

class Day2(Solver):
    def part1(self, input_file: str = None) -> int:
        if input_file is None:
            input_file = self.input_file

        safe_reports = 0
        with open(input_file, 'r') as file:
            for line in file:
                levels = list(map(int, line.strip().split()))
                if safe(levels):
                    safe_reports += 1

        return safe_reports


    def part2(self, input_file: str = None) -> int:
        if input_file is None:
            input_file = self.input_file
        
        def safe_with_dampener(levels):
            if safe(levels):
                return True
            
            return any(
                safe(levels[:i] + levels[i+1:])
                for i in range(len(levels))
            )

        safe_reports = 0
        with open(input_file, 'r') as file:
            for line in file:
                levels = list(map(int, line.strip().split()))
                if safe_with_dampener(levels):
                    safe_reports += 1
        
        return safe_reports

if __name__=="__main__":
    solver = Day2("input02.txt")
    print(solver.part1())
    print(solver.part2())
