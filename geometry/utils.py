from decimal import Decimal
from math import sqrt
from typing import Tuple, Union, Iterable


from geometry.core import AnyNumber, Point


def create_point_combinations(x: AnyNumber, y: AnyNumber) -> Iterable[Point]:
    return (
        Point(x, y),
        Point(x, -y),
        Point(-x, y),
        Point(-x, -y)
    )

def solve_elipse_equation(
        current_coef: AnyNumber,
        other_coordinate: AnyNumber,
        other_coef: AnyNumber
) -> Union[Decimal, float]:
    return current_coef * Decimal(1 - other_coordinate**2 / other_coef**2).sqrt()