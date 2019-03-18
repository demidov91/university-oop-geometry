from decimal import Decimal
from math import sqrt, pi
from typing import Sequence, Iterable

from geometry.core import Figure, Point, DrawMethod
from geometry.utils import get_distant_point


class Circle(Figure):
    draw_method = DrawMethod.PIXELS

    def __init__(self, center: Point, radius: int):
        if radius <= 0:
            raise ValueError('Radius should be positive.')

        self.center = center
        self.radius = radius

    def get_pixels(self) -> Iterable[Point]:
        for delta_x in range(self.radius + 1):
            delta_y = sqrt(self.radius**2 - delta_x**2)
            yield from self._create_pixel_combinations(delta_x, delta_y)
            yield from self._create_pixel_combinations(delta_y, delta_x)

    def _create_pixel_combinations(self, delta_x: float, delta_y: float):
        yield Point(self.center.x - delta_x, self.center.y - delta_y)
        yield Point(self.center.x + delta_x, self.center.y - delta_y)
        yield Point(self.center.x - delta_x, self.center.y + delta_y)
        yield Point(self.center.x + delta_x, self.center.y + delta_y)



class Triangle(Figure):
    draw_method = DrawMethod.POINTS

    def __init__(self, *points: Sequence[Point]):
        if len(points) != 3:
            raise ValueError('3 points expected, got %d', len(points))

        self.points = points

    def get_points(self):
        return self.points


class Rectangle(Figure):
    draw_method = DrawMethod.POINTS

    def __init__(
            self,
            up_left_point: Point,
            side_length_1: Decimal,
            side_length_2: Decimal,
            *,
            rotation: Decimal,
    ):
        if not (side_length_1 > 0 and side_length_2 > 0):
            raise ValueError('Side lengths should be positive numbers.')

        self.up_left_point = up_left_point
        self.side_length_1 = side_length_1
        self.side_length_2 = side_length_2
        self.rotation = rotation

    def get_points(self):
        yield self.up_left_point

        yield Point(*get_distant_point(
            self.up_left_point.x,
            self.up_left_point.y,
            self.side_length_1,
            self.rotation))

        yield Point(*get_distant_point(
            self.up_left_point.x,
            self.up_left_point.y,
            sqrt(self.side_length_1**2 + self.side_length_2**2),
            self.rotation + pi / 4))


        yield Point(*get_distant_point(
            self.up_left_point.x,
            self.up_left_point.y,
            self.side_length_2,
            self.rotation + pi / 2))


class Square(Rectangle):
    def __init__(self, up_left_point: Point, side_length: Decimal, rotation: Decimal):
        super().__init__(up_left_point, side_length, side_length, rotation=rotation)


