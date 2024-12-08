from utils.solver import Solver
from utils.input import read_input

def check(expected, inputs, operations):
    if len(operations) > len(inputs) - 1:
        return False, False
    
    result = inputs[0]
    for i in range(len(operations)):
        if operations[i] == '+':
            result += inputs[i + 1]
        elif operations[i] == '*':
            result *= inputs[i + 1]
        else:
            raise ValueError("unexpected operation")

    valid = (result <= expected)    
    exact = (result == expected) and (len(operations) == len(inputs) - 1)

    return valid, exact

def check_with_concat(expected, inputs, operations):
    if len(operations) > len(inputs) - 1:
        return False, False
    
    def concat(left, right):
        return int(f"{str(left)}{str(right)}")
    
    result = inputs[0]
    for i in range(len(operations)):
        if operations[i] == '+':
            result += inputs[i + 1]
        elif operations[i] == '*':
            result *= inputs[i + 1]
        elif operations[i] == '|':
            result = concat(result, inputs[i + 1])
        else:
            raise ValueError("unexpected operation")

    valid = (result <= expected)    
    exact = (result == expected) and (len(operations) == len(inputs) - 1)

    return valid, exact
    
class Day07(Solver):
    def get_expectations_and_inputs(self, lines):
        expectations = []
        inputs = []
        for line in lines:
            left, right = line.split(':')
            expectations.append(int(left))
            inputs.append([int(_) for _ in right.strip().split()])
        return expectations, inputs
    
    
    @read_input("lines")
    def part1(self, lines) -> int:
        expectations, inputs = self.get_expectations_and_inputs(lines)

        def is_solvable(expected, inputs):  
            stack = ['+', '*']
            while stack:
                operations = stack.pop()
                valid, exact = check(expected, inputs, operations)
                if exact:
                    return True
                elif valid:
                    stack.append(operations + '+')
                    stack.append(operations + '*')
            return False
        
        return sum(
            expectation
            for expectation, input in zip(expectations, inputs)
            if is_solvable(expectation, input)
        )
    
    @read_input("lines")
    def part2(self, lines) -> int:
        expectations, inputs = self.get_expectations_and_inputs(lines)

        def is_solvable(expected, inputs):  
            stack = ['+', '*', '|']
            while stack:
                operations = stack.pop()
                valid, exact = check_with_concat(expected, inputs, operations)
                if exact:
                    return True
                elif valid:
                    stack.append(operations + '+')
                    stack.append(operations + '*')
                    stack.append(operations + '|')
            return False
        
        return sum(
            expectation
            for expectation, input in zip(expectations, inputs)
            if is_solvable(expectation, input)
        )


    

if __name__=="__main__":
    solver = Day07("input07.txt")
    print(solver.part1())
    print(solver.part2())