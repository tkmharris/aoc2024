def read_input(lines=False):
    def decorator(func):
        def wrapper(self, input_file=None, *args, **kwargs):
            if input_file is None:
                input_file = self.input_file
            
            with open(input_file, 'r') as file:
                if lines:
                    # Can't do content = iter(file) as the file closes.
                    content = iter(file.readlines())
                else:
                    content = file.read()
            
            return func(self, content, *args, **kwargs)
        return wrapper
    return decorator
