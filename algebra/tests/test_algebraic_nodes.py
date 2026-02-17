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
# Key: 1 -> Value: [9]
def test_find_like_terms_1():
    two_deg = Product(Constant(2), Power(Variable("x"), Constant(2)))
    five_x = Product(Constant(5), Variable("x"))
    seven_x = Product(Constant(7), Variable("x"))
    nine = Constant(9)

    left_sum = Sum(two_deg, five_x)
    mid_sum = Sum(left_sum, seven_x)
    equation = Sum(mid_sum, nine)

    map = equation.find_like_terms()

    assert len(map) == 3
    assert "x²" in map
    assert "x" in map
    assert "1" in map

    x_squared_coefficients = map[Power(Variable("x"), Constant(2))]
    assert len(x_squared_coefficients) == 1
    assert isinstance(x_squared_coefficients[0], Constant) and x_squared_coefficients[0].value == 2

    x_coefficients = map[Variable("x")]
    assert len(x_coefficients) == 2
    assert Constant(5) in x_coefficients
    assert Constant(7) in x_coefficients

    constants = map[Constant(1)]
    assert len(constants) == 1
    assert Constant(9) in constants

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

# 2x² + (1/2)x + (3/5)x + 9
# Key: x² -> Value: [2]
# Key: x -> Value: [(1/2), (3/5)]
# Key: 1 -> Value: [9]
def test_find_like_terms_3():
    two_deg = Product(Constant(2), Power(Variable("x"), Constant(2)))
    half_x = Product(Quotient(Constant(1), Constant(2)), Variable("x"))
    three_fifth_x = Product(Quotient(Constant(3), Constant(5)), Variable("x"))
    nine = Constant(9)

    left_sum = Sum(two_deg, half_x)
    mid_sum = Sum(left_sum, three_fifth_x)
    equation = Sum(mid_sum, nine)

    map = equation.find_like_terms()

    assert len(map) == 3
    assert "x²" in map
    assert "x" in map
    assert "1" in map

    x_squared_coefficients = map[Power(Variable("x"), Constant(2))]
    assert len(x_squared_coefficients) == 1
    assert isinstance(x_squared_coefficients[0], Constant) and x_squared_coefficients[0].value == 2

    x_coefficients = map[Variable("x")]
    assert len(x_coefficients) == 2
    assert Quotient(Constant(1), Constant(2)) in x_coefficients
    assert Quotient(Constant(3), Constant(5)) in x_coefficients

    constants = map[Constant(1)]
    assert len(constants) == 1
    assert Constant(9) in constants

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

# 3x + 5x = 8x
def test_combine_like_terms_1():
    left = Product(Constant(3), Variable("x"))
    right = Product(Constant(5), Variable("x"))
    equation = Sum(left, right)
    
    result = equation.combine_like_terms()
    assert isinstance(result, Product)
    assert isinstance(result.left_side, Constant) and isinstance(result.right_side, Variable)
    assert result.left_side.value == 8 and result.right_side.name == "x"

# x + x = 2x
def test_combine_like_terms_2():
    x = Variable("x")
    equation = Sum(x, x.copy())

    result = equation.combine_like_terms()
    assert isinstance(result, Product)
    assert isinstance(result.left_side, Constant) and isinstance(result.right_side, Variable)
    assert result.left_side.value == 2 and result.right_side.name == "x"

# -3x + 5x = 2x
def test_combine_like_terms_3():
    left = Product(Constant(-3), Variable("x"))
    right = Product(Constant(5), Variable("x"))
    equation = Sum(left, right)

    result = equation.combine_like_terms()
    assert isinstance(result, Product)
    assert isinstance(result.left_side, Constant) and isinstance(result.right_side, Variable)
    assert result.left_side.value == 2 and result.right_side.name == "x"

