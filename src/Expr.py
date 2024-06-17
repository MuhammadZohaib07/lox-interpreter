from abc import ABC, abstractmethod


# Abstract base class for expression visitors
class ExprVisitor(ABC):
    @abstractmethod
    def visit_assign_expr(self, expr):
        # Method to visit an assignment expression
        pass

    @abstractmethod
    def visit_binary_expr(self, expr):
        # Method to visit a binary expression
        pass

    @abstractmethod
    def visit_call_expr(self, expr):
        # Method to visit a call expression
        pass

    @abstractmethod
    def visit_get_expr(self, expr):
        # Method to visit a get expression (property access)
        pass

    @abstractmethod
    def visit_grouping_expr(self, expr):
        # Method to visit a grouping expression (parentheses)
        pass

    @abstractmethod
    def visit_literal_expr(self, expr):
        # Method to visit a literal expression (e.g., numbers, strings)
        pass

    @abstractmethod
    def visit_logical_expr(self, expr):
        # Method to visit a logical expression (AND, OR)
        pass

    @abstractmethod
    def visit_set_expr(self, expr):
        # Method to visit a set expression (assignment to a property)
        pass

    @abstractmethod
    def visit_super_expr(self, expr):
        # Method to visit a super expression (accessing superclass methods)
        pass

    @abstractmethod
    def visit_this_expr(self, expr):
        # Method to visit this expression (current instance)
        pass

    @abstractmethod
    def visit_unary_expr(self, expr):
        # Method to visit a unary expression (negation, logical NOT)
        pass

    @abstractmethod
    def visit_variable_expr(self, expr):
        # Method to visit a variable expression
        pass


# Abstract base class for expressions
class Expr:
    @abstractmethod
    def __init__(self):
        pass


# Assignment expression
class Assign(Expr):
    def __init__(self, name, value):
        # Initialize with variable name and assigned value
        self.name = name
        self.value = value

    def accept(self, visitor):
        # Accept a visitor
        return visitor.visit_assign_expr(self)


# Binary expression
class Binary(Expr):
    def __init__(self, left, operator, right):
        # Initialize with left operand, operator, and right operand
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        # Accept a visitor
        return visitor.visit_binary_expr(self)


# Call expression (function calls)
class Call(Expr):
    def __init__(self, callee, paren, arguments):
        # Initialize with callee, parenthesis token, and arguments
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor):
        # Accept a visitor
        return visitor.visit_call_expr(self)


# Get expression (property access)
class Get(Expr):
    def __init__(self, object, name):
        # Initialize with object and property name
        self.object = object
        self.name = name

    def accept(self, visitor):
        # Accept a visitor
        return visitor.visit_get_expr(self)


# Grouping expression (parentheses)
class Grouping(Expr):
    def __init__(self, expr):
        # Initialize with inner expression
        self.expr = expr

    def accept(self, visitor):
        # Accept a visitor
        return visitor.visit_grouping_expr(self)


# Literal expression (numbers, strings, booleans, etc.)
class Literal(Expr):
    def __init__(self, value):
        # Initialize with value
        self.value = value

    def accept(self, visitor):
        # Accept a visitor
        return visitor.visit_literal_expr(self)


# Logical expression (AND, OR)
class Logical(Expr):
    def __init__(self, left, operator, right):
        # Initialize with left operand, operator, and right operand
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        # Accept a visitor
        return visitor.visit_logical_expr(self)


# Set expression (assignment to a property)
class Set(Expr):
    def __init__(self, object, name, value):
        # Initialize with object, property name, and value
        self.object = object
        self.name = name
        self.value = value

    def accept(self, visitor):
        # Accept a visitor
        return visitor.visit_set_expr(self)


# Super expression (accessing superclass methods)
class Super(Expr):
    def __init__(self, keyword, method):
        # Initialize with keyword (super) and method name
        self.keyword = keyword
        self.method = method

    def accept(self, visitor):
        # Accept a visitor
        return visitor.visit_super_expr(self)


# This expression (current instance)
class This(Expr):
    def __init__(self, keyword):
        # Initialize with keyword (this)
        self.keyword = keyword

    def accept(self, visitor):
        # Accept a visitor
        return visitor.visit_this_expr(self)


# Unary expression (negation, logical NOT)
class Unary(Expr):
    def __init__(self, operator, right):
        # Initialize with operator and operand
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        # Accept a visitor
        return visitor.visit_unary_expr(self)


# Variable expression
class Variable(Expr):
    def __init__(self, name):
        # Initialize with variable name
        self.name = name

    def accept(self, visitor):
        # Accept a visitor
        return visitor.visit_variable_expr(self)
