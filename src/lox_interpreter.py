import Expr
import Stmt
from time import time
from token_type import TokenType
from environment import Environment
from lox_callable import LoxCallable
from lox_function import LoxFunction
from lox_return import LoxReturn
from lox_class import LoxClass
from lox_instance import LoxInstance


class Interpreter(Expr.ExprVisitor, Stmt.StmtVisitor):
    def __init__(self) -> None:
        # Initialize the interpreter with a global environment and a map for local variable scopes
        self.globals = Environment()
        self.environment = self.globals
        self.locals = {}
        self.init_globals()

    def init_globals(self):
        # Define native functions in the global environment
        class Clock(LoxCallable):
            def __init__(self) -> None:
                super().__init__()
                self.start_time = time()

            def arity(self):
                return 0

            def call(self, interpreter, arguments):
                return time() - self.start_time

            def __str__(self):
                return "<native fn>"

        class InputFunction(LoxCallable):
            def arity(self):
                return 1

            def call(self, interpreter, arguments):
                prompt = arguments[0]
                return input(prompt)

            def __str__(self):
                return "<native fn 'input'>"

        self.globals.define("clock", Clock())
        self.globals.define("input", InputFunction())

    def visit_literal_expr(self, expr):
        # Evaluate a literal expression (e.g., numbers, strings, booleans)
        return expr.value

    def visit_logical_expr(self, expr):
        # Evaluate a logical expression (AND, OR)
        left = self.evaluate(expr.left)
        if expr.operator.type is TokenType.OR:
            if self.is_truthy(left):
                return left
        else:
            if not self.is_truthy(left):
                return left
        return self.evaluate(expr.right)

    def visit_set_expr(self, expr):
        # Evaluate a set expression to assign a value to an object's property
        object = self.evaluate(expr.object)
        if not isinstance(object, LoxInstance):
            raise RuntimeError("Only instances have fields")
        value = self.evaluate(expr.value)
        object.set(expr.name, value)
        return value

    def visit_super_expr(self, expr):
        # Evaluate a super expression to access superclass methods
        distance = self.locals.get(expr)
        if distance is None:
            raise RuntimeError("Unresolved variable 'super'.")
        super_class = self.environment.get_at(distance, "super")
        object = self.environment.get_at(distance - 1, "this")
        method = super_class.find_method(expr.method.lexeme)
        if method is None:
            raise RuntimeError(f"Undefined property '{expr.method.lexeme}'.")
        return method.bind(object)

    def visit_this_expr(self, expr):
        # Evaluate a 'this' expression to access the current instance
        return self.look_up_variable(expr.keyword, expr)

    def visit_grouping_expr(self, expr):
        # Evaluate a grouping expression (parentheses)
        return self.evaluate(expr.expr)

    def visit_unary_expr(self, expr):
        # Evaluate a unary expression (e.g., negation, logical NOT)
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            self.check_num_operand(right)
            return -float(right)
        elif expr.operator.type == TokenType.BANG:
            return not self.is_truthy(right)
        return None

    def visit_variable_expr(self, expr):
        # Evaluate a variable expression to get its value
        return self.look_up_variable(expr.name, expr)

    def look_up_variable(self, name, expr):
        # Look up a variable in the current or global environment
        distance = self.locals.get(expr)
        if distance is not None:
            return self.environment.get_at(distance, name.lexeme)
        else:
            return self.globals.get(name)

    def visit_binary_expr(self, expr):
        # Evaluate a binary expression (e.g., addition, subtraction, comparison)
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            self.check_num_operands(left, right)
            return float(left) - float(right) if isinstance(left, float) or isinstance(right, float) else int(left) - int(right)
        elif expr.operator.type in {TokenType.GREATER, TokenType.GREATER_EQUAL,
                                    TokenType.LESS, TokenType.LESS_EQUAL}:
            self.check_num_operands(left, right)
            return eval(f'{left} {expr.operator.lexeme} {right}')
        elif expr.operator.type in {TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL}:
            return (left == right) if expr.operator.type == TokenType.EQUAL_EQUAL else (left != right)
        elif expr.operator.type == TokenType.PLUS:
            if isinstance(left, (float, int)) and isinstance(right, (float, int)):
                return float(left) + float(right) if isinstance(left, float) or isinstance(right, float) else int(left) + int(right)
            elif isinstance(left, str) or isinstance(right, str):
                if isinstance(left, (int, float)):
                    left = str(left)
                if isinstance(right, (int, float)):
                    right = str(right)
                return left + right
            else:
                raise RuntimeError("Operands must be two numbers or two strings.")
        elif expr.operator.type == TokenType.SLASH:
            self.check_num_operands(left, right)
            if right == 0.0:
                raise RuntimeError("Division by 0 is not allowed.")
            return float(left) / float(right)
        elif expr.operator.type == TokenType.STAR:
            self.check_num_operands(left, right)
            return float(left) * float(right) if isinstance(left, float) or isinstance(right, float) else int(left) * int(right)
        return None

    def visit_call_expr(self, expr):
        # Evaluate a function call expression
        callee = self.evaluate(expr.callee)
        arguments = [self.evaluate(argument) for argument in expr.arguments]
        if not isinstance(callee, LoxCallable):
            raise RuntimeError("Can only call functions and classes.")
        function = callee
        if len(arguments) != function.arity():
            raise RuntimeError(
                f"Expected {function.arity()} arguments but got {len(arguments)}."
            )
        return function.call(self, arguments)

    def visit_get_expr(self, expr):
        # Evaluate a get expression to access an object's property
        object = self.evaluate(expr.object)
        if isinstance(object, LoxInstance):
            return object.get(expr.name)
        raise RuntimeError("Only instances have properties.")

    def check_num_operand(self, operand):
        # Check if a single operand is a number
        if isinstance(operand, (int, float)):
            return
        raise RuntimeError("Operand must be a number.")

    def check_num_operands(self, *operands):
        # Check if all operands are numbers
        for operand in operands:
            if not isinstance(operand, (int, float)):
                raise RuntimeError("Operands must be numbers.")

    def is_equal(self, a, b):
        # Check if two values are equal
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b

    def evaluate(self, expr):
        # Evaluate an expression by accepting it
        return expr.accept(self)

    def visit_expression_stmt(self, stmt):
        # Execute an expression statement
        self.evaluate(stmt.expr)
        return None

    def visit_function_stmt(self, stmt):
        # Execute a function statement to define a function
        function = LoxFunction(stmt, self.environment, False)
        self.environment.define(stmt.name.lexeme, function)
        return None

    def visit_if_stmt(self, stmt):
        # Execute an if statement
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)
        return None

    def visit_print_stmt(self, stmt):
        # Execute a print statement to output a value
        value = self.evaluate(stmt.expr)
        print(self.stringify(value))
        return None

    def visit_return_stmt(self, stmt):
        # Execute a return statement to return a value from a function
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        raise LoxReturn(value)

    def visit_var_stmt(self, stmt):
        # Execute a variable declaration statement
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)
        return None

    def visit_while_stmt(self, stmt):
        # Execute a while statement
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
        return None

    def visit_assign_expr(self, expr):
        # Evaluate an assignment expression to assign a value to a variable
        value = self.evaluate(expr.value)
        distance = self.locals.get(expr)
        if distance is not None:
            self.environment.assign_at(distance, expr.name, value)
        else:
            self.globals.assign(expr.name, value)
        return value

    def visit_input_stmt(self, stmt):
        # Execute an input statement to read input from the user
        prompt = self.evaluate(stmt.expression)
        value = self.globals.get("input").call(self, [prompt])
        self.environment.define(stmt.name.lexeme, value)

    def is_truthy(self, obj):
        # Determine if a value is truthy
        if obj is None:
            return False
        if isinstance(obj, bool):
            return bool(obj)
        return True

    def interpret(self, statements):
        # Interpret and execute a list of statements
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError as error:
            raise error

    def execute(self, stmt):
        # Execute a statement by accepting it
        stmt.accept(self)

    def resolve(self, expr, depth):
        # Resolve a variable by storing its scope distance
        self.locals[expr] = depth

    def execute_block(self, stmts, environment):
        # Execute a block of statements within a new environment
        previous = self.environment
        try:
            self.environment = environment
            for stmt in stmts:
                self.execute(stmt)
        finally:
            self.environment = previous

    def visit_block_stmt(self, stmt):
        # Execute a block statement
        self.execute_block(stmt.stmts, Environment(self.environment))
        return None

    def visit_class_stmt(self, stmt):
        # Execute a class statement to define a class
        super_class = None
        if stmt.super_class is not None:
            super_class = self.evaluate(stmt.super_class)
            if not isinstance(super_class, LoxClass):
                raise RuntimeError("Superclass must be a class.")
        self.environment.define(stmt.name.lexeme, None)
        if stmt.super_class is not None:
            self.environment = Environment(self.environment)
            self.environment.define("super", super_class)
        methods = {}
        for method in stmt.methods:
            function = LoxFunction(method, self.environment, method.name.lexeme == "init")
            methods.update({method.name.lexeme: function})
        klass = LoxClass(stmt.name.lexeme, super_class, methods)
        if super_class is not None:
            self.environment = self.environment.enclosing
        self.environment.assign(stmt.name, klass)
        return None

    def stringify(self, obj):
        # Convert a value to a string representation
        if obj is None:
            return "nil"
        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        return str(obj)
