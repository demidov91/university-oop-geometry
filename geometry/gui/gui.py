import tkinter as tk
from functools import partial
from typing import Iterable, Type

from PIL import Image, ImageDraw
from PIL.ImageTk import PhotoImage

from geometry.core import Point, FigureStorage, Figure, Container
from geometry.graphics import BaseBoard, GenericInterface
from geometry.gui.figure_dialog import FigureDialog


import logging
logger = logging.getLogger(__name__)


class GUI(tk.Frame, BaseBoard):
    image_size = (500, 500)

    def _init_left_side(self):
        self.paint_area = tk.Label(self)
        self.paint_area.pack(side=tk.LEFT)

    def _init_right_side(self):
        self.right_container = tk.Frame(self)
        self.right_container.pack(side=tk.LEFT, fill=tk.Y)

        self.dropdown_area = tk.Frame(self.right_container)
        self.dropdown_area.pack(side=tk.TOP)

        self.selected_dropdown = tk.StringVar()
        self.create_button = tk.Button(
            self.dropdown_area,
            text='Create',
            command=self.on_create_click
        )
        self.create_button.pack(side=tk.LEFT)
        self._update_dropdown_options()

        self._init_figures_ui(self.right_container)

    def _init_figures_ui(self, master):
        self.figures_frame = tk.Frame(master)
        self.figures_frame.pack(side=tk.TOP, fill=tk.Y)
        self._update_figures()

    def _update_figures(self):
        self._update_figures_frame()
        self._reset_image()
        GenericInterface(self).draw(self.figures)

    def _update_figures_frame(self):
        for child in tuple(self.figures_frame.children.values()):
            child.destroy()

        for item in self.figures.items:
            line = tk.Frame(self.figures_frame)
            line.pack(side=tk.TOP)

            label = tk.Label(line, text=item.items[0].get_display_symbol())
            remove = tk.Button(
                line,
                text='remove',
                command=partial(self.on_remove, container=item),
            )

            label.pack(side=tk.LEFT)
            remove.pack(side=tk.LEFT)

    def _update_dropdown_options(self):
        storage = FigureStorage()
        self._figure_name_to_class = {
            x.get_display_name(): x
            for x in storage.get()
        }

        if hasattr(self, 'dropdown'):
            self.dropdown.destroy()

        self.dropdown = tk.OptionMenu(
            self.dropdown_area,
            self.selected_dropdown,
            *self._figure_name_to_class
        )
        if self.selected_dropdown.get() not in self._figure_name_to_class:
            self.selected_dropdown.set(next(iter(self._figure_name_to_class), None))

        self.create_button.pack_forget()
        self.dropdown.pack(side=tk.LEFT)
        self.create_button.pack(side=tk.LEFT)

    def _get_figure_to_create(self) -> Type[Figure]:
        return self._figure_name_to_class.get(self.selected_dropdown.get())

    def __init__(self, *, master):
        super().__init__(master=master)
        self.pack()
        self.figures = Container()
        self._init_left_side()
        self._init_right_side()


    def _update_image(self):
        self._tkinter_image = PhotoImage(self._image)
        self.paint_area.configure(image=self._tkinter_image)

    def _reset_image(self):
        self._image = Image.new('RGB', self.image_size, color=(255, 255, 255))
        self._update_image()

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

    def create_figure(self, coordinates: Point, args: tuple, kwargs: dict):
        self.figures.items.append(Container(
            self._editing_figure_class(*args, **kwargs),
            coordinates
        ))
        self._update_figures()


    def on_create_click(self):
        figure_class = self._get_figure_to_create()
        if figure_class is None:
            return

        form = figure_class.get_form()
        self._editing_figure_class = figure_class
        FigureDialog(self, form)

    def on_remove(self, container):
        self.figures.items.remove(container)
        self._update_figures()
