from utils.solver import Solver

class Day2(Solver):
    def part1(self, input_file=None):
        if input_file is None:
            input_file = self.input_file

        def safe(ints):
            if ints == []:
                raise ValueError
            if len(ints) == 1:
                return True
            
            diffs = [ints[i+1] - ints[i] for i in range(0, len(ints) - 1)]
            safe_diffs = [1, 2, 3]

            return all(
                (diff in safe_diffs) for diff in diffs
            ) or all(
                (-diff in safe_diffs) for diff in diffs
            )

        safe_reports = 0
        with open(input_file, 'r') as file:
            for line in file:
                levels = list(map(int, line.strip().split()))
                if safe(levels):
                    safe_reports += 1

        return safe_reports


    def part2(self, input_file=None):
        if input_file is None:
            input_file = self.input_file

        def safe_no_alterations(ints):
            if ints == []:
                raise ValueError
            if len(ints) == 1:
                return True
            
            diffs = [ints[i+1] - ints[i] for i in range(0, len(ints) - 1)]
            safe_diffs = [1, 2, 3]

            all_small_increase = all((diff in safe_diffs) for diff in diffs)
            all_small_decrease = all((-diff in safe_diffs) for diff in diffs)

            return all_small_increase or all_small_decrease
        
        def safe(ints):
            if safe_no_alterations(ints):
                return True
            
            return any(
                safe_no_alterations(ints[:i] + ints[i+1:])
                for i in range(len(ints))
            )

        safe_reports = 0
        with open(input_file, 'r') as file:
            for line in file:
                levels = list(map(int, line.strip().split()))
                if safe(levels):
                    safe_reports += 1
        
        return safe_reports

if __name__=="__main__":
    solver = Day2("input02.txt")
    print(solver.part1())
    print(solver.part2())
