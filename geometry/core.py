import dataclasses
from abc import ABC, abstractmethod
from copy import copy
from decimal import Decimal
from enum import Enum
from itertools import chain
from typing import Iterable, Union, Sequence


AnyNumber = Union[float, int, Decimal]


@dataclasses.dataclass
class Point:
    x: AnyNumber
    y: AnyNumber

    def to_int(self):
        return IntPoint(
            round(self.x),
            round(self.y),
        )

    def __iadd__(self, other):
        if isinstance(other, Point):
            self.x += other.x
            self.y += other.y
        else:
            return NotImplemented

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(
                self.x + other.x,
                self.y + other.y
            )

        return NotImplemented



@dataclasses.dataclass
class IntPoint(Point):
    x: int
    y: int

    def __hash__(self):
        return self.x + self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def to_int(self):
        return self


class DrawMethod(Enum):
    PIXELS = 'pixel'
    POINTS_CLOSED = 'points_closed'
    POINTS_OPEN = 'points_open'


class DrawInfo:
    def __init__(self, draw_method: DrawMethod, data: Iterable):
        self.draw_method = draw_method
        self.data = data

    def __add__(self, other):
        if isinstance(other, Point):
            return DrawInfo(
                draw_method=self.draw_method,
                data=[item + other for item in self.data]
            )

        return NotImplemented


    def __radd__(self, other):
        return self + other


class Drawable(ABC):
    @abstractmethod
    def get_draw_info(self) -> Iterable[DrawInfo]:
        raise NotImplementedError


class Container(Drawable):
    def __init__(self, items: Union[Sequence[Drawable], Drawable], coordinates: Point=None):
        self.coordinates = coordinates or Point(0, 0)
        if isinstance(items, Drawable):
            self.items = [items]
        else:
            self.items = items

    def get_draw_info(self) -> Iterable[Drawable]:
        drawables = chain.from_iterable(x.get_draw_info() for x in self.items)
        return (self.coordinates + x for x in drawables)

    def __copy__(self):
        return Container(self.items, copy(self.coordinates))


class Figure(Drawable):
    draw_method = None  # type: DrawMethod

    def get_pixels(self) -> Iterable[Point]:
        raise NotImplementedError

    def get_points(self) -> Iterable[Point]:
        raise NotImplementedError

    def _get_draw_data(self):
        if self.draw_method == DrawMethod.PIXELS:
            return self.get_pixels()
        if self.draw_method in (DrawMethod.POINTS_OPEN, DrawMethod.POINTS_CLOSED):
            return self.get_points()
        raise NotImplementedError(self.draw_method)

    def get_draw_info(self):
        return [DrawInfo(
            draw_method=self.draw_method,
            data=self._get_draw_data()
        )]
