from lox_callable import LoxCallable
from environment import Environment
from lox_return import LoxReturn


# Class representing a Lox function
class LoxFunction(LoxCallable):
    def __init__(self, declaration, closure, is_initializer):
        # Initialize the function with its declaration, closure environment, and whether it is an initializer
        self.declaration = declaration
        self.closure = closure
        self.is_initializer = is_initializer

    def call(self, interpreter, arguments):
        # Call the function with the given arguments
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except LoxReturn as return_value:
            if self.is_initializer:
                return self.closure.get_at(0, "this")
            return return_value.value
        if self.is_initializer:
            return self.closure.get_at(0, "this")
        return None

    def arity(self):
        # Return the number of parameters the function expects
        return len(self.declaration.params)

    def bind(self, instance):
        # Bind the function to an instance
        environment = Environment(self.closure)
        environment.define("this", instance)
        return LoxFunction(self.declaration, environment, self.is_initializer)

    def __str__(self):
        # Return the string representation of the function
        return "<fn " + self.declaration.name.lexeme + ">"
