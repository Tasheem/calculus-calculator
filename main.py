from algebra.models.atomic_nodes import *
from algebra.models.algebraic_nodes import *
from algebra.utils.normalize import *

# 2x² + 5x + 7x + 9
""" two_deg = Product(Constant(2), Power(Variable("x"), Constant(2)))
five_x = Product(Constant(5), Variable("x"))
seven_x = Product(Constant(7), Variable("x"))
nine = Constant(9)

left_sum = Sum(two_deg, five_x)
mid_sum = Sum(left_sum, seven_x)
equation = Sum(mid_sum, nine)

map = equation.find_like_terms()
# print("map:", map)
for key in map:
    print("Key:", key, end=" -> ")
    print("Value:", map[key]) """

equation = Sum(Variable("x"), Sum(Variable("y"), Variable("z")))
result = flatten_sums_products(equation)
print("Result:", result)
