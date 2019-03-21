import tkinter as tk
from typing import Iterable, Type
from decimal import Decimal

from PIL import Image, ImageDraw
from PIL.ImageTk import PhotoImage

from geometry.core import Point, FigureStorage, FigureForm, Figure, Container
from geometry.graphics import BaseBoard, GenericInterface


import logging
logger = logging.getLogger(__name__)


class GUI(tk.Frame, BaseBoard):
    image_size = (500, 500)

    def _init_left_side(self):
        self.paint_area = tk.Label(self)
        self._reset_image()
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

        self.figures = tk.Frame(self.right_container)
        self.figures.pack(side=tk.TOP, fill=tk.Y)

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
            self.selected_dropdown.set('')

        self.create_button.pack_forget()
        self.dropdown.pack(side=tk.LEFT)
        self.create_button.pack(side=tk.LEFT)

    def _get_figure_to_create(self) -> Type[Figure]:
        return self._figure_name_to_class.get(self.selected_dropdown.get())

    def __init__(self, *, master):
        super().__init__(master=master)
        self.pack()
        self._init_left_side()
        self._init_right_side()
        self.figures = Container()

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

    def on_create_click(self):
        figure_class = self._get_figure_to_create()
        if figure_class is None:
            return

        form = figure_class.get_form()
        self._editing_figure_class = figure_class
        FigureDialog(self, form)


    def update_figure(self, identifier, args, kwargs):
        self.figures.items.append(self._editing_figure_class(*args, **kwargs))
        self._reset_image()
        GenericInterface(self).draw(self.figures)


class FigureDialog(tk.Toplevel):
    def __init__(self, master, form: FigureForm, identifier=None):
        super().__init__(master)
        self.form = form
        self.figure_identifier = identifier
        self._widgets = {}
        self._build_window()

    def _build_window(self):
        for field in self.form.fields:
            line = tk.Frame(self)

            label = tk.Label(line, text=field.name)
            label.pack(side=tk.LEFT)
            input_widget = self._create_widget(line, field.input_class)
            input_widget.pack(side=tk.LEFT)
            self._widgets[field.name] = input_widget

            line.pack(side=tk.TOP)

        self.save_button = tk.Button(self, text='Save', command=self.on_save)
        self.save_button.pack(side=tk.TOP)

    def on_save(self):
        data = (
            {name: self._widgets[name].get_value() for name in self._widgets}
        )
        self.master.update_figure(self.figure_identifier, *self.form.as_args_kwargs(data))
        self.destroy()

    def _create_widget(self, master, data_type: Type):
        if type(data_type) is type and issubclass(data_type, Point):
            return PointWidget(master)
        return DecimalWidget(master)


class PointWidget(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x = DecimalWidget(self)
        self.y = DecimalWidget(self)
        self.x.pack(side=tk.LEFT)
        self.y.pack(side=tk.LEFT)

    def get_value(self):

        x = self.x.get_value()
        y = self.y.get_value()

        if x is not None and y is not None:
            return Point(x, y)

        return None


class DecimalWidget(tk.Entry):
    def get_value(self):
        raw_value = self.get()
        if not raw_value:
            return None
        try:
            return Decimal(raw_value)
        except (ValueError, TypeError, ArithmeticError) as e:
            logger.warning(e)
            return None





