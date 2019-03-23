from decimal import Decimal
from math import pi, cos, sin

from geometry.core import Figure, DrawMethod, Point


class RegularPolygon(Figure):
    draw_method = DrawMethod.POINTS_CLOSED
    display_symbol = '◇'

    def __init__(self, n: int, radius: Decimal):
        self.n = int(n)
        self.radius = radius

    @classmethod
    def get_display_name(cls):
        return 'Polygon'

    def get_points(self):
        step = 2 * pi / self.n

        for i in range(self.n):
            yield Point(
                self.radius * Decimal(cos(step * i - pi / 2)),
                self.radius * Decimal(sin(step * i - pi / 2))
            )
