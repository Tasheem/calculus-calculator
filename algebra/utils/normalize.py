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
    - This should result in `Sum` nodes with either of these two children:
        - A negative `Constant` child.
        - A `Product` child with `Constant(-1)` as its left child.

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
    pass

def _normalize(expression: Expression):
    pass

def distribute_minus(node: Difference):
    """
    Distribute a negative to the right side of a `Difference` node and its subtree.
    Return a `Sum` node with the subtree updated with the negative applied.
    """
    def traverse_and_distribute(expression: Expression | None, distribute: bool):
        if expression is None:
            return
        
        if isinstance(expression, Constant):
            return expression.additive_inverse() if distribute else expression
        elif isinstance(expression, Variable):
            return Product(Constant(-1), expression.copy()) if distribute else expression
        elif isinstance(expression, Sum):
            left_subtree = traverse_and_distribute(expression.left_side, distribute)
            right_subtree = traverse_and_distribute(expression.right_side, distribute)

            return Sum(left_subtree, right_subtree)
        elif isinstance(expression, Difference):
            """
            Example passing negative to nested expression: 2 - (5 - 3) -> 2 - 5 + 3
            Represented this way in the tree: 2 + -5 + 3

            Example with multiple nested sums and differences:
            Distributing:
            2 - (5 - (4 + 1)) -> 2 - (5 + -4 + -1) -> 2 + -5 + 4 + 1 = -3 + 5 = 2
            Just evaluating the constants using PEMDAS gives the same answer, so distributing should be valid.
            2 - (5 - (4 + 1)) -> 2 - (5 - 5) -> 2 - 0 = 2
            """

            # Distribute current `Difference` negative and transform to a `Sum` node.
            left_subtree = traverse_and_distribute(expression.left_side, False)
            right_subtree = traverse_and_distribute(expression.right_side, True)

            transformed_node = Sum(left_subtree, right_subtree)
            if distribute:
                # Distribute negative over the subtrees again for the parent node's negative.
                return Sum(traverse_and_distribute(transformed_node.left_side, True), traverse_and_distribute(transformed_node.right_side, True))
            else:
                return transformed_node
        elif isinstance(expression, Power):
            """
            Example: 2 - x² -> 2 + -1*(x²)
            """
            if distribute:
                return Product(Constant(-1), expression)
            else:
                return expression
        elif isinstance(expression, Product):
            """
            Example: 2 - 5x³ -> 2 + -5x³
            Example: 2 - (x - 1)(x + 1) ->
            """
            if distribute:
                # Only distribute along the left subtree
                pass
