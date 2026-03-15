from algebra.models.atomic_nodes import *
from algebra.models.atomic_nodes import Expression

class NAryNode(Expression):
    def __init__(self, children: list[Expression]) -> None:
        super().__init__()
        if len(children) < 2:
            raise ValueError("An N-Ary node cannot contain less than 2 children.")

        self._children = children

    def compute(self) -> Expression:
        return Constant(0)
    
    def add_node(self, node: Expression):
        self._children.append(node)

class NArySum(NAryNode):
    def __init__(self, children: list[Expression]) -> None:
        super().__init__(children)

class NAryProduct(NAryNode):
    def __init__(self, children: list[Expression]) -> None:
        super().__init__(children)