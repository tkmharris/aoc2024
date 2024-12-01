from collections import defaultdict

class Solver:
    def __init__(self, input_file="input01.txt"):
        self.input_file = input_file

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


if __name__=='__main__':
    solver = Solver()

    print(solver.part1())
    print(solver.part2())
