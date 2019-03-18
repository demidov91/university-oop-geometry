import dataclasses
from enum import Enum
from typing import Iterable

from geometry.utils import AnyNumber


@dataclasses.dataclass
class Point:
    x: AnyNumber
    y: AnyNumber

    def to_int(self):
        return IntPoint(
            round(self.x),
            round(self.y),
        )


@dataclasses.dataclass
class IntPoint:
    x: int
    y: int

    def __hash__(self):
        return self.x + self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class DrawMethod(Enum):
    PIXELS = 'pixel'
    POINTS = 'points'


class Figure:
    draw_method = None  # type: DrawMethod

    def get_pixels(self) -> Iterable[Point]:
        raise NotImplementedError

    def get_points(self) -> Iterable[Point]:
        raise NotImplementedError