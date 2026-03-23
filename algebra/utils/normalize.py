from models.atomic_nodes import *
from models.algebraic_nodes import *

def normalize(expression: Expression):
    """
    Structural/Normalization Rules:

    Pass 1: Recursive Descent Normalization
    - Recurse to leaf nodes and normalize upward.
    - This guarantees that any given node will have its subtree already normalized.

    Pass 2: Normalize negation and subtraction
    - Distribute `Difference` nodes so that they no longer exist in subsequent passes.
    - This should result in `Sum` nodes with a `Product` child with `Constant(-1)` as its left child.

    Pass 3: Flatten Nested Associative Operations
    - `Sum` nodes need to be flattened to N-ary `Sum` nodes.
    - `Product` nodes need to be flattened to N-ary `Product` nodes.

    Pass 4: Expand Products Over Sums
    - Distribute Product to each child in the `Sum`.
        - And the `Sum` must be a direct node.

    Pass 5: Collect Like Terms
    - Merge `Sum` children that share the same symbolic part.
        - The `combine_like_terms()` method from the `AdditiveOperation` class can be used.

    Pass 6: Sort Children Canonically
    - Order:
        - Sort by Degree:
            - Compound nodes come first.
                - Any node in which the degree cannot be determined will fall into this category.
            - Power nodes with coefficients.
                - So degree 2 and higher.
            - Variable nodes.
                - These satisfy degree 1.
            - Constants.
                - These statisfy degree 0.
        - Sort Variable letters:
            - So x² and x should come before y² and y.

    Pass 7: Simplify Trivial Cases and Promote `Polynomial`
    - Sum with one child → replace the Sum node with that child directly
    - Product with one child → same
    - Product containing a Constant(0) → replace the entire node with Constant(0)
    - Product containing a Constant(1) → remove that child
    - Sum containing a Constant(0) → remove that child
    - Quotient with denominator Constant(1) → replace with numerator
    - Constant nodes that are the result of an operation on two other Constant nodes → evaluate numerically and collapse to a single Constant
    """
    return _normalize(expression)

def _normalize(expression: Expression):
    if isinstance(expression, Atomic):
        return expression.copy()
    elif isinstance(expression, BinaryOperation):
        expression.left_side = _normalize(expression.left_side)
        expression.right_side = _normalize(expression.right_side)

    # Pass 2
    updated_expression = eliminate_difference(expression)

    # Pass 3
    updated_expression = flatten_sums_products(updated_expression)

    # Pass 4
    updated_expression = expand_product_over_sums(updated_expression)

    # Pass 5
    updated_expression = combine_like_terms(updated_expression)

    # TODO: Implement passes 6-7

    return updated_expression

def eliminate_difference(expression: Expression) -> Expression:
    """
    This function transforms `Difference` nodes into `Product(-1, expression)` nodes.
    """
    # Ex: 2 - (4 * x) -> 2 + -1(4 * x)
    if isinstance(expression, Difference):
        return Sum(expression.left_side, Product(Constant(-1), expression.right_side))
    
    return expression

def flatten_sums_products(expression: Expression) -> Expression:
    """
    This function flattens nested `Product` and `Sum` nodes since they are associative operations. This function only combines direct children
    with their parent node, since pass 1 recurses and guarantees that grandchild nodes are already flattened.\n

    N-ary nodes are also taken into account since they're being constructed on the way back up the expression tree.
    """
    if not isinstance(expression, (Sum, Product)):
        return expression.copy()
    
    nodes: list[Expression] = []
    def add_children(child: Expression):
        if (isinstance(expression, Sum) and isinstance(child, Sum)) or (isinstance(expression, Product) and isinstance(child, Product)):
            nodes.append(child.left_side)
            nodes.append(child.right_side)
        elif isinstance(child, (FlatSum, FlatProduct)) and child.is_n_ary_equivalent(expression):
            nodes.extend(child.operands)
        else:
            nodes.append(child)

    add_children(expression.left_side)
    add_children(expression.right_side)

    if len(nodes) == 2:
        # Keep binary nodes if there aren't nested sums or products.
        return Sum(nodes[0], nodes[1]) if isinstance(expression, Sum) else Product(nodes[0], nodes[1])

    return FlatSum(nodes) if isinstance(expression, Sum) else FlatProduct(nodes)

