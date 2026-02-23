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
            if isinstance(expression, Power):
                equation_body = f"{self._stringify(expression.left_side, expression)}{superscript(int(expression.right_side.value)) if isinstance(expression.right_side, Constant) else "^" + self._stringify(expression.right_side, expression)}"
            elif isinstance(expression, Product) and isinstance(expression.right_side, (Power, Variable)):
                equation_body = f"{self._stringify(expression.left_side, expression)}{self._stringify(expression.right_side, expression)}"
            else:
                equation_body = f"{self._stringify(expression.left_side, expression)} {expression.operation} {self._stringify(expression.right_side, expression)}"
            
            if parent is None or isinstance(expression, Power) or (isinstance(expression, Product) and isinstance(expression.right_side, (Power, Variable))):
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
        # Distribute negatives from difference nodes.
        curr_tree = self.distribute_negatives()
        if isinstance(curr_tree, Constant):
            return curr_tree

        # Simplify powers
        curr_tree = curr_tree.simplify_powers()

        # Combine fractions with same denominators

        # Simplify complex fractions

        # Maybe factor if it is a polynomial? 
        # May need to factor the numerator and denominator if the root of the expression tree is a Quotient at this point.

        # Combine like terms

        return Constant(0)
    
    def distribute_negatives(self):
        return self._distribute_negatives(self, False)

    def _distribute_negatives(self, expression: Expression, distribute: bool):
        if not isinstance(expression, BinaryOperation):
            if isinstance(expression, Constant):
                return expression.additive_inverse()
            else: # return -x
                return Product(Constant(-1), expression.copy())
        
        if not isinstance(expression, Difference):
            # Recurse to find Difference nodes
            expression.left_side = self._distribute_negatives(expression.left_side, distribute)
            expression.right_side = self._distribute_negatives(expression.right_side, distribute)

            return expression
        
        return Sum(expression.left_side.copy(), self._distribute_negatives(expression.right_side, True))
    
    def simplify_powers(self):
        return self._simplify_powers(self)

    def _simplify_powers(self, expression: Expression):
        if not isinstance(expression, BinaryOperation):
            return expression.copy()
        
        if not isinstance(expression, Product):
            expression.left_side = self._simplify_powers(expression.left_side)
            expression.right_side = self._simplify_powers(expression.right_side)

            return expression
        
        # Multiply the coefficients and add the exponents
        if isinstance(expression.left_side, (Product, Power, Variable)) and isinstance(expression.right_side, (Product, Power, Variable)):
            left_components = self._extract_power_components(expression.left_side)
            right_components = self._extract_power_components(expression.right_side)
            if left_components is None or right_components is None:
                return expression.copy()

            left_coefficient, left_variable, left_exponent = left_components
            right_coefficient, right_variable, right_exponent = right_components

            if left_variable != right_variable:
                return expression.copy()
            
            coefficient = Constant(left_coefficient * right_coefficient)
            power_portion = Power(Variable(left_variable), Constant(left_exponent + right_exponent))
            if coefficient.value == 1:
                return Power(Variable(left_variable), Constant(left_exponent + right_exponent))
            else:
                return Product(coefficient, power_portion)
        else:
            expression.left_side = self._simplify_powers(expression.left_side)
            expression.right_side = self._simplify_powers(expression.right_side)

            return expression
        
    def _extract_power_components(self, expression: Product | Power | Variable) -> tuple[int, str, int] | None:
        """
        Returns a tuple in the form (coefficient, variable_name, exponent)
        """
        if isinstance(expression, Variable):
            return (1, expression.name, 1)
        elif isinstance(expression, Power):
            if isinstance(expression.base, Variable) and isinstance(expression.exponent, Constant):
                return (1, expression.base.name, int(expression.exponent.value))
        elif isinstance(expression, Product):
            if isinstance(expression.left_side, Constant) and isinstance(expression.right_side, Variable):
                return (int(expression.left_side.value), expression.right_side.name, 1)
            elif isinstance(expression.left_side, Variable) and isinstance(expression.right_side, Constant):
                return (int(expression.right_side.value), expression.left_side.name, 1)
            elif isinstance(expression.left_side, Constant) and isinstance(expression.right_side, Power):
                base = expression.right_side.base
                exponent = expression.right_side.exponent

                if isinstance(base, Variable) and isinstance(exponent, Constant):
                    return (int(expression.left_side.value), base.name, int(exponent.value))
            elif isinstance(expression.left_side, Power) and isinstance(expression.right_side, Constant):
                base = expression.left_side.base
                exponent = expression.left_side.exponent

                if isinstance(base, Variable) and isinstance(exponent, Constant):
                    return (int(expression.right_side.value), base.name, int(exponent.value))
            
        return None

