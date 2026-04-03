from algebra.utils.normalize import *

def test_eliminate_difference_1():
    a, b = Constant(5), Constant(3)
    equation = Difference(a, b)
    result = eliminate_difference(equation)

    assert result == Sum(a, Product(Constant(-1), b))

def test_eliminate_difference_2():
    # Negation of a Sum
    equation = Difference(Constant(0), Sum(Variable("x"), Constant(1)))
    result = eliminate_difference(equation)

    assert result == Sum(Constant(0), Product(Constant(-1), Sum(Variable("x"), Constant(1))))

def test_eliminate_difference_3():
    # Negation of a Product
    equation = Difference(Constant(0), Product(Variable("x"), Variable("y")))
    result = eliminate_difference(equation)

    assert result == Sum(Constant(0), Product(Constant(-1), Product(Variable("x"), Variable("y"))))
    
def test_eliminate_difference_4():
    equation = Difference(Constant(0), Quotient(Variable("x"), Variable("y")))
    result = eliminate_difference(equation)

def test_eliminate_difference_5():
    # Negation of a Power
    equation = Difference(Constant(0), Power(Variable("x"), Constant(2)))
    result = eliminate_difference(equation)

    assert result ==  Sum(Constant(0), Product(Constant(-1), Power(Variable("x"), Constant(2))))

def test_eliminate_difference_6():
    equation = Difference(Variable("a"), Sum(Variable("b"), Product(Constant(-1), Variable("c"))))
    result = eliminate_difference(equation)

    assert result == Sum(Variable("a"), Product(Constant(-1), Sum(Variable("b"), Product(Constant(-1), Variable("c")))))

def test_eliminate_difference_7():
    equation = Difference(Constant(2), Product(Sum(Variable("x"), Constant(-1)), Sum(Variable("x"), Constant(1))))
    result = eliminate_difference(equation)
    
    assert result == Sum(Constant(2), Product(Constant(-1), Product(Sum(Variable("x"), Constant(-1)), Sum(Variable("x"), Constant(1)))))

def test_flatten_sum_products_1():
    # Basic `Sum` flattening
    equation = Sum(Variable("x"), Sum(Variable("y"), Variable("z")))
    result = flatten_sums_products(equation)

    assert result == FlatSum([Variable("x"), Variable("y"), Variable("z")])

def test_flatten_sum_products_2():
    equation = Product(Variable("x"), Product(Variable("y"), Variable("z")))
    result = flatten_sums_products(equation)

    assert result ==  FlatProduct([Variable("x"), Variable("y"), Variable("z")])

def test_flatten_sum_products_3():
    equation = Sum(Sum(Variable("x"), Variable("y")), Sum(Variable("z"), Constant(1)))
    result = flatten_sums_products(equation)

    assert result == FlatSum([Variable("x"), Variable("y"), Variable("z"), Constant(1)])

def test_flatten_sum_products_4():
    equation = Product(Product(Variable("x"), Variable("y")), Product(Variable("z"), Constant(2)))
    result = flatten_sums_products(equation)

    assert result == FlatProduct([Variable("x"), Variable("y"), Variable("z"), Constant(2)])

def test_flatten_sum_products_5():
    equation = Product(Variable("x"), Sum(Variable("y"), Variable("z")))
    result = flatten_sums_products(equation)

    assert result == Product(Variable("x"), Sum(Variable("y"), Variable("z")))

def test_flatten_sum_products_6():
    equation = Sum(Variable("x"), Product(Variable("y"), Variable("z")))
    result = flatten_sums_products(equation)

    assert result == Sum(Variable("x"), Product(Variable("y"), Variable("z")))

def test_flatten_sum_products_7():
    equation = Power(Variable("x"), Constant(2))
    result = flatten_sums_products(equation)

    assert result == Power(Variable("x"), Constant(2))
