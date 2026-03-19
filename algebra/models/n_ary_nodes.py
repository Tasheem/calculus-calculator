from algebra.models.atomic_nodes import *
from algebra.models.algebraic_nodes import *

class NAryNode(Expression):
    def __init__(self, operands: list[Expression]) -> None:
        super().__init__()
        if len(operands) < 2:
            raise ValueError("An N-Ary node cannot contain less than 2 operands.")

        self.operands = operands

    def compute(self) -> Expression:
        return Constant(0)
    
    def copy(self):
        return FlatSum(self.operands) if isinstance(self, FlatSum) else FlatProduct(self.operands)
    
    def is_n_ary_equivalent(self, node: Expression) -> bool:
        return False