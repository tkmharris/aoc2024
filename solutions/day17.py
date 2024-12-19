from utils.solver import Solver
from utils.input import read_input
from dataclasses import dataclass
from collections import deque


@dataclass
class Program:
    register_a: int
    register_b: int
    register_c: int
    instructions: list[int]

class Computer:
    register_a: int = 0
    register_b: int = 0
    register_c: int = 0
    instruction_pointer: int = 0
    outputs: list[int] = []
    jump_flag: bool = False

    def reset(self):
        self.register_a = 0
        self.register_b = 0
        self.register_c = 0
        self.instruction_pointer = 0
        self.outputs = []
        self.jump_flag = False

    def output(self):
        return ','.join(map(str, self.outputs))

    def literal(self, operand):
        return operand
    
    def combo(self, operand):
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.register_a
            case 5:
                return self.register_b
            case 6:
                return self.register_c
            case 7:
                raise ValueError("Combo operand 7 should never appear")


    def execute_instruction(self, opcode, operand):
        self.jump_flag = False
        
        # Individual opcode instructions
        def adv(literal):
            self.register_a = self.register_a >> literal
        
        def bdv(literal):
            self.register_b = self.register_a >> literal

        def cdv(literal):
            self.register_c = self.register_a >> literal
        
        def bxl(literal):
            self.register_b = self.register_b ^ literal

        def bst(literal):
            self.register_b = literal % 8
        
        def jnz(literal):
            if self.register_a != 0:
                self.instruction_pointer = literal
                self.jump_flag = True
        
        def bxc():
            self.register_b = self.register_b ^ self.register_c

        def out(literal):
            self.outputs.append(literal % 8)

        match opcode:
            case 0: 
                adv(self.combo(operand))
            case 1:
                bxl(self.literal(operand))
            case 2:
                bst(self.combo(operand))
            case 3:
                jnz(self.literal(operand))
            case 4:
                bxc()
            case 5:
                out(self.combo(operand))
            case 6:
                bdv(self.combo(operand))
            case 7:
                cdv(self.combo(operand))
            case _:
                raise ValueError("Invalid opcode")

    
    def execute(self, program: Program) -> str:
        self.reset()
        self.register_a = program.register_a
        self.register_b = program.register_b
        self.register_c = program.register_c

        while (p := self.instruction_pointer) < len(program.instructions):
            opcode, operand = program.instructions[p: p + 2]
            self.execute_instruction(opcode, operand)

            if not self.jump_flag:
                self.instruction_pointer += 2
            
        return self.output()

class Day17(Solver):
    def setup(self, lines: list[str]):
        for line_number, line in enumerate(lines):
            match line_number:
                case 0:
                    register_a = int(line[12:])
                case 1:
                    register_b = int(line[12:])
                case 2:
                    register_c = int(line[12:])    
                case 3:
                    continue
                case 4:
                    instructions = [
                        int(number) for number in line[9:].split(',')
                    ]
                case _:
                    raise ValueError("Invalid format")
        
        computer = Computer()
        program = Program(
            register_a=register_a,
            register_b=register_b,
            register_c=register_c,
            instructions=instructions
        )

        return computer, program
    

    @read_input("lines")
    def part1(self, lines: list[str]) -> str:
        computer, program = self.setup(lines)
        computer.execute(program)
        return computer.output()
    
    
    @read_input("lines")
    def part1_alt(self, lines: list[str]) -> str:
        computer, program = self.setup(lines)
        
        # This is what program actually does for the 
        # program in input17.txt
        outputs = []
        a, b = program.register_a, program.register_b
        while a > 0:
            a, b = (
                a // 8,
                (6 ^ (a % 8) ^ (a >> ((a % 8) ^ 3))) % 8
            )
            outputs.append(b)
        output = ','.join(map(str, outputs))

        computer.execute(program)
        assert output == computer.output()
        
        return output


    @read_input("lines")
    def part2(self, lines: list[str]) -> int:
        computer, program = self.setup(lines)

        queue = deque([(0,len(program.instructions) - 1)])
        winners = []
        while queue:
            register_a, current_instruction = queue.popleft()
            target = program.instructions[current_instruction]
            for candidate in range(8):
                current_guess = 8 * register_a + candidate
                calc = (6 ^ candidate ^ (current_guess >> (candidate ^ 3))) % 8
                if calc == target:
                    if current_instruction != 0:
                        queue.append(
                            (current_guess, current_instruction - 1)
                        )
                    else:
                        winners.append(current_guess)

        register_a = min(winners)

        program.register_a = register_a
        computer.execute(program)
        assert computer.output() == ','.join(map(str, program.instructions))
        
        return register_a
    

if __name__=="__main__":
    solver = Day17("input17.txt")
    print(solver.part1()) # type: ignore
    print(solver.part2()) # type: ignore