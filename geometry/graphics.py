from typing import Iterable

from geometry.core import DrawMethod, Point, DrawInfo, Drawable


def draw(drawable: Drawable):
    for info in drawable.get_draw_info():
        draw_item(info)


def draw_item(info: DrawInfo):
    if info.draw_method == DrawMethod.PIXELS:
        draw_pixels(info.data)
    elif info.draw_method == DrawMethod.POINTS_OPEN:
        draw_points(info.data)
    elif info.draw_method == DrawMethod.POINTS_CLOSED:
        points = list(info.data)
        points.append(points[0])
        draw_points(points)


def draw_pixels(pixels: Iterable[Point]):
    unique_pixels = set(x.to_int() for x in pixels)
    points_as_str = (f'({x.x}, {x.y})' for x in unique_pixels)
    print('Pixels[' + ', '.join(points_as_str) + ']')


def draw_points(points: Iterable[Point]):
    points_as_str = (f'({x.x}, {x.y})' for x in (x.to_int() for x in points))
    print('Line ' + ' -> '.join(points_as_str))

