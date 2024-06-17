from abc import ABC, abstractmethod


# Abstract base class for Lox callable entities (e.g., functions, classes)
class LoxCallable(ABC):
    @abstractmethod
    def call(self, interpreter, arguments):
        # Abstract method to call the entity with the given arguments
        pass

    def arity(self):
        # Method to return the number of arguments the callable expects
        pass
