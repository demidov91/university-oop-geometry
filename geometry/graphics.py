import tkinter as tk
from typing import Iterable

from PIL import Image, ImageDraw
from PIL.ImageTk import PhotoImage

from geometry.core import DrawMethod, Point, DrawInfo, Drawable, IntPoint



class GenericInterface:
    def __init__(self, board):
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


class TextBoard:
    def draw_pixels(self, pixels: Iterable[IntPoint]):
        points_as_str = (f'({x.x}, {x.y})' for x in pixels)
        print('Pixels[' + ', '.join(points_as_str) + ']')

    def draw_lines(self, points: Iterable[Point]):
        points_as_str = (f'({x.x}, {x.y})' for x in (x.to_int() for x in points))
        print('Line ' + ' -> '.join(points_as_str))


class GUI(tk.Frame):
    image_size = (500, 500)

    def __init__(self, *, master):
        super().__init__(master=master)
        self._image = Image.new('RGB', self.image_size, color=(255, 255, 255))
        self.board = tk.Label(master)
        self._update_image()
        self.board.pack()

    def _update_image(self):
        self._tkinter_image = PhotoImage(self._image)
        self.board.configure(image=self._tkinter_image)

    def draw_lines(self, points: Iterable[Point]):
        editor = ImageDraw.Draw(self._image)
        iterator = iter(points)
        prev = next(iterator)

        for next_point in iterator:
            editor.line((prev.x, prev.y, next_point.x, next_point.y), fill=0)
            prev = next_point

        self._update_image()

    def draw_pixels(self, points: Iterable[Point]):
        editor = ImageDraw.Draw(self._image)
        for point in points:
            editor.point((point.x, point.y), fill=0)

        self._update_image()

