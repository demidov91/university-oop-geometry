import dataclasses
from abc import ABC, abstractmethod
from collections import OrderedDict
from copy import copy
from decimal import Decimal
from enum import Enum
from itertools import chain
from typing import Iterable, Union, Sequence

from geometry.forms import FigureForm

AnyNumber = Union[float, int, Decimal]


@dataclasses.dataclass
class Point:
    x: Decimal
    y: Decimal

    def __post_init__(self):
        self.x = Decimal(self.x)
        self.y = Decimal(self.y)


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
        return int(self.x + self.y)

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
    def __init__(self, items: Union[Sequence[Drawable], Drawable]=None, coordinates: Point=None):
        self.coordinates = coordinates or Point(0, 0)
        if not items:
            self.items = []
        elif isinstance(items, Drawable):
            self.items = [items]
        else:
            self.items = items

    def get_draw_info(self) -> Iterable[Drawable]:
        drawables = chain.from_iterable(x.get_draw_info() for x in self.items)
        return (self.coordinates + x for x in drawables)

    def __copy__(self):
        return Container(self.items, copy(self.coordinates))


class FigureStorage:
    _instance = None

    def __new__(cls, *args, **kwargs):
        # Not thread-safe.
        if cls._instance is not None:
            return cls._instance
        return super().__new__(cls, *args, **kwargs)

    def __init__(self):
        # Not thread-safe.
        if type(self)._instance is not None:
            return

        self.figure_classes = []
        type(self)._instance = self


    def add(self, figure_class):
        self.figure_classes.append(figure_class)

    def get(self):
        return tuple(self.figure_classes)


class Figure(Drawable):
    draw_method = None  # type: DrawMethod
    display_symbol = '?'
    _form = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        FigureStorage().add(cls)

    @classmethod
    def get_display_name(cls) -> str:
        return cls.__name__

    @classmethod
    def get_display_symbol(cls) -> str:
        return cls.display_symbol

    @classmethod
    def _create_form(cls):
        annotations = OrderedDict(cls.__init__.__annotations__)
        return FigureForm(
            annotations,
            {x: x for x in annotations}
        )

    @classmethod
    def get_form(cls) -> FigureForm:
        if '_form' not in cls.__dict__:
            cls._form = cls._create_form()

        return cls._form

    def get_instance_form(self):
        form = self.get_form()
        data = form.as_data(self)
        for field in form.fields:
            field.value = data[field.name]

        return form

    def get_data(self):
        return self.get_form().as_data(self)

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
