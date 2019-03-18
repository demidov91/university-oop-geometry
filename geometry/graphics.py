from typing import Iterable

from geometry.core import Figure, DrawMethod, Point


def draw_figure(figure: Figure):
    if figure.draw_method == DrawMethod.PIXELS:
        draw_pixels(figure.get_pixels())
    elif figure.draw_method == DrawMethod.POINTS:
        draw_points(figure.get_points())


def draw_pixels(pixels: Iterable[Point]):
    unique_pixels = set(x.to_int() for x in pixels)
    points_as_str = (f'({x.x}, {x.y})' for x in unique_pixels)
    print('[' + ', '.join(points_as_str) + ']')


def draw_points(points: Iterable[Point]):
    points_as_str = (f'({x.x}, {x.y})' for x in (x.to_int() for x in points))
    print(' -> '.join(points_as_str))

