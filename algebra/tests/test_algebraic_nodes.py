from algebra.models.algebraic_nodes import *

def test_str_1():
    two = Constant(2)
    four = Constant(4)
    sum = Sum(two, four)

    assert str(sum) == "2 + 4"

def test_str_2():
    five = Constant(5)
    eight = Constant(8)
    twelve = Constant(12)
    three = Constant(3)

    left = Sum(five, eight)
    right = Sum(twelve, three)
    equation = Difference(left, right)

    assert str(equation) == "(5 + 8) - (12 + 3)"

def test_str_3():
    x = Variable("x")
    two = Constant(2)
    y = Variable("y")
    one = Constant(1)

    left = Sum(x, two)
    right = Difference(y, one)
    equation = Difference(left, right)

    assert str(equation) == "(x + 2) - (y - 1)"

def test_str_4():
    x = Variable("x")
    two = Constant(2)
    x_squared = Power(x, two)
    
    two_bottom = Constant(2)
    x_bottom = Variable("x")
    two_x = Sum(two_bottom, x_bottom)

    equation = Quotient(x_squared, two_x)
    assert str(equation) == "x^2 / (2 + x)"

# 2 + 4
def test_compute_1():
    two = Constant(2)
    four = Constant(4)
    sum = Sum(two, four)

    res = sum.compute()
    assert isinstance(res, Constant)
    assert res.value == 6

# (5 + 8) - (12 + 3)
def test_compute_2():
    five = Constant(5)
    eight = Constant(8)
    twelve = Constant(12)
    three = Constant(3)

    left = Sum(five, eight)
    right = Sum(twelve, three)
    equation = Difference(left, right)

    res = equation.compute()
    assert isinstance(res, Constant)
    assert res.value == -2

# (x + 2) - (8 - 1)
def test_compute_3():
    x = Variable("x")
    two = Constant(2)
    eight = Constant(8)
    one = Constant(1)

    left = Sum(x, two)
    right = Difference(eight, one)
    equation = Difference(left, right)

    res = equation.compute()
    assert isinstance(res, Difference)
    assert isinstance(res.left_side, Sum)
    assert isinstance(res.right_side, Constant)
    
    assert isinstance(res.left_side.left_side, Variable)
    assert isinstance(res.left_side.right_side, Constant)
    assert res.left_side.left_side.name == "x"
    assert res.left_side.right_side.value == 2

    assert res.right_side.value == 7

# x^2 / (2 + x)
# Need to combine like terms
def test_compute_4():
    x = Variable("x")
    two = Constant(2)
    x_squared = Power(x, two)
    
    two_bottom = Constant(2)
    x_bottom = Variable("x")
    two_x = Sum(two_bottom, x_bottom)

    equation = Quotient(x_squared, two_x)
    res = equation.compute()

    assert isinstance(res, Quotient)
    assert isinstance(res.left_side, Variable)
    assert isinstance(res.right_side, Constant)
    
    assert res.left_side.name == "x"
    assert res.right_side.value == 2
