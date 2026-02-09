from algebra.models.atomic_nodes import *
from algebra.models.algebraic_nodes import *

# 2x² + 5x + 7x + 9
two_deg = Product(Constant(2), Power(Variable("x"), Constant(2)))
five_x = Product(Constant(5), Variable("x"))
seven_x = Product(Constant(7), Variable("x"))
nine = Constant(9)

left_sum = Sum(two_deg, five_x)
mid_sum = Sum(left_sum, seven_x)
equation = Sum(mid_sum, nine)

map: dict[Expression, list[int]] = {}
res = equation._find_like_terms(equation, map, False)
# print("map:", map)
for key in map:
    print("Key:", key, end=" -> ")
    print("Value:", map[key])
