import re
from utils.solver import Solver
from utils.input import read_input
from dataclasses import dataclass

@dataclass
class InputWire:
    name: str
    value: int


@dataclass
class LogicGate:
    input1: str
    input2: str
    operation: str
    output: str
    activated: bool = False


class Day24(Solver):
    def setup(self, lines: list[str]) -> tuple[dict[str, int], list[LogicGate]]:
        input_wires = []
        logic_gates = []
        output_wires = []

        input_mode = "variables"
        for line in lines:
            if not line.strip():
                input_mode = "operations"
                continue

            match input_mode:
                case "variables":
                    pattern = r'([a-z0-9]+): ([01])'
                    match = re.match(pattern, line)
                    name, value = match.groups()
                    input_wires.append(InputWire(name, int(value)))
                case "operations":
                    pattern = r'([a-z0-9]+) (AND|OR|XOR) ([a-z0-9]+) -> ([a-z0-9]+)'
                    match = re.match(pattern, line)
                    input1, operation, input2, output = match.groups()
                    logic_gates.append(LogicGate(input1, input2, operation, output))
                    if output.startswith('z'):
                        output_wires.append(output)

        return input_wires, logic_gates, output_wires


    @read_input("lines")
    def part1(self, lines: list[str]) -> int:
        input_wires, logic_gates, output_wires = self.setup(lines)
        state = {
            input_wire.name: input_wire.value
            for input_wire in input_wires
        }
        
        while any(
            state.get(output_wire) is None
            for output_wire in output_wires
        ):
            for gate in logic_gates:
                input1, input2 = state.get(gate.input1), state.get(gate.input2)
                
                if gate.activated or (input1 is None) or (input2 is None):
                    continue

                if gate.operation == 'AND':
                    state[gate.output] = state[gate.input1] & state[gate.input2]
                elif gate.operation == 'OR':
                    state[gate.output] = state[gate.input1] | state[gate.input2]
                elif gate.operation == 'XOR':
                    state[gate.output] = state[gate.input1] ^ state[gate.input2]
                
                gate.activated = True
        
        return int(
            ''.join(str(state[output]) for output in sorted(output_wires, reverse=True)),
            2
        )


    @read_input("lines")
    def part2(self, lines: list[str]) -> str:
        pass

if __name__ == "__main__":
    solver = Day24("input24.txt")
    print(solver.part1())  # type: ignore
    #print(solver.part2())  # type: ignore