class AdditiveOperation(BinaryOperation):
    def __init__(self, left_side: Expression, operation: str, right_side: Expression) -> None:
        super().__init__(left_side, operation, right_side)

    def extract_coefficient(self, expression: Expression, distribute_minus: bool) -> tuple[Constant | Quotient | None, Constant | Variable | Power | None]:
        """
        This method takes an `Expression` and returns a tuple containing that expression's coefficient
        and variable_part in the form of (coefficient, variable_part).

        If a coefficient-variable pair cannot be found, this method returns `(None, None)`.
        """
        if isinstance(expression, Constant):
            # Group all constants under the key "1".
            # Treating them as if they have 1 as their like-term, for example 9 + 3 = 9*1 + 3*1
            coefficient = Constant(-expression.value) if distribute_minus else Constant(expression.value)
            variable_part = Constant(1)

            return (coefficient, variable_part)
        elif isinstance(expression, Variable):
            coefficient = Constant(-1) if distribute_minus else Constant(1)
            return (coefficient, expression)
        elif isinstance(expression, Quotient) and isinstance(expression.numerator, Constant) and isinstance(expression.denominator, Constant):
            # Group all fractions under the key "1", along with constants.
            coefficient = Quotient(expression.numerator.additive_inverse(), expression.denominator.copy()) if distribute_minus else Quotient(expression.numerator.copy(), expression.denominator.copy())
            variable_part = Constant(1)

            return (coefficient, variable_part)
        elif isinstance(expression, Product):
            if isinstance(expression.left_side, Constant) and isinstance(expression.right_side, Variable):
                coefficient = Constant(-int(expression.left_side.value)) if distribute_minus else Constant(int(expression.left_side.value))
                variable_part = expression.right_side

                return (coefficient, variable_part)
            elif isinstance(expression.left_side, Quotient) and isinstance(expression.right_side, Variable):
                quotient = expression.left_side
                if not isinstance(quotient.numerator, Constant) or not isinstance(quotient.denominator, Constant):
                    return (None, None)

                coefficient = Quotient(quotient.numerator.additive_inverse(), quotient.denominator.copy()) if distribute_minus else Quotient(quotient.numerator.copy(), quotient.denominator.copy())
                variable_part = expression.right_side

                return (coefficient, variable_part)
            elif isinstance(expression.left_side, Constant) and isinstance(expression.right_side, Power):
                coefficient = Constant(-int(expression.left_side.value)) if distribute_minus else Constant(int(expression.left_side.value))
                variable_part = expression.right_side

                return (coefficient, variable_part)
            elif isinstance(expression.left_side, Quotient) and isinstance(expression.right_side, Power):
                quotient = expression.left_side
                if not isinstance(quotient.numerator, Constant) or not isinstance(quotient.denominator, Constant):
                    return (None, None)
                
                coefficient = Quotient(quotient.numerator.additive_inverse(), quotient.denominator.copy()) if distribute_minus else Quotient(quotient.numerator.copy(), quotient.denominator.copy())
                variable_part = expression.right_side

                return (coefficient, variable_part)
            else:
                return (None, None)
        elif isinstance(expression, Power):
            base = expression.base
            exponent = expression.exponent

            if isinstance(base, Variable) and isinstance(exponent, Constant):
                return (Constant(-1) if distribute_minus else Constant(1), expression)
            
            return (None, None)
        else:
            # Return False to indicate the root expression cannot be evaluated to combine like terms.
            return (None, None)
    
    def has_like_terms(self):
        """
        This method traverses the expression tree, reaches all leaf nodes and returns
        true if any of the leaf nodes share a common variable part or like-term.
        """
        return self._has_like_terms_helper(self, set())

    def _has_like_terms_helper(self, expression: Expression | None, seen: set[Expression]) -> bool:
        if expression is None:
            return False
        
        if not isinstance(expression, (Sum, Difference)): 
            _, variable_part = self.extract_coefficient(expression, False)
            if variable_part is None:
                return False
            
            # If more than one term with the same non-coefficient has been found, 
            # we can conclude that like terms exist.
            if variable_part in seen:
                return True
            seen.add(variable_part)

            return False

        left_has_like_terms = self._has_like_terms_helper(expression.left_side, seen)
        right_has_like_terms = self._has_like_terms_helper(expression.right_side, seen)
        return left_has_like_terms or right_has_like_terms

    
    def find_like_terms(self):
        """
        This function finds like terms in an expression returns the results in a map,
        with the key being the non-coefficient portion of like terms and the value being a list of coefficients 
        with matching non-coefficient expressions.
        """
        map: dict[Expression, list[Constant | Quotient]] = {}
        self._find_like_terms_helper(self, map, False)

        return map
    
    def _find_like_terms_helper(self, expression: Expression, map: dict[Expression, list[Constant | Quotient]], distribute_minus: bool) -> bool:
        if isinstance(expression, (Sum, Difference)):
            # Recurse left and right
            left_is_valid = self._find_like_terms_helper(expression.left_side, map, False)
            right_is_valid = self._find_like_terms_helper(expression.right_side, map, isinstance(expression, Difference))

            return left_is_valid and right_is_valid
        else:
            coefficient, variable_part = self.extract_coefficient(expression, distribute_minus)
            if coefficient is None or variable_part is None:
                return False

            self._add_to_map(map, variable_part, coefficient)
            return True
        
    def _add_to_map(self, map: dict[Expression, list[Constant | Quotient]], key: Expression, value: Constant | Quotient):
        if key in map:
            like_terms = map[key]
            like_terms.append(value)
        else:
            map[key] = [value]

    def combine_like_terms(self):
        if not self.has_like_terms():
            return None

        # Find like terms
        map = self.find_like_terms()

        # TODO: Combine fractions before combining like terms

        # Add like terms & put them in a final array.
        combined_terms: list[Expression] = []
        for key in map:
            like_terms = map[key]
            
            final_coefficient: Constant | Quotient = Constant(0)
            for current_coefficient in like_terms:
                if isinstance(final_coefficient, Constant) and final_coefficient.value == 0 and isinstance(current_coefficient, (Constant, Quotient)):
                    final_coefficient = current_coefficient.copy()
                    continue

                if not isinstance(current_coefficient, (Constant, Quotient)):
                    # Should never hit this case since we should only have coefficients that are constants or quotients.
                    continue
                elif isinstance(current_coefficient, Constant):
                    if isinstance(final_coefficient, Constant):
                        final_coefficient = Constant(final_coefficient.value + current_coefficient.value)
                    elif isinstance(final_coefficient, Quotient):
                        added_frac = final_coefficient.add(Quotient(current_coefficient, Constant(1)))
                        if added_frac is None:
                            raise ValueError("Something went wrong when trying to add coefficients that are fractions.", current_coefficient, final_coefficient)
                        
                        final_coefficient = added_frac
                elif isinstance(current_coefficient, Quotient):
                    if isinstance(final_coefficient, Constant):
                        added_frac = current_coefficient.add(Quotient(final_coefficient, Constant(1)))
                        if added_frac is None:
                            raise ValueError("Something went wrong when trying to add coefficients that are fractions.", current_coefficient, final_coefficient)

                        final_coefficient = added_frac
                    elif isinstance(final_coefficient, Quotient):
                        added_frac = final_coefficient.add(current_coefficient)
                        if added_frac is None:
                            raise ValueError("Something went wrong when trying to add coefficients that are fractions.", current_coefficient, final_coefficient)
                        
                        final_coefficient = added_frac

            # Not adding it to the list if the coefficient is zero.
            if isinstance(final_coefficient, Constant) and final_coefficient.value == 0:
                continue

            # Add the non-coefficient part back.
            if isinstance(key, Constant):
                combined_terms.append(final_coefficient)
            else:
                if isinstance(final_coefficient, Constant) and final_coefficient.value == 1:
                    combined_terms.append(key.copy())
                else:
                    combined_terms.append(Product(final_coefficient, key.copy()))

        # Rebuild expression tree
        if len(combined_terms) == 0:
            return Constant(0)
        
        if len(combined_terms) == 1:
            return combined_terms[0]
        
        # [2x², 13x, 9]
        def rebuild(parent: Expression, terms: list[Expression], curr: int):
            if curr == len(combined_terms):
                return
            
            curr_expression = terms[curr]
            if isinstance(parent, (Sum, Difference)):
                # Determine if the next expression has a negative.
                # If so, undo the distribution of the negative and create a Difference node.
                is_neg, updated_expression = is_negative(curr_expression)
                if is_neg:
                    parent.right_side = Difference(parent.right_side, updated_expression)

                # Build the expression from left to right. Replace the right side with a new sum node
                # where the left side of that sum node is the old right side of the parent.
                parent.right_side = Sum(parent.right_side, curr_expression)
            elif isinstance(parent, (Product, Quotient)):
                parent.right_side = curr_expression
                if isinstance(parent, Quotient):
                    parent.denominator = parent.right_side
            else:
                # Need to figure out what to do with leaf nodes like constants.
                pass

            # TODO: Implement the recursive case here.
            rebuild(curr_expression, terms, curr + 1)

        def is_negative(expression: Expression) -> tuple[bool, Expression]:
            if isinstance(expression, Constant):
                return (True, expression.additive_inverse()) if expression.value < 0 else (False, expression)
            elif isinstance(expression, Product):
                # Consider the expression negative if its coefficient is negative.
                if isinstance(expression.left_side, Constant) and expression.left_side.value < 0:
                    copy = expression.copy()
                    # Flip the sign
                    copy.left_side = expression.left_side.additive_inverse()

                    return (True, copy)
                else:
                    return (False, expression)
            elif isinstance(expression, Quotient):
                # Consider the expression negative if its coefficient is negative.
                if isinstance(expression.numerator, Constant) and expression.numerator.value < 0:
                    copy = expression.copy()
                    # Flip the sign
                    copy.numerator = expression.numerator.additive_inverse()
                    copy.left_side = copy.numerator

                    return (True, copy)
                else:
                    return (False, expression)
            else:
                return (False, expression)
                
        is_neg, second_term = is_negative(combined_terms[1])
        root = Difference(combined_terms[0], second_term) if is_neg else Sum(combined_terms[0], second_term)
        rebuild(root, combined_terms, 2)

        return root
        
