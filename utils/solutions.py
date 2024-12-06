from enum import Enum
import json

class InputType(Enum):
    EXAMPLE = "example"
    PUZZLE = "puzzle"

with open("tests/solutions.json", 'r') as file:
    SOLUTIONS = json.load(file)

def solution(day, input_type, part):
    return SOLUTIONS[f"day{day:02}"][input_type][f"part{part}"]
