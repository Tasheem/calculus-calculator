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
