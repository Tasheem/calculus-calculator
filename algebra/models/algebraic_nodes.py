from algebra.models.atomic_nodes import *

class BinaryOperation(Expression):
    def __init__(self, left_side: Expression, operation: str, right_side: Expression) -> None:
        super().__init__()

        self.left_side = left_side
        self.operation = operation
        self.right_side = right_side

    def __str__(self):
        return self._stringify(self, None)

    def _stringify(self, expression: Expression | None, parent: Expression | None):
        if expression is None:
            return ""
        
        if isinstance(expression, BinaryOperation):
            equation_body = ""
            if expression.operation == "^":
                equation_body = f"{self._stringify(expression.left_side, expression)}{expression.operation}{self._stringify(expression.right_side, expression)}"
            else:
                equation_body = f"{self._stringify(expression.left_side, expression)} {expression.operation} {self._stringify(expression.right_side, expression)}"
            
            if parent is None or isinstance(expression, Power):
                return equation_body
            else:
                return f"({equation_body})"
        
        return str(expression)
    
    def compute(self):
        return self._binary_compute(self)

    def _binary_compute(self, expression: Expression):
        if isinstance(expression, Constant) or isinstance(expression, Variable):
            return expression.copy()
        elif isinstance(expression, BinaryOperation):
            left_side = expression.left_side.compute()
            right_side = expression.right_side.compute()

            if isinstance(left_side, Constant) and isinstance(right_side, Constant):
                value = 0.00
                if isinstance(expression, Sum):
                    value = left_side.value + right_side.value
                elif isinstance(expression, Difference):
                    value = left_side.value - right_side.value
                elif isinstance(expression, Product):
                    value = left_side.value * right_side.value
                elif isinstance(expression, Quotient):
                    if left_side.value == 0 or right_side.value == 0:
                        return expression.copy()

                    value = left_side.value / right_side.value
                elif isinstance(expression, Power):
                    value = left_side.value ** right_side.value
                else:
                    raise ValueError("Unknown Binary Expression")
                
                return Constant(value)
            else:
                simplified = expression.copy()
                simplified.left_side = left_side
                simplified.right_side = right_side

                return simplified
            
        return expression.copy()
            
        
class Sum(BinaryOperation):
    def __init__(self, left_side: Expression, right_side: Expression) -> None:
        super().__init__(left_side, "+", right_side)

    def copy(self):
        return Sum(self.left_side, self.right_side)

class Difference(BinaryOperation):
    def __init__(self, left_side: Expression, right_side: Expression) -> None:
        super().__init__(left_side, "-", right_side)

    def copy(self):
        return Difference(self.left_side, self.right_side)

class Product(BinaryOperation):
    def __init__(self, left_side: Expression, right_side: Expression) -> None:
        super().__init__(left_side, "*", right_side)

    def copy(self):
        return Product(self.left_side, self.right_side)

class Quotient(BinaryOperation):
    def __init__(self, left_side: Expression, right_side: Expression) -> None:
        super().__init__(left_side, "/", right_side)

        self.numerator = left_side
        self.denominator = right_side

    def copy(self):
        return Quotient(self.left_side, self.right_side)

class Power(BinaryOperation):
    def __init__(self, left_side: Expression, right_side: Expression) -> None:
        super().__init__(left_side, "^", right_side)

        self.base = left_side
        self.exponent = right_side

    def copy(self):
        return Power(self.left_side, self.right_side)
