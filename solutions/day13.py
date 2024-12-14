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

def _cost(A: int, B: int) -> int:
    return 3 * A + B


def _solve_simultaneous_equations_in_nonnegative_integers(
    # represents a_x * A + b_x * B = prize_x
    a_x: int, b_x: int, prize_x: int,
    # represents a_y * A + b_y * B = prize_y
    a_y: int, b_y: int, prize_y: int 
) -> tuple[int, int] | None:
    det = a_x * b_y - a_y * b_x
    # Luckily for us, all the equations in the input have unique solutions.
    assert(det) != 0

    # formula falls out of the equations after inverting the 2x2 matrix
    # we check for divisibility by det first so we don't have to cast to floots
    # and handle precision issues
    A, B = (
        (b_y * prize_x - b_x * prize_y),
        (a_x * prize_y - a_y * prize_x)
    )
    if A % det != 0 or B % det != 0:
        return None
    
    A, B = A // det, B // det
    if A < 0 or B < 0:
        return None

    return A, B

def _parse_input_lines(lines: list[str]) -> list[tuple[int, int, int, int, int, int]]:
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

class Day13(Solver):
    @read_input("lines")
    def part1(self, lines: list[str]) -> int: 
        total_cost = 0
        
        for input_variables in _parse_input_lines(lines):
            a_x, a_y, b_x, b_y, prize_x, prize_y = input_variables
            
            solution = _solve_simultaneous_equations_in_nonnegative_integers(
                a_x, b_x, prize_x,
                a_y, b_y, prize_y
            )
            if solution:
                A, B = solution
                total_cost += _cost(A, B)
        
        return total_cost

    @read_input("lines")
    def part2(self, lines: list[str]) -> int: 
        total_cost = 0
        
        for input_variables in _parse_input_lines(lines):
            a_x, a_y, b_x, b_y, prize_x, prize_y = input_variables
            prize_x, prize_y = 10000000000000 + prize_x, 10000000000000 + prize_y
             
            solution = _solve_simultaneous_equations_in_nonnegative_integers(
                a_x, b_x, prize_x,
                a_y, b_y, prize_y
            )
            if solution:
                A, B = solution
                total_cost += _cost(A, B)

        return total_cost

if __name__=="__main__":
    solver = Day13("input13.txt")
    print(solver.part1())
    print(solver.part2())