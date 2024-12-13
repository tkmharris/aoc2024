"""
NOTES:
I thought I was going to enjoy this one by doing some elementary number theory
to get all the integral solutions for each equation in the desired range and then
checking for matches and finding the minimum cost (indeed this works for part 1).
It didn't occur to me that all the matrices defining the sets of simultaneous
equations would be invertible -- it seemed too easy. But after failing for a while
to narrow down the range enough for my original approach to work in part 2, I checked
the determinants on a hunch: they're all invertible. So you just have to invert the 
matrices and check for positive integrality, which is a doddle. I did it "by hand"
at least instead of using numpy.linalg as I'm trying not to go beyond the standard
library.
"""

from utils.solver import Solver
from utils.input import read_input
import re

def cost(A: int, B: int) -> int:
    return 3 * A + B


def is_nonnegative_integral(number: float, epsilon: float = 1e-9) -> bool:
    return abs(number - round(number, 0)) < epsilon and number > -epsilon


def solve_simultaneous_equations(
        a_x: int, b_x: int, prize_x: int, # represents a_x * A + b_x * B = prize_x
        a_y: int, b_y: int, prize_y: int  # represents a_y * A + b_y * B = prize_y
) -> tuple[float, float]:
    det = a_x * b_y - a_y * b_x
    # Luckily for us, all the equations in the input have unique solutions.
    assert(det) != 0

    # formula falls out of the equations after inverting the 2x2 matrix
    solution = (
        (b_y * prize_x - b_x * prize_y) / det,
        (a_x * prize_y - a_y * prize_x) / det
    )
    return solution


class Day13(Solver):
    def parse_input_lines(self, lines: list[str]) -> list[tuple[int, int, int, int, int, int]]:
        input_variables = []
        current_inputs = [0] * 6
        for i, line in enumerate(lines):
            if not line.strip('\n'):
                continue
            x, y = map(int, re.findall(r'\d+', line))
            
            if i % 4 == 0:
                current_inputs[0], current_inputs[1] = x, y
            elif i % 4 == 1:
                current_inputs[2], current_inputs[3] = x, y
            elif i % 4 == 2:
                current_inputs[4], current_inputs[5] = x, y
                input_variables.append(tuple(current_inputs))
            else:
                continue
        return input_variables
    
    @read_input("lines")
    def part1(self, lines: list[str]) -> int: 
        total_cost = 0
        
        for input_variables in self.parse_input_lines(lines):
            a_x, a_y, b_x, b_y, prize_x, prize_y = input_variables
            
            A, B = solve_simultaneous_equations(
                a_x, b_x, prize_x,
                a_y, b_y, prize_y
            )
            if is_nonnegative_integral(A) and is_nonnegative_integral(B):
                A, B = int(round(A, 0)), int(round(B, 0))
                total_cost += cost(A, B)
        
        return total_cost

    @read_input("lines")
    def part2(self, lines: list[str]) -> int: 
        total_cost = 0
        
        for input_variables in self.parse_input_lines(lines):
            a_x, a_y, b_x, b_y, prize_x, prize_y = input_variables
            prize_x, prize_y = 10000000000000 + prize_x, 10000000000000 + prize_y
             
            A, B = solve_simultaneous_equations(
                a_x, b_x, prize_x,
                a_y, b_y, prize_y
            )
            if is_nonnegative_integral(A) and is_nonnegative_integral(B):
                A, B = int(round(A, 0)), int(round(B, 0))
                total_cost += cost(A, B)

        return total_cost

if __name__=="__main__":
    solver = Day13("input13.txt")
    print(solver.part1())
    print(solver.part2())