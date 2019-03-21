
from abc import ABC
from typing import Iterable



from geometry.core import DrawMethod, Point, DrawInfo, Drawable, IntPoint



class BaseBoard(ABC):
    def draw_pixels(self, pixels: Iterable[Point]):
        raise NotImplementedError

    def draw_lines(self, points: Iterable[Point]):
        raise NotImplementedError


class GenericInterface:
    def __init__(self, board: BaseBoard):
        self.board = board

    def draw(self, drawable: Drawable):
        for info in drawable.get_draw_info():
            self.draw_item(info)

    def draw_item(self, info: DrawInfo):
        if info.draw_method == DrawMethod.PIXELS:
            self.board.draw_pixels(set(x.to_int() for x in info.data))
        elif info.draw_method == DrawMethod.POINTS_OPEN:
            self.board.draw_lines(info.data)
        elif info.draw_method == DrawMethod.POINTS_CLOSED:
            points = list(info.data)
            points.append(points[0])
            self.board.draw_lines(points)


class TextBoard(BaseBoard):
    def draw_pixels(self, pixels: Iterable[IntPoint]):
        points_as_str = (f'({x.x}, {x.y})' for x in pixels)
        print('Pixels[' + ', '.join(points_as_str) + ']')

    def draw_lines(self, points: Iterable[Point]):
        points_as_str = (f'({x.x}, {x.y})' for x in (x.to_int() for x in points))
        print('Line ' + ' -> '.join(points_as_str))
