from dataclasses import dataclass
from math import ceil, floor, gcd
import re

@dataclass
class IntegerLinearEquation2Vars:
    """Represents Ax + By = c"""
    x_coefficient: int
    y_coefficient: int
    target: int

    @property
    def solvable(self) -> bool:
        # Solvable in integers if and only if the target value is divisible
        # by the greatest common divisor of the x and y coefficients
        # (essentially Bezout's identity).
        return self.target % gcd(self.x_coefficient, self.y_coefficient) == 0
    
    def is_solution(self, x: int, y: int) -> bool:
        return self.x_coefficient * x + self.y_coefficient * y == self.target
    
    def particular_solution(self) -> tuple[int, int]:
        if not self.solvable:
            raise Exception("Not solvable")
        
        # first solve x_coef / d * x + y_coef / d * y = c / d
        # where d = gcd(x_coef, y_coef)
        d = gcd(self.x_coefficient, self.y_coefficient)
        a, b = self.x_coefficient // d, self.y_coefficient // d
        
        if self.x_coefficient < self.y_coefficient: # require a >= b
            a, b = b, a 
        s0, s1 = 1, 0
        t0, t1 = 0, 1
        
        while b != 0:
            q = a // b
            a, b = b, a % b
            s0, s1 = s1, s0 - q * s1
            t0, t1 = t1, t0 - q * t1
        
        if self.x_coefficient < self.y_coefficient: # switch back if necessary
            s0, t0 = t0, s0

        # s0, t0 now solves x_coef / d * x + y_coef / d * y = 1
        Q = self.target // d
        return Q * s0, Q * t0
    
    def positive_solutions(self):
        x, y = self.particular_solution()
        d = gcd(self.x_coefficient, self.y_coefficient)

        t = floor(x * d / self.y_coefficient)
        x, y = ( x - t * (self.y_coefficient//d)), ( y + t * (self.x_coefficient//d))
        while x >= 0 and y >= 0:
            yield x,y
            x += (self.y_coefficient//d)
            y -= (self.x_coefficient//d)
        

    def solutions_increasing_first_coordinate(self, start):
        x, y = self.particular_solution()
        d = gcd(self.x_coefficient, self.y_coefficient)

        t = floor((x - start) * d / self.y_coefficient)
        x, y = ( x - t * (self.y_coefficient//d)), ( y + t * (self.x_coefficient//d))
        while x >= 0 and y >= 0:
            yield x,y
            x += (self.y_coefficient//d)
            y -= (self.x_coefficient//d)
    
    def solutions_in_range(self, lwr, upr):
        """
        Return all integer solutions with lwr <= x, y <= upr.
        """
        x, y = self.particular_solution()
        d = gcd(self.x_coefficient, self.y_coefficient)
        Q = self.target // d
        
        # these bounds fall out of the algebra if you look at parameterizing
        # the general solution to Bezout's identity from a particular one
        lwr_t = max(
            (lwr - y) * d / self.x_coefficient,
            (x - upr) * d / self.y_coefficient
        )
        upr_t = min(
            (upr - y) * d / self.x_coefficient,
            (x - lwr) * d / self.y_coefficient
        )
        t_range = range(ceil(lwr_t), floor(upr_t) + 1)
        
        return [
            (
                x - t * (self.y_coefficient // d), 
                y + t * (self.x_coefficient // d)
            )
            for t in t_range
        ]

def cost(solution: tuple[int, int]) -> int:
    return 3 * solution[0] + 1 * solution[1]

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
             
            equation_X = IntegerLinearEquation2Vars(a_x, b_x, prize_x)
            equation_Y = IntegerLinearEquation2Vars(a_y, b_y, prize_y)

            if not (equation_X.solvable and equation_Y.solvable):
                continue
            
            # equation_X.positive_solutions() yields the positive solutions to the X
            # equation in increasing size of the first variable (and, therefore, decreasing
            # size of the second variable). The cost function 3 * first_var + 1 * second_var
            # strictly increases so the minimal cost solution is the first positive solution
            # that satisfies both equations (if it exists).
            for solution in equation_X.positive_solutions():
                if equation_Y.is_solution(*solution):
                    total_cost += cost(solution)
                    break

        return total_cost
    