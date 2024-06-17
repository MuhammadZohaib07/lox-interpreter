# Custom exception class for handling return statements in Lox
class LoxReturn(Exception):
    def __init__(self, value):
        # Initialize the return exception with a value
        super().__init__(None)
        self.value = value
