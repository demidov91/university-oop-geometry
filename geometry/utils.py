from decimal import Decimal
from typing import Tuple, Union


AnyNumber = Union[float, int, Decimal]


def get_distant_point(
        x: AnyNumber,
        y: AnyNumber,
        distance: AnyNumber,
        angle: AnyNumber
) -> Tuple[float, float]:
    return 0.0, 0.0