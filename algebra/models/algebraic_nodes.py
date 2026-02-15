from algebra.models.atomic_nodes import *
from utils.string_utils import *

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
                equation_body = f"{self._stringify(expression.left_side, expression)}{superscript(int(expression.right_side.value)) if isinstance(expression.right_side, Constant) else "^" + self._stringify(expression.right_side, expression)}"
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
    
    def simplify(self) -> Expression:
        raise RuntimeError("All subclasses of BinaryOperation should override the simplify() method.")
    
    def find_like_terms(self):
        """
        This function finds like terms in an expression returns the results in a map,
        with the key being the non-coefficient portion of like terms and the value being a list of coefficients 
        with matching non-coefficient expressions.
        """
        map: dict[Expression, list[int]] = {}
        self._find_like_terms_helper(self, map, False)

        return map
    
    def _find_like_terms_helper(self, expression: Expression, map: dict[Expression, list[int]], distribute_minus: bool) -> bool:
        if isinstance(expression, Constant):
            # Group all constants under the key "1".
            # Treating them as if they have 1 as their like-term, for example 9 + 3 = 9*1 + 3*1
            key = Constant(1)
            value = int(-expression.value) if distribute_minus else int(expression.value)

            self._add_to_map(map, key, value)

            return True
        elif isinstance(expression, Variable):
            value = -1 if distribute_minus else 1
            self._add_to_map(map, expression, value)

            return True
        elif isinstance(expression, Product):
            if isinstance(expression.left_side, Constant) and isinstance(expression.right_side, Variable):
                key = expression.right_side
                value = int(expression.left_side.value)
                self._add_to_map(map, key, -value if distribute_minus else value)

                return True
            elif isinstance(expression.left_side, Constant) and isinstance(expression.right_side, Power):
                key = expression.right_side
                value = int(expression.left_side.value)
                self._add_to_map(map, key, -value if distribute_minus else value)

                return True
            return False
        elif isinstance(expression, Power):
            base = expression.base
            exponent = expression.exponent

            if isinstance(base, Variable) and isinstance(exponent, Constant):
                self._add_to_map(map, expression, -1 if distribute_minus else 1)
                return True
            
            return False
        elif isinstance(expression, (Sum, Difference)):
            # Recurse left and right
            left_is_valid = self._find_like_terms_helper(expression.left_side, map, False)
            right_is_valid = self._find_like_terms_helper(expression.right_side, map, isinstance(expression, Difference))

            return left_is_valid and right_is_valid
        else:
            # Return False to indicate the root expression cannot be evaluated to combine like terms.
            return False
        
    def _add_to_map(self, map: dict[Expression, list[int]], key: Expression, value: int):
        if key in map:
            like_terms = map[key]
            like_terms.append(value)
        else:
            map[key] = [value]
        
class Sum(BinaryOperation):
    def __init__(self, left_side: Expression, right_side: Expression) -> None:
        super().__init__(left_side, "+", right_side)

    def copy(self):
        return Sum(self.left_side.copy(), self.right_side.copy())
    
    def simplify(self) -> Expression:
        map = self.find_like_terms()
        
        if len(map) > 0:
            return Constant(0)
        
        return Constant(0)
    
    def combine_fractions(self) -> Quotient | None:
        """
        If `self` contains quotients on its left and right sides and their denominators are the same, 
        this method combines those quotients into one quotient and returns that `Quotient` representation.

        Else, this method returns `None`.
        """
        if not isinstance(self.left_side, Quotient) or not isinstance(self.right_side, Quotient):
            return None
        
        # TODO: Replace this with a more robust Expression comparison function. Maybe traversing the expression tree.
        if not self.left_side.denominator.__eq__(self.right_side.denominator):
            return None
        
        combined_numerators = Sum(self.left_side.numerator.copy(), self.right_side.numerator.copy())
        return Quotient(combined_numerators, self.left_side.denominator.copy())

class Difference(BinaryOperation):
    def __init__(self, left_side: Expression, right_side: Expression) -> None:
        super().__init__(left_side, "-", right_side)

    def copy(self):
        return Difference(self.left_side.copy(), self.right_side.copy())
    
    def combine_fractions(self) -> Quotient | None:
        """
        If `self` contains quotients on its left and right sides and their denominators are the same, 
        this method combines those quotients into one quotient and returns that `Quotient` representation.

        Else, this method returns `None`.
        """
        if not isinstance(self.left_side, Quotient) or not isinstance(self.right_side, Quotient):
            return None
        
        # TODO: Replace this with a more robust Expression comparison function. Maybe traversing the expression tree.
        if not self.left_side.denominator.__eq__(self.right_side.denominator):
            return None
        
        combined_numerators = Difference(self.left_side.numerator.copy(), self.right_side.numerator.copy())
        return Quotient(combined_numerators, self.left_side.denominator.copy())

class Product(BinaryOperation):
    def __init__(self, left_side: Expression, right_side: Expression) -> None:
        super().__init__(left_side, "*", right_side)

    def copy(self):
        return Product(self.left_side.copy(), self.right_side.copy())

class Quotient(BinaryOperation):
    def __init__(self, left_side: Expression, right_side: Expression) -> None:
        super().__init__(left_side, "/", right_side)

        self.numerator = left_side
        self.denominator = right_side

    def copy(self):
        return Quotient(self.left_side.copy(), self.right_side.copy())

class Power(BinaryOperation):
    def __init__(self, left_side: Expression, right_side: Expression) -> None:
        super().__init__(left_side, "^", right_side)

        self.base = left_side
        self.exponent = right_side

    def copy(self):
        return Power(self.left_side.copy(), self.right_side.copy())