class Sum(AdditiveOperation):
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

class Difference(AdditiveOperation):
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
    def __init__(self, numerator: Expression, denominator: Expression) -> None:
        super().__init__(numerator, "/", denominator)

        self.numerator = numerator
        self.denominator = denominator

    def copy(self):
        return Quotient(self.left_side.copy(), self.right_side.copy())
    
    # 8/10 = 4 / 5
    def simplify(self) -> Constant | Quotient:
        if not isinstance(self.numerator, Constant) or not isinstance(self.denominator, Constant):
            return self.copy()
        
        # Divide the top and bottom if the bottom divides evenly into the top.
        if self.numerator.value % self.denominator.value == 0:
            return Constant(self.numerator.value / self.denominator.value)
        
        greatest_common_factor = 1
        upper_bound = min(int(self.numerator.value), int(self.denominator.value))
        for factor in range(2, upper_bound + 1):
            if self.numerator.value % factor == 0 and self.denominator.value % factor == 0:
                greatest_common_factor = factor
        
        new_numerator = Constant(self.numerator.value / greatest_common_factor)
        new_denominator = Constant(self.denominator.value / greatest_common_factor)
        return Quotient(new_numerator, new_denominator)
    
    # 3/5 + 2/10 = 6/10 + 2/10 = 8/10 = 4 / 5
    def add(self, q2: Quotient) -> Constant | Quotient | None:
        # If the fractions don't add nicely with constants as their denominator,
        # then we just make an immediate exit.
        if not isinstance(self.denominator, Constant) or not isinstance(q2.denominator, Constant):
            return None
        
        lcd = int(max(self.denominator.value, q2.denominator.value))
        start = int(max(self.denominator.value, q2.denominator.value))
        worst_case = int(self.denominator.value * q2.denominator.value)
        for num in range(start, worst_case + 1):
            # If both denominators are factors, we found our lowest common denominator.
            if num % self.denominator.value == 0 and num % q2.denominator.value == 0:
                lcd = num
                break

        q1_multiplier = int(lcd / self.denominator.value)
        q2_multiplier = int(lcd / q2.denominator.value)

        q1_numerator = Constant(self.numerator.value * q1_multiplier) if isinstance(self.numerator, Constant) else Product(Constant(q1_multiplier), self.numerator.copy())
        q2_numerator = Constant(q2.numerator.value * q2_multiplier) if isinstance(q2.numerator, Constant) else Product(Constant(q2_multiplier), q2.numerator.copy())

        if isinstance(q1_numerator, Constant) and isinstance(q2_numerator, Constant):
            numerators_summed = Constant(q1_numerator.value + q2_numerator.value)
            return Quotient(numerators_summed, Constant(lcd)).simplify()
        
        numerators_summed = Sum(q1_numerator, q2_numerator)
        return Quotient(numerators_summed, Constant(lcd))
        

class Power(BinaryOperation):
    def __init__(self, left_side: Expression, right_side: Expression) -> None:
        super().__init__(left_side, "^", right_side)

        self.base = left_side
        self.exponent = right_side

    def copy(self):
        return Power(self.left_side.copy(), self.right_side.copy())
