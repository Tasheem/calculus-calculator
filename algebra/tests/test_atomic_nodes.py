from algebra.models.atomic_nodes import *

def test_constant_1():
    five = Constant(5)
    assert five.compute().value == 5

def test_constant_2():
    neg_four = Constant(-4)
    assert neg_four.compute().value == -4

def test_variable_1():
    x = Variable("x")
    assert x.compute().name == "x"

def test_variable_2():
    t = Variable("t")
    assert t.compute().name == "t"

def test_variable_3():
    try:
        invalid = Variable("xy")
        assert False
    except:
        assert True

def test_constant_str_1():
    nine = Constant(9)
    assert str(nine) == "9"

def test_constant_str_2():
    zero = Constant(float("inf"))
    assert str(zero) == "inf"

def test_constant_str_3():
    nine = Constant(-15)
    assert str(nine) == "-15"

def test_variable_str_1():
    nine = Variable("x")
    assert str(nine) == "x"

def test_variable_str_2():
    nine = Variable("y")
    assert str(nine) == "y"
