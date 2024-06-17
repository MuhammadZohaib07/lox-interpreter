from abc import ABC, abstractmethod


# Abstract base class for statement visitors
class StmtVisitor(ABC):
    @abstractmethod
    def visit_block_stmt(self, stmt):
        # Method to visit a block statement
        pass

    @abstractmethod
    def visit_class_stmt(self, stmt):
        # Method to visit a class statement
        pass

    @abstractmethod
    def visit_expression_stmt(self, stmt):
        # Method to visit an expression statement
        pass

    @abstractmethod
    def visit_function_stmt(self, stmt):
        # Method to visit a function statement
        pass

    @abstractmethod
    def visit_if_stmt(self, stmt):
        # Method to visit an if statement
        pass

    @abstractmethod
    def visit_print_stmt(self, stmt):
        # Method to visit a print statement
        pass

    @abstractmethod
    def visit_return_stmt(self, stmt):
        # Method to visit a return statement
        pass

    @abstractmethod
    def visit_var_stmt(self, stmt):
        # Method to visit a variable statement
        pass

    @abstractmethod
    def visit_while_stmt(self, stmt):
        # Method to visit while statement
        pass

    @abstractmethod
    def visit_input_stmt(self, stmt):
        # Method to visit an input statement
        pass


# Abstract base class for statements
class Stmt:
    @abstractmethod
    def __init__(self):
        pass


# Block statement (a list of statements)
class Block(Stmt):
    def __init__(self, stmts):
        # Initialize with a list of statements
        self.stmts = stmts

    def accept(self, visitor):
        # Accept a visitor
        return visitor.visit_block_stmt(self)


# Class statement (class declaration)
class Class(Stmt):
    def __init__(self, name, super_class, methods):
        # Initialize with class name, superclass, and methods
        self.name = name
        self.super_class = super_class
        self.methods = methods

    def accept(self, visitor):
        # Accept a visitor
        return visitor.visit_class_stmt(self)


# Expression statement
class Expression(Stmt):
    def __init__(self, expr):
        # Initialize with an expression
        self.expr = expr

    def accept(self, visitor):
        # Accept a visitor
        return visitor.visit_expression_stmt(self)


# Function statement (function declaration)
class Function(Stmt):
    def __init__(self, name, params, body):
        # Initialize with function name, parameters, and body
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor):
        # Accept a visitor
        return visitor.visit_function_stmt(self)


# If statement
class If(Stmt):
    def __init__(self, condition, then_branch, else_branch):
        # Initialize with condition, then-branch, and else-branch
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor):
        # Accept a visitor
        return visitor.visit_if_stmt(self)


# Print statement
class Print(Stmt):
    def __init__(self, expr):
        # Initialize with an expression to print
        self.expr = expr

    def accept(self, visitor):
        # Accept a visitor
        return visitor.visit_print_stmt(self)


# Return statement
class Return(Stmt):
    def __init__(self, keyword, value):
        # Initialize with return keyword and return value
        self.keyword = keyword
        self.value = value

    def accept(self, visitor):
        # Accept a visitor
        return visitor.visit_return_stmt(self)


# Variable declaration statement
class Var(Stmt):
    def __init__(self, name, initializer):
        # Initialize with variable name and initializer expression
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        # Accept a visitor
        return visitor.visit_var_stmt(self)


# While statement
class While(Stmt):
    def __init__(self, condition, body):
        # Initialize with condition and body statements
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        # Accept a visitor
        return visitor.visit_while_stmt(self)


# Input statement (custom statement for reading input)
class Input(Stmt):
    def __init__(self, name, expression):
        # Initialize with variable name and input prompt expression
        self.name = name
        self.expression = expression

    def accept(self, visitor):
        # Accept a visitor
        return visitor.visit_input_stmt(self)
