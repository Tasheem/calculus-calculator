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

def test_expand_products_over_sums_1():
    # Basic distribution
    equation = Product(Variable("x"), Sum(Variable("y"), Variable("z")))
    result = expand_product_over_sums(equation)

    assert result == Sum(Product(Variable("x"), Variable("y")), Product(Variable("x"), Variable("z")))

def test_expand_products_over_sums_2():
    # Distribution with a Constant
    equation = Product(Constant(2), Sum(Variable("x"), Constant(1)))
    result = expand_product_over_sums(equation)

    assert result == Sum(Product(Constant(2), Variable("x")), Product(Constant(2), Constant(1)))

def test_expand_products_over_sums_3():
    # Distribution with Constant(-1)
    equation = Product(Constant(-1), Sum(Variable("x"), Constant(1)))
    result = expand_product_over_sums(equation)

    assert result == Sum(Product(Constant(-1), Variable("x")), Product(Constant(-1), Constant(1)))

def test_expand_products_over_sums_4():
    # Two Sum Children in a Product
    # (x + 1)(x - 1) -> x² - x + x - 1
    equation = Product(Sum(Variable("x"), Constant(1)), Sum(Variable("x"), Constant(-1)))
    result = expand_product_over_sums(equation)
    answer = Sum(Sum(Product(Variable("x"), Variable("x")), Product(Variable("x"), Constant(-1))), Sum(Product(Constant(1), Variable("x")), Product(Constant(1), Constant(-1))))
    print("Result 4:", result)
    print("Answer 4:", answer)

    assert result == answer

def test_expand_products_over_sums_5():
    # TODO: Implement logic for expanding products over sums when the product is in the form of a FlatProduct.
    # FlatProduct with a Sum Child
    equation = FlatProduct([Constant(2), Variable("x"), Sum(Variable("y"), Constant(1))])
    result = expand_product_over_sums(equation)
    answer = Sum(Product(Constant(2), Product(Variable("x"), Variable("y"))), Product(Constant(2), Product(Variable("x"), Constant(1))))
    print("Result 5:", result)
    print("Answer 5:", answer)

    assert result == answer

def test_expand_products_over_sums_6():
    # TODO: Implement logic for expanding products over sums when the product is in the form of a FlatProduct.
    # FlatProduct with Multiple Sum Children
    equation = FlatProduct([Constant(2), Variable("x"), Sum(Variable("y"), Constant(1))])
    result = expand_product_over_sums(equation)
    answer = Sum(Product(Constant(2), Product(Variable("x"), Variable("y"))), Product(Constant(2), Product(Variable("x"), Constant(1))))
    print("Result 6:", result)
    print("Answer 6:", answer)

    assert result == answer

def test_expand_products_over_sums_7():
    # Sum Inside a Quotient — No Change. Expansion only applies to Product and FlatProduct nodes
    equation = Quotient(Sum(Variable("x"), Constant(1)), Variable("x"))
    result = expand_product_over_sums(equation)

    assert result == Quotient(Sum(Variable("x"), Constant(1)), Variable("x"))

def test_expand_products_over_sums_8():
    # No change. No Sum children.
    equation = Product(Variable("x"), Variable("y"))
    result = expand_product_over_sums(equation)

    assert result == Product(Variable("x"), Variable("y"))

def test_expand_products_over_sums_9():
    # No change. Not a Product node.
    equation = Sum(Variable("x"), Constant(1))
    result = expand_product_over_sums(equation)

    assert result == Sum(Variable("x"), Constant(1))

def test_expand_products_over_sums_10():
    # No change. Not a Product node.
    equation = FlatProduct([Constant(2), Variable("x"), Variable("y")])
    result = expand_product_over_sums(equation)

    assert result == FlatProduct([Constant(2), Variable("x"), Variable("y")])
