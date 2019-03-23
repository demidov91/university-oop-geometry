import logging
import os
import sys
from decimal import Decimal
from importlib import import_module
from typing import Tuple, Union, Iterable

from geometry.core import AnyNumber, Point


logger = logging.getLogger(__name__)


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


def read_plugins(path: str):
    sys.path.append(path)
    for module_file in os.listdir(path):
        if not module_file.endswith('.py'):
            continue

        plugin = import_module(module_file[:-3])
        logger.info('Plugin is activated: %s', plugin)


