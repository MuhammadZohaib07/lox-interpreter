from token_type import TokenType
import Expr
import Stmt


# Custom exception class for handling parse errors
class ParseError(RuntimeError):
    pass


class Parser:
    def __init__(self, tokens):
        # Initialize the parser with a list of tokens and set the current position to 0
        self.current = 0
        self.tokens = tokens

    # Entry point for parsing expressions
    def expression(self):
        return self.assignment()

    # Parse a declaration statement
    def declaration(self):
        try:
            if self.match(TokenType.FUN):
                return self.function("function")
            if self.match(TokenType.VAR):
                return self.var_declaration()
            if self.match(TokenType.CLASS):
                return self.class_declaration()
            return self.statement()
        except ParseError:
            self.synchronize()
            return None

    # Parse a class declaration
    def class_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect a class name.")
        super_class = None
        if self.match(TokenType.LESS):
            self.consume(TokenType.IDENTIFIER, "Expect superclass name.")
            super_class = Expr.Variable(self.previous())
        self.consume(TokenType.LEFT_BRACE, "Expect a '{' before class body.")
        methods = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            methods.append(self.function("method"))
        self.consume(TokenType.RIGHT_BRACE, "Expect a '}' after class body.")
        return Stmt.Class(name, super_class, methods)

    # Parse an equality expression
    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Expr.Binary(expr, operator, right)
        return expr

    # Check if the next token matches one of the given types
    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    # Check if the current token matches the given type
    def check(self, type):
        if self.is_at_end():
            return False
        return self.peek().type == type

    # Advance to the next token
    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    # Check if the current token is the end of file
    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    # Return the current token
    def peek(self):
        return self.tokens[self.current]

    # Return the previous token
    def previous(self):
        return self.tokens[self.current - 1]

    # Parse a comparison expression
    def comparison(self):
        expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Expr.Binary(expr, operator, right)
        return expr

    # Parse a term expression (addition and subtraction)
    def term(self):
        expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Expr.Binary(expr, operator, right)
        return expr

    # Parse a factor expression (multiplication and division)
    def factor(self):
        expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Expr.Binary(expr, operator, right)
        return expr

    # Parse a unary expression (negation and logical NOT)
    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Expr.Unary(operator, right)
        return self.call()

    # Finish parsing a function call
    def finish_call(self, callee):
        arguments = []
        if not self.check(TokenType.RIGHT_PAREN):
            arguments.append(self.expression())
            while self.match(TokenType.COMMA):
                if len(arguments) >= 255:
                    raise ValueError("Can't have more than 255 arguments.")
                arguments.append(self.expression())
        paren = self.consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")
        return Expr.Call(callee, paren, arguments)

    # Parse a function call or property access
    def call(self):
        expr = self.primary()
        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finish_call(expr)
            elif self.match(TokenType.DOT):
                name = self.consume(TokenType.IDENTIFIER, "Expect property name after '.'.")
                expr = Expr.Get(expr, name)
            else:
                break
        return expr

    # Parse a primary expression (literals, identifiers, grouping)
    def primary(self):
        if self.match(TokenType.FALSE):
            return Expr.Literal(False)
        elif self.match(TokenType.TRUE):
            return Expr.Literal(True)
        elif self.match(TokenType.NIL):
            return Expr.Literal(None)
        elif self.match(TokenType.NUMBER, TokenType.STRING):
            return Expr.Literal(self.previous().literal)
        elif self.match(TokenType.SUPER):
            keyword = self.previous()
            self.consume(TokenType.DOT, "Expect '.' after 'super'.")
            method = self.consume(TokenType.IDENTIFIER, "Expect superclass method name.")
            return Expr.Super(keyword, method)
        elif self.match(TokenType.THIS):
            return Expr.This(self.previous())
        elif self.match(TokenType.IDENTIFIER):
            return Expr.Variable(self.previous())
        elif self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)
        raise ParseError("Expect expression.")

    # Consume the current token if it matches the given type, otherwise raise an error
    def consume(self, type, message):
        if self.check(type):
            return self.advance()
        raise RuntimeError(message)

    # Raise a general parse error
    def error(self, message):
        raise RuntimeError(message)

    # Synchronize the parser to recover from errors
    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return
            if self.peek().type in [TokenType.CLASS, TokenType.FUN, TokenType.VAR, TokenType.FOR, TokenType.IF,
                                    TokenType.WHILE, TokenType.PRINT, TokenType.RETURN]:
                return
            self.advance()

    # Parse the list of statements in the source code
    def parse(self):
        statements = []
        while not self.is_at_end():
            stmt = self.declaration()
            if stmt is not None:
                statements.append(stmt)
        return statements

    # Parse a single statement
    def statement(self):
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.match(TokenType.LEFT_BRACE):
            return Stmt.Block(self.block())
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.RETURN):
            return self.return_statement()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.FOR):
            return self.for_statement()
        if self.match(TokenType.INPUT):
            return self.input_statement()
        return self.expression_statement()

    # Parse an input statement
    def input_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'input'.")
        expression = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after input prompt.")
        var_name = self.consume(TokenType.IDENTIFIER, "Expect variable name after 'input' statement.")
        self.consume(TokenType.SEMICOLON, "Expect ';' after input statement.")
        return Stmt.Input(var_name, expression)

    # Parse an if statement
    def if_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after 'if' condition.")
        then_branch = self.statement()
        else_branch = None
        if self.match(TokenType.ELSE):
            else_branch = self.statement()
        return Stmt.If(condition, then_branch, else_branch)

    # Parse a print statement
    def print_statement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Stmt.Print(value)

    # Parse a return statement
    def return_statement(self):
        keyword = self.previous()
        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return Stmt.Return(keyword, value)

    # Parse a variable declaration
    def var_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")
        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Stmt.Var(name, initializer)

    # Parse a while statement
    def while_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body = self.statement()
        return Stmt.While(condition, body)

    # Parse a for statement
    def for_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")
        initializer = None
        if self.match(TokenType.SEMICOLON):
            pass
        elif self.match(TokenType.VAR):
            initializer = self.var_declaration()
        else:
            initializer = self.expression_statement()
        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")
        increment = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")
        body = self.statement()
        if increment is not None:
            body = Stmt.Block([body, Stmt.Expression(increment)])
        if condition is None:
            condition = Expr.Literal(True)
        body = Stmt.While(condition, body)
        if initializer is not None:
            body = Stmt.Block([initializer, body])
        return body

    # Parse an expression statement
    def expression_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Stmt.Expression(expr)

    # Parse a function declaration
    def function(self, kind):
        name = self.consume(TokenType.IDENTIFIER, "Expect " + kind + " name.")
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after " + kind + " name.")
        parameters = []
        if not self.check(TokenType.RIGHT_PAREN):
            parameters.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name."))
            while self.match(TokenType.COMMA):
                if len(parameters) >= 255:
                    raise ValueError("Can't have more than 255 parameters.")
                parameters.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name."))
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")
        self.consume(TokenType.LEFT_BRACE, "Expect '{' before " + kind + " body.")
        body = self.block()
        return Stmt.Function(name, parameters, body)

    # Parse a block of statements
    def block(self):
        stmts = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            stmts.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return stmts

    # Parse an assignment expression
    def assignment(self):
        expr = self.logic_or()
        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expr, Expr.Variable):
                return Expr.Assign(expr.name, value)
            elif isinstance(expr, Expr.Get):
                return Expr.Set(expr.object, expr.name, value)
            raise ParseError("Invalid assignment target.")
        return expr

    # Parse a logical OR expression
    def logic_or(self):
        expr = self.logic_and()
        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.logic_and()
            expr = Expr.Logical(expr, operator, right)
        return expr

    # Parse a logical AND expression
    def logic_and(self):
        expr = self.equality()
        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = Expr.Logical(expr, operator, right)
        return expr
