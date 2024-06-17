# Class representing a token in the Lox language
class LoxToken:
    def __init__(self, type, lexeme, literal, line):
        # Initialize the token with its type, lexeme, literal value, and line number
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        # Return a string representation of the token
        return f"{str(self.type)} {self.lexeme} {self.literal}"

    def __repr__(self):
        # Return a representation of the token (same as its string representation)
        return self.__str__()
