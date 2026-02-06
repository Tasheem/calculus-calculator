from typing import Type

class Expression:
    def __init__(self) -> None:
        pass

    def compute[T](self: T) -> T:
        return self
    
    def copy[T](self: T) -> T:
        return self

class Constant(Expression):
    def __init__(self, value: float) -> None:
        super().__init__()

        self.value = value

    def copy(self):
        return Constant(self.value)

class Variable(Expression):
    def __init__(self, name: str) -> None:
        super().__init__()

        if len(name) > 1:
            raise ValueError("A variable can only be a char.")

        self.name = name

    def copy(self):
        return Variable(self.name)
