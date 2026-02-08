from algebra.models.polynomial import *

# x + 5
def test_construct_from_expression_1():
    x = Variable("x")
    five = Constant(5)
    equation = Sum(x, five)
    p = Polynomial(equation)
    
    assert p.variable is not None and p.variable.name == "x"
    assert p.degree() == 1
    assert p.coefficients[1].value == 1
    assert p.coefficients[0].value == 5

# 3x - 2
def test_construct_from_expression_2():
    product = Product(Constant(3), Variable("x"))
    two = Constant(2)
    equation = Difference(product, two)
    p = Polynomial(equation)

    assert p.variable is not None and p.variable.name == "x"
    assert p.degree() == 1
    assert p.coefficients[1].value == 3
    assert p.coefficients[0].value == -2

# t² - 4t + 2
def test_construct_from_expression_3():
    two_deg = Power(Variable("t"), Constant(2))
    one_deg = Product(Constant(4), Variable("t"))
    zero_deg = Constant(2)

    equation = Sum(Difference(two_deg, one_deg), zero_deg)
    p = Polynomial(equation)

    assert p.variable is not None and p.variable.name == "t"
    assert p.degree() == 2
    assert p.coefficients[2].value == 1
    assert p.coefficients[1].value == -4
    assert p.coefficients[0].value == 2

# 5t³ + 2t² - 16t - 8
def test_construct_from_expression_4():
    three_deg = Product(Constant(5), Power(Variable("t"), Constant(3)))
    two_deg = Product(Constant(2), Power(Variable("t"), Constant(2)))
    one_deg = Product(Constant(16), Variable("t"))
    zero_deg = Constant(8)
    
    # Evalutate from left to right since add and subtract take equal precendence in PEMDAS.
    add_three_two = Sum(three_deg, two_deg)
    sub_res_one = Difference(add_three_two, one_deg)
    sub_res_zero = Difference(sub_res_one, zero_deg)
    p = Polynomial(sub_res_zero)

    assert p.variable is not None and p.variable.name == "t"
    assert p.degree() == 3
    assert p.coefficients[3].value == 5
    assert p.coefficients[2].value == 2
    assert p.coefficients[1].value == -16
    assert p.coefficients[0].value == -8

# 2x² - 1
def test_construct_from_expression_5():
    two_deg = Product(Constant(2), Power(Variable("x"), Constant(2)))
    zero_deg = Constant(1)

    equation = Difference(two_deg, zero_deg)
    p = Polynomial(equation)

    assert p.variable is not None and p.variable.name == "x"
    assert p.degree() == 2
    assert p.coefficients[2].value == 2
    assert p.coefficients[1].value == 0
    assert p.coefficients[0].value == -1

# x² * 2x + 1
def test_construct_from_expression_6():
    two_deg = Power(Variable("x"), Constant(2))
    one_deg = Product(Constant(2), Variable("x"))
    zero_deg = Constant(1)

    equation = Sum(Product(two_deg, one_deg), zero_deg)
    
    try:
        p = Polynomial(equation)
        assert False
    except:
        assert True
