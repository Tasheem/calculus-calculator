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
    assert str(equation) == "x² / (2 + x)"

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

# x² / (2 + x)
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
    assert isinstance(res.numerator, Power)
    assert isinstance(res.numerator.base, Variable)
    assert isinstance(res.numerator.exponent, Constant)
    assert res.numerator.base.name == "x"
    assert res.numerator.exponent.value == 2
    assert isinstance(res.denominator, Sum)
    assert isinstance(res.denominator.left_side, Constant)
    assert isinstance(res.denominator.right_side, Variable)
    assert res.denominator.left_side.value == 2
    assert res.denominator.right_side.name == "x"

# 2x² + 5x + 7x + 9
# Key: x² -> Value: [2]
# Key: x -> Value: [5, 7]
def test_find_like_terms_1():
    two_deg = Product(Constant(2), Power(Variable("x"), Constant(2)))
    five_x = Product(Constant(5), Variable("x"))
    seven_x = Product(Constant(7), Variable("x"))
    nine = Constant(9)

    left_sum = Sum(two_deg, five_x)
    mid_sum = Sum(left_sum, seven_x)
    equation = Sum(mid_sum, nine)

    map = equation.find_like_terms()

    assert len(map) == 2
    assert "x²" in map
    assert "x" in map
    x_squared_coefficients = map[Power(Variable("x"), Constant(2))]
    assert len(x_squared_coefficients) == 1
    assert x_squared_coefficients[0] == 2
    x_coefficients = map[Variable("x")]
    assert len(x_coefficients) == 2
    assert 5 in x_coefficients
    assert 7 in x_coefficients

# 3sin(x) + 5sin(x) = 8sin(x)
# TODO: Implement after creating unary node representation.
""" def test_find_like_terms_sin():
    pass """

# (3x²)/y + (7x²)/y = (3x² + 7x²)/y
# Key: x² -> Value: [3, 7]
def test_find_like_terms_2():
    numer_1 = Product(Constant(3), Power(Variable("x"), Constant(2)))
    numer_2 = Product(Constant(7), Power(Variable("x"), Constant(2)))

    denom_1 = Variable("y")
    denom_2 = Variable("y")
    
    left = Quotient(numer_1, denom_1)
    right = Quotient(numer_2, denom_2)

    equation = Sum(left, right)
    combined_fracs = equation.combine_fractions()

    assert combined_fracs is not None
    assert isinstance(combined_fracs.numerator, Sum)
    map = combined_fracs.numerator.find_like_terms()

    assert len(map) == 1
    key = Power(Variable("x"), Constant(2))
    assert key in map
    coefficients = map[key]
    assert len(coefficients) == 2
    assert 3 in coefficients
    assert 7 in coefficients

# (3x²)/y + (7x²)/y = (3x² + 7x²)/y
def test_combine_fractions_1():
    numer_1 = Product(Constant(3), Power(Variable("x"), Constant(2)))
    numer_2 = Product(Constant(7), Power(Variable("x"), Constant(2)))

    denom_1 = Variable("y")
    denom_2 = Variable("y")
    
    left = Quotient(numer_1, denom_1)
    right = Quotient(numer_2, denom_2)

    equation = Sum(left, right)
    result = equation.combine_fractions()
    
    assert isinstance(result, Quotient)
    assert isinstance(result.numerator, Sum)
    assert isinstance(result.numerator.left_side, Product)
    assert isinstance(result.numerator.right_side, Product)
    left_numer = result.numerator.left_side
    right_numer = result.numerator.right_side

    # Check for 3x²
    assert isinstance(left_numer.left_side, Constant) and isinstance(left_numer.right_side, Power)
    assert left_numer.left_side == 3
    assert isinstance(left_numer.right_side.base, Variable) and isinstance(left_numer.right_side.exponent, Constant)
    assert left_numer.right_side.base.name == "x" and left_numer.right_side.exponent.value == 2

    # Check for 7x²
    assert isinstance(right_numer.left_side, Constant) and isinstance(right_numer.right_side, Power)
    assert right_numer.left_side == 7
    assert isinstance(right_numer.right_side.base, Variable) and isinstance(right_numer.right_side.exponent, Constant)
    assert right_numer.right_side.base.name == "x" and right_numer.right_side.exponent.value == 2

# (3x²)/y - (7x²)/y = (3x² - 7x²)/y
def test_combine_fractions_2():
    numer_1 = Product(Constant(3), Power(Variable("x"), Constant(2)))
    numer_2 = Product(Constant(7), Power(Variable("x"), Constant(2)))

    denom_1 = Variable("y")
    denom_2 = Variable("y")
    
    left = Quotient(numer_1, denom_1)
    right = Quotient(numer_2, denom_2)

    equation = Difference(left, right)
    result = equation.combine_fractions()
    
    assert isinstance(result, Quotient)
    assert isinstance(result.numerator, Difference)
    assert isinstance(result.numerator.left_side, Product)
    assert isinstance(result.numerator.right_side, Product)
    left_numer = result.numerator.left_side
    right_numer = result.numerator.right_side

    # Check for 3x²
    assert isinstance(left_numer.left_side, Constant) and isinstance(left_numer.right_side, Power)
    assert left_numer.left_side == 3
    assert isinstance(left_numer.right_side.base, Variable) and isinstance(left_numer.right_side.exponent, Constant)
    assert left_numer.right_side.base.name == "x" and left_numer.right_side.exponent.value == 2

    # Check for 7x²
    assert isinstance(right_numer.left_side, Constant) and isinstance(right_numer.right_side, Power)
    assert right_numer.left_side == 7
    assert isinstance(right_numer.right_side.base, Variable) and isinstance(right_numer.right_side.exponent, Constant)
    assert right_numer.right_side.base.name == "x" and right_numer.right_side.exponent.value == 2