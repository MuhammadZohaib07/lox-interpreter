import enum
import Expr
import Stmt


# Enum to represent different types of functions
class FunctionType(enum.Enum):
    NONE = enum.auto()
    FUNCTION = enum.auto()
    INITIALIZER = enum.auto()
    METHOD = enum.auto()


# Enum to represent different types of classes
class ClassType(enum.Enum):
    NONE = enum.auto()
    CLASS = enum.auto()
    SUBCLASS = enum.auto()


# Resolver class to resolve variable and function scopes
class Resolver(Expr.ExprVisitor, Stmt.StmtVisitor):
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes = []
        self.current_function = FunctionType.NONE
        self.current_class = ClassType.NONE

    def visit_block_stmt(self, stmt):
        # Resolve a block statement by creating a new scope
        self.begin_scope()
        self.resolve_stmts(stmt.stmts)
        self.end_scope()
        return None

    def visit_class_stmt(self, stmt):
        # Resolve a class statement
        enclosing_class = self.current_class
        self.current_class = ClassType.CLASS
        self.declare(stmt.name)
        self.define(stmt.name)

        if stmt.super_class is not None and stmt.name.lexeme == stmt.super_class.name.lexeme:
            raise ValueError("A class can't inherit from itself.")

        if stmt.super_class is not None:
            self.current_class = ClassType.SUBCLASS
            self.resolve(stmt.super_class)
            self.begin_scope()
            self.scopes[-1]["super"] = True

        self.begin_scope()
        self.scopes[-1]["this"] = True
        for method in stmt.methods:
            declaration = FunctionType.METHOD
            if method.name.lexeme == "init":
                declaration = FunctionType.INITIALIZER
            self.resolve_function(method, declaration)

        self.end_scope()

        if stmt.super_class is not None:
            self.end_scope()
        self.current_class = enclosing_class
        return None

    def visit_expression_stmt(self, stmt):
        # Resolve an expression statement
        self.resolve(stmt.expr)
        return None

    def visit_function_stmt(self, stmt):
        # Resolve a function statement
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolve_function(stmt, FunctionType.FUNCTION)
        return None

    def visit_if_stmt(self, stmt):
        # Resolve an if statement
        self.resolve(stmt.condition)
        self.resolve(stmt.then_branch)
        if stmt.else_branch is not None:
            self.resolve(stmt.else_branch)
        return None

    def visit_print_stmt(self, stmt):
        # Resolve a print statement
        self.resolve(stmt.expr)
        return None

    def visit_return_stmt(self, stmt):
        # Resolve a return statement
        if self.current_function is FunctionType.NONE:
            raise ValueError("Can't return from top-level code.")
        if stmt.value is not None:
            if self.current_function is FunctionType.INITIALIZER:
                raise ValueError("Can't return a value from an initializer.")
            self.resolve(stmt.value)
        return None

    def visit_var_stmt(self, stmt):
        # Resolve a variable declaration statement
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve(stmt.initializer)
        self.define(stmt.name)
        return None

    def visit_while_stmt(self, stmt):
        # Resolve a while statement
        self.resolve(stmt.condition)
        self.resolve(stmt.body)
        return None

    def visit_assign_expr(self, expr):
        # Resolve an assignment expression
        self.resolve(expr.value)
        self.resolve_local(expr, expr.name)
        return None

    def visit_binary_expr(self, expr):
        # Resolve a binary expression
        self.resolve(expr.left)
        self.resolve(expr.right)
        return None

    def visit_call_expr(self, expr):
        # Resolve a call expression
        self.resolve(expr.callee)
        for arg in expr.arguments:
            self.resolve(arg)
        return None

    def visit_get_expr(self, expr):
        # Resolve a get expression (property access)
        self.resolve(expr.object)
        return None

    def visit_grouping_expr(self, expr):
        # Resolve a grouping expression
        self.resolve(expr.expr)
        return None

    def visit_literal_expr(self, expr):
        # Resolve a literal expression (no action needed)
        return None

    def visit_logical_expr(self, expr):
        # Resolve a logical expression
        self.resolve(expr.left)
        self.resolve(expr.right)
        return None

    def visit_set_expr(self, expr):
        # Resolve a set expression (assignment to a property)
        self.resolve(expr.value)
        self.resolve(expr.object)
        return None

    def visit_super_expr(self, expr):
        # Resolve a super expression (accessing superclass methods)
        if self.current_class is ClassType.NONE:
            raise ValueError("Can't use 'super' outside of a class.")
        elif self.current_class is not ClassType.SUBCLASS:
            raise ValueError("Can't use 'super' in a class with no superclass.")
        self.resolve_local(expr, expr.keyword)
        return None

    def visit_this_expr(self, expr):
        # Resolve this expression (current instance)
        if self.current_class is ClassType.NONE:
            raise ValueError("Can't use 'this' outside of a class.")
        self.resolve_local(expr, expr.keyword)
        return None

    def visit_unary_expr(self, expr):
        # Resolve a unary expression
        self.resolve(expr.right)
        return None

    def visit_variable_expr(self, expr):
        # Resolve a variable expression
        if len(self.scopes) != 0 and self.scopes[-1].get(expr.name.lexeme) is False:
            self.on_error(
                expr.name, "Cannot read local variable in its own initializer."
            )
        self.resolve_local(expr, expr.name)
        return None

    def visit_input_stmt(self, stmt):
        # Resolve an input statement
        self.resolve(stmt.expression)
        self.declare(stmt.name)
        self.define(stmt.name)
        return None

    def resolve_stmts(self, stmts):
        # Resolve a list of statements
        for stmt in stmts:
            self.resolve(stmt)

    def resolve(self, obj):
        # Resolve an expression or statement
        obj.accept(self)

    def resolve_function(self, function, type):
        # Resolve a function declaration
        enclosing_function = self.current_function
        self.current_function = type
        self.begin_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve_stmts(function.body)
        self.end_scope()
        self.current_function = enclosing_function

    def begin_scope(self):
        # Begin a new scope
        self.scopes.append({})

    def end_scope(self):
        # End the current scope
        self.scopes.pop()

    def declare(self, name):
        # Declare a variable in the current scope
        if len(self.scopes) == 0:
            return
        scope = self.scopes[-1]
        if name.lexeme in scope:
            raise ValueError("Already a variable with this name in this scope.")
        scope[name.lexeme] = False

    def define(self, name):
        # Define a variable in the current scope
        if len(self.scopes) == 0:
            return
        scope = self.scopes[-1]
        scope[name.lexeme] = True

    def resolve_local(self, expr, name):
        # Resolve a local variable in the current or enclosing scopes
        for idx, scope in enumerate(reversed(self.scopes)):
            if name.lexeme in scope:
                self.interpreter.resolve(expr, idx)
                return