# 3x - 5x = -2x
def test_combine_like_terms_4():
    left = Product(Constant(3), Variable("x"))
    right = Product(Constant(5), Variable("x"))
    equation = Difference(left, right)

    result = equation.combine_like_terms()
    assert isinstance(result, Product)
    assert isinstance(result.left_side, Constant) and isinstance(result.right_side, Variable)
    assert result.left_side.value == -2 and result.right_side.name == "x"

# 3x² + 5x
# Cannot combine
def test_combine_like_terms_5():
    left = Product(Constant(3), Power(Variable("x"), Constant(2)))
    right = Product(Constant(5), Variable("x"))
    equation = Sum(left, right)

    result = equation.combine_like_terms()
    assert result is None

# x³ + x²
# Cannot combine
def test_combine_like_terms_6():
    left = Power(Variable("x"), Constant(3))
    right = Power(Variable("x"), Constant(2))
    equation = Sum(left, right)

    result = equation.combine_like_terms()
    assert result is None

# x² + x² = 2x²
def test_combine_like_terms_7():
    left = Power(Variable("x"), Constant(2))
    right = Power(Variable("x"), Constant(2))
    equation = Sum(left, right)

    result = equation.combine_like_terms()
    assert isinstance(result, Product)
    assert isinstance(result.left_side, Constant) and isinstance(result.right_side, Power)
    assert result.left_side.value == 2
    power = result.right_side
    assert isinstance(power.base, Variable) and isinstance(power.exponent, Constant)
    assert power.base.name == "x" and power.exponent.value == 2

# 3x² + 5x + 2x² + 7x = 5x² + 12x
def test_combine_like_terms_8():
    equation = Sum(
        Product(Constant(3), Power(Variable("x"), Constant(2))),
        Sum(
            Product(Constant(5), Variable("x")),
            Sum(
                Product(Constant(2), Power(Variable("x"), Constant(2))),
                Product(Constant(7), Variable("x")),
            )
        )
    )

    result = equation.combine_like_terms()
    assert isinstance(result, Sum)
    assert isinstance(result.left_side, Product) and isinstance(result.right_side, Product)

    five_x_squared = result.left_side
    assert isinstance(five_x_squared.left_side, Constant) and isinstance(five_x_squared.right_side, Power)
    x_squared = five_x_squared.right_side
    assert isinstance(x_squared.base, Variable) and isinstance(x_squared.exponent, Constant)
    assert five_x_squared.left_side.value == 5 and x_squared.base.name == "x" and x_squared.exponent.value == 2
    
    twelve_x = result.right_side
    assert isinstance(twelve_x.left_side, Constant) and isinstance(twelve_x.right_side, Variable)
    assert twelve_x.left_side.value == 12 and twelve_x.right_side.name == "x"

# x³ + 2x² + 3x³ + x² = 4x³ + 3x²
def test_combine_like_terms_9():
    equation = Sum(
        Power(Variable("x"), Constant(3)),
        Sum(
            Product(Constant(2), Power(Variable("x"), Constant(2))),
            Sum(
                Product(Constant(3), Power(Variable("x"), Constant(3))),
                Power(Variable("x"), Constant(2))
            )
        )
    )

    result = equation.combine_like_terms()
    assert isinstance(result, Sum)
    assert isinstance(result.left_side, Product) and isinstance(result.right_side, Product)

    four_x_cubed = result.left_side
    assert isinstance(four_x_cubed.left_side, Constant) and isinstance(four_x_cubed.right_side, Power)
    x_cubed = four_x_cubed.right_side
    assert isinstance(x_cubed.base, Variable) and isinstance(x_cubed.exponent, Constant)
    assert four_x_cubed.left_side.value == 4 and x_cubed.base.name == "x" and x_cubed.exponent.value == 3
    
    three_x_squared = result.right_side
    assert isinstance(three_x_squared.left_side, Constant) and isinstance(three_x_squared.right_side, Power)
    x_squared = three_x_squared.right_side
    assert isinstance(x_squared.base, Variable) and isinstance(x_squared.exponent, Constant)
    assert three_x_squared.left_side.value == 3 and x_squared.base.name == "x" and x_squared.exponent.value == 2

