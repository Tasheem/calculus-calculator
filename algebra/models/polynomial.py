from .atomic_nodes import *
from .algebraic_nodes import *

class Polynomial(Expression):
    def __init__(self, expression_or_coefficients: Sum | Difference | tuple[str, list[int]]) -> None:
        super().__init__()

        if isinstance(expression_or_coefficients, (Sum, Difference)):
            self.coefficients = []
            self._construct_polynomial(expression_or_coefficients)
        else:
            self.variable = expression_or_coefficients[0]
            self.coefficients = expression_or_coefficients[1]

    def _construct_polynomial(self, expression: Expression | None):
        if expression is None:
            return
        elif isinstance(expression, Constant): # 0th degree
            self._add_coefficient(int(expression.value), 0)
        elif isinstance(expression, Power):
            base = expression.base
            exponent = expression.exponent
            if not isinstance(exponent, Constant):
                raise ValueError("A power node cannot contain a non-Constant type as its exponent. This is an invalid polynomial.")

            if isinstance(base, Variable): # i.e x²
                self._add_coefficient(1, int(exponent.value))
            elif isinstance(base, Product):
                if isinstance(base.left_side, Constant) and isinstance(base.right_side, Variable):
                    self._add_coefficient(int(base.left_side.value), int(exponent.value))
                else:
                    raise ValueError("The base of this Power is a Product type. Expected the Product to contain a Constant on its left and Variable on its right.")

    def _add_coefficient(self, coefficient: int, degree: int):
        while len(self.coefficients) <= degree:
            self.coefficients.append(0)

        self.coefficients[degree] = coefficient
