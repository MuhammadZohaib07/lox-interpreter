from lox_token import LoxToken
from token_type import TokenType


class Scanner:
    def __init__(self, source) -> None:
        # Initialize the scanner with source code and setup initial states
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.keywords = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE
        }

    def scan_tokens(self):
        # Scan tokens until the end of the source code is reached
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(LoxToken(TokenType.EOF, "", None, self.line))  # Add EOF token at the end
        return self.tokens

    def is_at_end(self):
        # Check if the current position has reached the end of the source code
        return self.current >= len(self.source)

    def scan_token(self):
        # Scan a single token and categorize it
        c = self.advance()
        if c == '(':
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ')':
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == '{':
            self.add_token(TokenType.LEFT_BRACE)
        elif c == '}':
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ',':
            self.add_token(TokenType.COMMA)
        elif c == '.':
            self.add_token(TokenType.DOT)
        elif c == '+':
            self.add_token(TokenType.PLUS)
        elif c == '-':
            self.add_token(TokenType.MINUS)
        elif c == ';':
            self.add_token(TokenType.SEMICOLON)
        elif c == '*':
            self.add_token(TokenType.STAR)
        elif c == '!':
            self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
        elif c == '=':
            self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
        elif c == '>':
            self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
        elif c == '<':
            self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
        elif c == '/':
            if self.match('/'):
                # Skip single-line comment
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif c == '\n':
            self.line += 1  # New line
        elif c in {' ', '\r', '\t'}:
            pass  # Ignore whitespace
        elif c == '"':
            self.string()
        else:
            if c.isdigit():
                self.number()
            elif c.isalpha() or c == '_':
                self.identifier()
            else:
                raise ValueError(f"Unexpected character: {c}")

    def advance(self):
        # Advance to the next character in the source code
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, token_type, literal=None):
        # Add a token of a given type and literal value to the token list
        text = self.source[self.start:self.current]
        self.tokens.append(LoxToken(token_type, text, literal, self.line))

    def match(self, expected):
        # Match the current character with an expected character
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self):
        # Look at the current character without consuming it
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self):
        # Look at the next character without consuming it
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def string(self):
        # Scan a string literal
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.is_at_end():
            raise ValueError("Unterminated string.")
        self.advance()
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)

    def number(self):
        # Scan a number literal
        while self.peek().isdigit():
            self.advance()
        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()
            self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))
        else:
            self.add_token(TokenType.NUMBER, int(self.source[self.start:self.current]))

    def identifier(self):
        # Scan an identifier or a keyword
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()
        text = self.source[self.start:self.current]
        token_type = self.keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)