# (1/2)x + (1/2)x = x
def test_combine_like_terms_10():
    left = Product(Quotient(Constant(1), Constant(2)), Variable("x"))
    right = Product(Quotient(Constant(1), Constant(2)), Variable("x"))
    equation = Sum(left, right)

    result = equation.combine_like_terms()
    assert isinstance(result, Variable)
    assert result.name == "x"

# (1/2)x + (1/3)x = (5/6)x
def test_combine_like_terms_11():
    left = Product(Quotient(Constant(1), Constant(2)), Variable("x"))
    right = Product(Quotient(Constant(1), Constant(3)), Variable("x"))
    equation = Sum(left, right)

    result = equation.combine_like_terms()
    assert isinstance(result, Product)
    assert isinstance(result.left_side, Quotient) and isinstance(result.right_side, Variable)
    assert isinstance(result.left_side.numerator, Constant) and isinstance(result.left_side.denominator, Constant)
    assert result.left_side.numerator.value == 5 and result.left_side.denominator.value == 6 and result.right_side.name == "x"

# 2x + (1/2)x = (5/2)x
def test_combine_like_terms_12():
    left = Product(Constant(2), Variable("x"))
    right = Product(Quotient(Constant(1), Constant(2)), Variable("x"))
    equation = Sum(left, right)

    result = equation.combine_like_terms()
    assert isinstance(result, Product)
    assert isinstance(result.left_side, Quotient) and isinstance(result.right_side, Variable)
    q = result.left_side
    assert isinstance(q.numerator, Constant) and isinstance(q.denominator, Constant)
    assert q.numerator.value == 5 and q.denominator.value == 2 and result.right_side.name == "x"

# -3x - 5x = -8x
def test_combine_like_terms_13():
    left = Product(Constant(-3), Variable("x"))
    right = Product(Constant(5), Variable("x"))
    equation = Difference(left, right)

    result = equation.combine_like_terms()
    assert isinstance(result, Product)
    assert isinstance(result.left_side, Constant) and isinstance(result.right_side, Variable)
    assert result.left_side.value == -8 and result.right_side.name == "x"

# 5x - 3x = 2x
def test_combine_like_terms_14():
    left = Product(Constant(5), Variable("x"))
    right = Product(Constant(3), Variable("x"))
    equation = Difference(left, right)

    result = equation.combine_like_terms()
    assert isinstance(result, Product)
    assert isinstance(result.left_side, Constant) and isinstance(result.right_side, Variable)
    assert result.left_side.value == 2 and result.right_side.name == "x"

# 3x - 3x = 0
def test_combine_like_terms_15():
    left = Product(Constant(3), Variable("x"))
    right = Product(Constant(3), Variable("x"))
    equation = Difference(left, right)

    result = equation.combine_like_terms()
    assert isinstance(result, Constant)
    assert result.value == 0

# 5x² - 5x² = 0
def test_combine_like_terms_16():
    left = Product(Constant(5), Power(Variable("x"), Constant(2)))
    right = Product(Constant(5), Power(Variable("x"), Constant(2)))
    equation = Difference(left, right)

    result = equation.combine_like_terms()
    assert isinstance(result, Constant)
    assert result.value == 0

# Adding fractions can reveal like terms that weren't obvious before:
# x/2 + x/3
# = 3x/6 + 2x/6    # Find common denominator
# = (3x + 2x)/6     # Add fractions
# = 5x/6            # Combine like terms in numerator
def test_combine_like_terms_17():
    left = Quotient(Variable("x"), Constant(2))
    right = Quotient(Variable("x"), Constant(3))
    equation = Sum(left, right)

    result = equation.combine_like_terms()
    assert isinstance(result, Quotient)
    assert isinstance(result.numerator, Product) and isinstance(result.denominator, Constant)
    assert isinstance(result.numerator.left_side, Constant) and isinstance(result.numerator.right_side, Variable)
    assert result.numerator.left_side.value == 5 and result.numerator.right_side.name == "x" and result.denominator.value == 6