def expand_product_over_sums(expression: Expression):
    """
    This function applies the distributive law to expand products over sums.
    """
    if isinstance(expression, Product):
        if isinstance(expression.left_side, Sum) and isinstance(expression.right_side, Sum):
            return foil(expression.left_side, expression.right_side)
        elif isinstance(expression.left_side, Sum):
            return multiply_across(expression.right_side, expression.left_side)
        
        multiplied = multiply_to_expand(expression.left_side, expression.right_side)
        return expression.copy() if multiplied is None else multiplied
    elif isinstance(expression, BinaryOperation):
        left_updated = expand_product_over_sums(expression.left_side)
        right_updated = expand_product_over_sums(expression.right_side)

        expression.left_side = left_updated
        expression.right_side = right_updated

        return expression.copy()
    
    return expression.copy()
    
def multiply_across(left_side: Expression, sum: Sum | FlatSum):
    """
    This function multiplies one expression over each operand in a `Sum` or `FlatSum` expression.
    """
    sum_operands = [sum.left_side, sum.right_side] if isinstance(sum, Sum) else sum.operands
    result: list[Expression] = []

    for operand in sum_operands:
        curr_res = multiply_to_expand(left_side, operand)
        if curr_res is None:
            raise ValueError("Something went wrong when multiplying a product across a sum.", left_side, operand)
        
        if isinstance(curr_res, Constant) and curr_res.value == 0:
            continue
        
        result.append(curr_res)
    
    if len(result) == 2:
        return Sum(result[0], result[1])
    
    return FlatSum(result)

def foil(left_side: Sum, right_side: Sum):
    # FOIL
    operands = []
    # First
    first_left = left_side.left_side
    first_right = right_side.left_side
    first_res = multiply_to_expand(first_left, first_right)
    if first_res is None:
        raise ValueError("Something went wrong with the F-operation when using the FOIL method in multiply_to_expand().")
    
    operands.append(first_res)
    # Outside
    outside_left = left_side.left_side
    outside_right = right_side.right_side
    outside_res = multiply_to_expand(outside_left, outside_right)
    if outside_res is None:
        raise ValueError("Something went wrong with the O-operation when using the FOIL method in multiply_to_expand().")
    
    operands.append(outside_res)
    # Inside
    inside_left = left_side.right_side
    inside_right = right_side.left_side
    inside_res = multiply_to_expand(inside_left, inside_right)
    if inside_res is None:
        raise ValueError("Something went wrong with the O-operation when using the FOIL method in multiply_to_expand().")
    
    operands.append(inside_res)
    # Last
    inside_left = left_side.right_side
    inside_right = right_side.right_side
    inside_res = multiply_to_expand(inside_left, inside_right)
    if inside_res is None:
        raise ValueError("Something went wrong with the O-operation when using the FOIL method in multiply_to_expand().")
    
    operands.append(inside_res)

    return FlatSum(operands)

def multiply_to_expand(left_side: Expression, right_side: Expression):
    if (isinstance(left_side, Constant) and left_side == 0) or (isinstance(right_side, Constant) and right_side.value == 0):
        return Constant(0)

    # Multiply two expressions and return the result.
    if isinstance(left_side, Constant) and isinstance(right_side, Constant):
        return Constant(left_side.value * right_side.value)
    elif isinstance(left_side, Quotient) and isinstance(right_side, Quotient):
        return left_side.multiply(right_side)
    elif isinstance(left_side, (Constant, Quotient)) and isinstance(right_side, Variable):
        return Product(left_side.copy(), right_side.copy())
    elif isinstance(left_side, Variable) and isinstance(right_side, (Constant, Quotient)):
        return Product(right_side.copy(), left_side.copy())
    elif isinstance(left_side, (Constant, Quotient)) and isinstance(right_side, Power):
        return Product(left_side.copy(), right_side.copy())
    elif isinstance(left_side, Power) and isinstance(right_side, (Constant, Quotient)):
        return Product(right_side.copy(), left_side.copy())
    elif isinstance(left_side, Variable) and isinstance(right_side, Variable):
        if left_side.name == right_side.name:
            return Power(left_side.copy(), Constant(2))
        else:
            return Product(left_side.copy(), right_side.copy())
    elif isinstance(left_side, Power) and isinstance(right_side, Power):
        return left_side.multiply(right_side)
    else:
        return None
    
def combine_like_terms(expression: Expression):
    if isinstance(expression, (Sum, FlatSum)):
        return expression.combine_like_terms()
    elif isinstance(expression, BinaryOperation):
        # Traverse tree to find more Sum or FlatSum nodes.
        updated_left = combine_like_terms(expression.left_side)
        updated_right = combine_like_terms(expression.right_side)

        expression.left_side = updated_left
        expression.right_side = updated_right

    return expression
    