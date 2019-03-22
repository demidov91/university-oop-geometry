from math import sqrt
from typing import Iterable
from itertools import chain

from geometry.core import Figure, Point, DrawMethod, AnyNumber
from geometry.forms import FigureForm
from geometry.utils import (
    solve_elipse_equation,
    create_point_combinations,
)


class Circle(Figure):
    draw_method = DrawMethod.PIXELS
    display_symbol = '\u25cb'

    def __init__(self, radius: int):
        if radius <= 0:
            raise ValueError('Radius should be positive.')

        self.radius = radius

    def get_pixels(self) -> Iterable[Point]:
        for delta_x in range(int(self.radius) + 1):
            delta_y = sqrt(self.radius**2 - delta_x**2)
            yield from chain(
                create_point_combinations(delta_x, delta_y),
                create_point_combinations(delta_y, delta_x)
            )


class Triangle(Figure):
    draw_method = DrawMethod.POINTS_CLOSED
    display_symbol = '\u25b3'

    @classmethod
    def _create_form(cls):
        return TriangleForm()

    def __init__(self, *points: Point):
        if len(points) != 3:
            raise ValueError('3 points expected, got %d', len(points))

        self.points = points

    def get_points(self):
        return self.points




class Rectangle(Figure):
    draw_method = DrawMethod.POINTS_CLOSED
    display_symbol = '\u25ad'

    def __init__(
            self,
            x_length: AnyNumber,
            y_length: AnyNumber,
    ):
        if not (x_length > 0 and y_length > 0):
            raise ValueError('Side lengths should be positive numbers.')

        self.x_length = x_length
        self.y_length = y_length

    def get_points(self):
        return (
            Point(0, 0),
            Point(self.x_length, 0),
            Point(self.x_length, self.y_length),
            Point(0, self.y_length),
        )


class Square(Rectangle):
    display_symbol = '\u25a1'

    def __init__(self, side_length: AnyNumber):
        super().__init__(side_length, side_length)

    @property
    def side_length(self):
        return self.x_length


class Elipse(Figure):
    draw_method = DrawMethod.PIXELS
    display_symbol = '\u2b2d'

    def __init__(self, x_radius: AnyNumber, y_radius: AnyNumber):
        self.x_radius = x_radius
        self.y_radius = y_radius

    def get_pixels(self):
        for delta_x in range(int(self.x_radius)):
            delta_y = solve_elipse_equation(self.y_radius, delta_x, self.x_radius)
            yield from create_point_combinations(delta_x, delta_y)


        for delta_y in range(int(self.y_radius)):
            delta_x = solve_elipse_equation(self.x_radius, delta_y, self.y_radius)
            yield from create_point_combinations(delta_x, delta_y)



class Line(Figure):
    draw_method = DrawMethod.POINTS_OPEN
    display_symbol = '\u2572'

    def __init__(self, a: Point, b: Point):
        self.a = a
        self.b = b

    def get_points(self):
        return self.a, self.b


class TriangleForm(FigureForm):
    def __init__(self):
        fields = 'a', 'b', 'c'
        super().__init__(
            field_types={x: Point for x in fields},
            text_labels={x: x for x in fields}
        )

    def as_args_kwargs(self, data: dict):
        return (data['a'], data['b'], data['c']), {}

    def as_data(self, figure):
        return dict(zip(('a', 'b', 'c'), figure.points))