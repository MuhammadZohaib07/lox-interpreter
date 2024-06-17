from lox_callable import LoxCallable
from lox_instance import LoxInstance


# Class representing a Lox class
class LoxClass(LoxCallable):
    def __init__(self, name, super_class, methods):
        # Initialize the class with a name, an optional superclass, and a dictionary of methods
        self.name = name
        self.super_class = super_class
        self.methods = methods

    def __str__(self):
        # Return the name of the class
        return self.name

    def find_method(self, name):
        # Find a method in the class or its superclass
        try:
            return self.methods[name]
        except KeyError:
            pass
        if self.super_class is not None:
            return self.super_class.find_method(name)
        return None

    def call(self, interpreter, args):
        # Create a new instance of the class and initialize it if there is an initializer method
        instance = LoxInstance(self)
        initializer = self.find_method("init")
        if initializer is not None:
            initializer.bind(instance).call(interpreter, args)
        return instance

    def arity(self):
        # Return the number of arguments the initializer method expects, or 0 if there is no initializer
        initializer = self.find_method("init")
        if initializer is None:
            return 0
        return initializer.arity()
