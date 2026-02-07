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
