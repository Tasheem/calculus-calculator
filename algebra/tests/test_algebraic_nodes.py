from algebra.models.algebraic_nodes import *

# (2 + 4)
def test_str_1():
    two = Constant(2)
    four = Constant(4)
    sum = Sum(two, four)

    assert str(sum) == "2 + 4"