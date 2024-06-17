class Environment:
    def __init__(self, environment=None):
        # Initialize the environment with an optional enclosing environment
        self.values = {}
        self.enclosing = environment

    def define(self, name, object):
        # Define a new variable in the environment
        self.values[name] = object

    def ancestor(self, distance):
        # Find the ancestor environment at a given distance
        environment = self
        for _ in range(distance):
            environment = environment.enclosing
        return environment

    def get_at(self, distance, name):
        # Get the value of a variable at a specific distance in the environment chain
        value = self.ancestor(distance).values.get(name)
        return value

    def assign_at(self, distance, name, value):
        # Assign a value to a variable at a specific distance in the environment chain
        self.ancestor(distance).values.update({name.lexeme: value})

    def get(self, name):
        # Get the value of a variable in the current or enclosing environments
        if name.lexeme in self.values.keys():
            value = self.values[name.lexeme]
            return value
        if self.enclosing is not None:
            return self.enclosing.get(name)
        raise RuntimeError("Undefined variable " + name.lexeme + ".")

    def assign(self, name, value):
        # Assign a value to a variable in the current or enclosing environments
        if name.lexeme in self.values.keys():
            self.values.update({name.lexeme: value})
            return None
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return None
        raise RuntimeError("Undefined variable '" + name.lexeme + "'.")
