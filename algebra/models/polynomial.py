from .atomic_nodes import *
from .algebraic_nodes import *

class Polynomial(Expression):
    def __init__(self, expression_or_coefficients: Sum | Difference | tuple[str, list[int]]) -> None:
        super().__init__()

        if isinstance(expression_or_coefficients, (Sum, Difference)):
            self.variable: Variable | None = None
            self.coefficients: list[Constant] = []
            self._construct_polynomial(expression_or_coefficients, None)
        else:
            self.variable = Variable(expression_or_coefficients[0])
            self.coefficients = [Constant(n) for n in expression_or_coefficients[1]]

    def degree(self):
        return len(self.coefficients) - 1

    def _construct_polynomial(self, expression: Expression | None, parent: Expression | None):
        distribute_minus = isinstance(parent, Difference) and expression is parent.right_side

        if expression is None:
            return
        elif isinstance(expression, Constant): # 0-degree
            self._add_coefficient(int(expression.value), None, 0, distribute_minus)
        elif isinstance(expression, Variable):
            # i.e. The x in the equation 2x² + x + 8
            self._add_coefficient(1, expression, 1, False)
        elif isinstance(expression, Power):
            base = expression.base
            exponent = expression.exponent
            if not isinstance(exponent, Constant):
                raise ValueError("A power node cannot contain a non-Constant type as its exponent. This is an invalid polynomial.")

            if isinstance(base, Variable): # i.e x²
                self._add_coefficient(1, base, int(exponent.value), distribute_minus)
            elif isinstance(base, Product): # i.e (2x)²
                if isinstance(base.left_side, Constant) and isinstance(base.right_side, Variable):
                    self._add_coefficient(int(base.left_side.value), base.right_side, int(exponent.value), distribute_minus)
                else:
                    raise ValueError("The base of this Power is a Product type. Expected the Product to contain a Constant on its left and Variable on its right.")
            else:
                raise ValueError("This Power node contains a base which should not exist in this polynomial:", expression, base)
        elif isinstance(expression, Product): # i.e 2x -> Product(Constant(2), Variable("x")) or 2x² -> Product(Constant(2), Power(Variable("x"), Constant(2)))
            if not isinstance(expression.left_side, Constant):
                raise ValueError("A Product node cannot contain a non-Constant type on its left side. This is an invalid polynomial.")
            
            if isinstance(expression.right_side, Variable): # 1-degree
                self._add_coefficient(int(expression.left_side.value), expression.right_side, 1, distribute_minus)
            elif isinstance(expression.right_side, Power): # nth-degree
                base = expression.right_side.left_side
                exponent = expression.right_side.right_side
                if not isinstance(exponent, Constant):
                    raise ValueError("A power node cannot contain a non-Constant type as its exponent. This is an invalid polynomial.")

                if not isinstance(base, Variable): # i.e x²
                    raise ValueError("A product node cannot contain a power node with a non-Variable type as its base.")
                
                self._add_coefficient(int(expression.left_side.value), base, int(exponent.value), distribute_minus)
            else:
                raise ValueError("This Product node contains a node on its right side which should not exist in this polynomial:", expression, expression.right_side)
        elif isinstance(expression, (Sum, Difference)):
            # Recursive case.
            # Recursive right first
            self._construct_polynomial(expression.right_side, expression)
            self._construct_polynomial(expression.left_side, expression)
        else:
            raise ValueError("This expression contains a node which should not exist in this polynomial:", expression)

    def _add_coefficient(self, coefficient: int, variable: Variable | None, degree: int, distribute_minus: bool):
        while len(self.coefficients) <= degree:
            self.coefficients.append(Constant(0))

        # If there is already a non-zero value at this degree, then we have duplicate degrees
        if self.coefficients[degree].value != 0:
            raise ValueError(f"Duplicates at degree: {degree}", self.coefficients[degree].value, coefficient)
        
        # Set the variable equal to the variable at this degree.
        if variable is not None:
            self._set_variable(variable)

        self.coefficients[degree] = Constant(coefficient * -1) if distribute_minus else Constant(coefficient)

    def _set_variable(self, exp_var: Variable):
        if self.variable is None:
            # Assume the first variable we come across is the single variable for this polynomial
            self.variable = exp_var.copy()
        elif self.variable.name != exp_var.name:
            # Raise error if we come across a second variable
            # This program will not support multivariable polynomials
            raise ValueError("Multivariable polynomials are not supported.", self.variable.name, exp_var.name)
