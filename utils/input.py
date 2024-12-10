from enum import Enum

class InputFormat(Enum):
    STRING = "string"
    LINES = "lines"
    GRID = "grid"

def read_input(format: str):
    def decorator(func):
        def wrapper(self, input_file=None, *args, **kwargs):
            if input_file is None:
                input_file = self.input_file
            
            with open(input_file, 'r') as file:
                match format:
                    case InputFormat.STRING.value:
                        content = file.read().strip()
                    case InputFormat.LINES.value:
                        content = file.readlines()
                    case InputFormat.GRID.value:
                        content = [list(line.strip('\n')) for line in file.readlines()]
                    case _:
                        raise ValueError(f"Unrecognized input format: {format}")
            
            return func(self, content, *args, **kwargs)
        return wrapper
    return decorator
