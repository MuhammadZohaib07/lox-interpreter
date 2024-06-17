class LoxInstance:
    def __init__(self, klass):
        # Initialize the instance with its class and an empty field dictionary
        self.klass = klass
        self.fields = {}

    def __str__(self):
        # Return a string representation of the instance
        return self.klass.name + " instance"

    def get(self, name):
        # Get the value of a field or method by name
        if name.lexeme in self.fields.keys():
            return self.fields.get(name.lexeme)
        method = self.klass.find_method(name.lexeme)
        if method is not None:
            return method.bind(self)
        raise RuntimeError("Undefined property '" + name.lexeme + "'.")

    def set(self, name, value):
        # Set the value of a field
        self.fields.update({name.lexeme: value})
