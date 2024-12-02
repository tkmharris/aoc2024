from collections import defaultdict
from utils.solver import Solver

class Day1(Solver):
    """
    NOTES:
    After doing the obvious thing I re-implemented part 1 using a pair
    of heaps to avoid another pass through the input to sort, but a 
    benchmark revealed the input isn't big enough for the savings to 
    cancel out the heap overheads.
    """

    def part1(self, input_file=None):
        if input_file is None:
            input_file = self.input_file

        left_column = []
        right_column = []
        with open(input_file, 'r') as file:
            for line in file:
                left, right = map(int, line.strip().split())
                left_column.append(left)
                right_column.append(right)

        left_column.sort()
        right_column.sort()

        return sum(
            abs(left - right)
            for left, right in zip(left_column, right_column)
        )


    def part2(self, input_file=None):
        if input_file is None:
            input_file = self.input_file

        left_column = []
        right_column = defaultdict(int)

        with open(input_file, 'r') as file:
            for line in file:
                left, right = map(int, line.strip().split())
                left_column.append(left)
                right_column[right] += 1

        return sum(
            left * right_column[left]
            for left in left_column
        )

if __name__=="__main__":
    solver = Day1("input01.txt")
    print(solver.part1())
    print(solver.part2())
