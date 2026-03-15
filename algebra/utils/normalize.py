from models.atomic_nodes import *
from models.algebraic_nodes import *
from models.n_ary_nodes import *

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
    - Keep recursing and distrubuting to `Sum` nodes if there are more nested deeper in the tree.

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
    updated_expression = flatten_node(expression)

    # TODO: Implement passes 4-7

    return updated_expression

def eliminate_difference(expression: Expression) -> Expression:
    """
    This function transforms `Difference` nodes into `Product(-1, expression)` nodes.
    """
    # Ex: 2 - (4 * x) -> 2 + -1(4 * x)
    if isinstance(expression, Difference):
        return Sum(expression.left_side, Product(Constant(-1), expression.right_side))
    
    return expression

def flatten_node(expression: Expression) -> Expression:
    """
    This function flattens `Product` and `Sum` nodes. This function only combines direct children
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
        elif isinstance(child, NAryNode) and child.is_n_ary_equivalent(expression):
            nodes.extend(child.operands)
        else:
            nodes.append(child)

    add_children(expression.left_side)
    add_children(expression.right_side)

    if len(nodes) == 2:
        # Keep binary nodes if there aren't nested sums or products.
        return Sum(nodes[0], nodes[1]) if isinstance(expression, Sum) else Product(nodes[0], nodes[1])

    return FlatSum(nodes) if isinstance(expression, Sum) else FlatProduct(nodes)
