import tkinter as tk
from tkinter import filedialog
from copy import deepcopy
from functools import partial
from typing import Iterable, Type

from geometry.core import Point, FigureStorage, Figure, Container
from geometry.graphics import BaseBoard, GenericInterface
from geometry.gui import constants as gui_const
from geometry.gui.figure_dialog import FigureDialog
from geometry.serializers import TextSerializer, TextDeserializer


import logging
logger = logging.getLogger(__name__)


class GUI(tk.Frame, BaseBoard):
    def _init_left_side(self):
        self.canvas = tk.Canvas(
            self,
            width=gui_const.WINDOW_SIZE[0],
            height=gui_const.WINDOW_SIZE[1],
            bg='white'
        )

        self.canvas.pack(side=tk.LEFT)

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

        self.actions_frame = tk.Frame(self.right_container)
        self.actions_frame.pack(side=tk.TOP, pady=(15, 0))
        self.save_button = tk.Button(self.actions_frame, text='Save', command=self.on_save)
        self.save_button.pack(side=tk.LEFT)
        self.open_button = tk.Button(self.actions_frame, text='Open', command=self.on_open)
        self.open_button.pack(side=tk.LEFT)

    def _init_figures_ui(self, master):
        self.figures_frame = tk.Frame(master)
        self.figures_frame.pack(side=tk.TOP, fill=tk.Y)
        self._update_figures()

    def _update_figures(self):
        self._update_figures_frame()
        self._repaint()

    def _repaint(self):
        self.canvas.delete(tk.ALL)
        GenericInterface(self).draw(self.figures)

    def _update_figures_frame(self):
        for child in tuple(self.figures_frame.children.values()):
            child.destroy()

        for item in self.figures.items:
            line = tk.Frame(self.figures_frame)
            line.pack(side=tk.TOP)

            if len(item.items) == 1 and isinstance(item.items[0], Figure):
                self._build_figure_line(line, item)
            else:
                self._build_container_line(line, item)

    def _build_figure_line(self, line, item: Container):
        label = tk.Label(line, text=item.items[0].get_display_symbol())
        copy_btn = tk.Button(
            line,
            text='⎘',
            command=partial(self.on_copy_click, container=item),
        )
        edit = tk.Button(
            line,
            text='✎',
            command=partial(self.on_edit_click, container=item),
        )
        remove = tk.Button(
            line,
            text='✖',
            command=partial(self.on_remove_click, container=item),
        )

        label.pack(side=tk.LEFT)
        copy_btn.pack(side=tk.LEFT)
        edit.pack(side=tk.LEFT)
        remove.pack(side=tk.LEFT)

    def _build_container_line(self, line, item: Container):
        label = tk.Label(line, text='\u06de')
        copy_btn = tk.Button(
            line,
            text='⎘',
            command=partial(self.on_copy_click, container=item),
        )
        remove = tk.Button(
            line,
            text='✖',
            command=partial(self.on_remove_click, container=item),
        )

        label.pack(side=tk.LEFT)
        copy_btn.pack(side=tk.LEFT)
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
        self.figures = Container(coordinates=Point(1, 1))
        self._init_left_side()
        self._init_right_side()

    def draw_lines(self, points: Iterable[Point]):
        iterator = iter(points)
        prev = next(iterator)

        for next_point in iterator:
            self.canvas.create_line((prev.x, prev.y, next_point.x, next_point.y), fill='black')
            prev = next_point

    def draw_pixels(self, points: Iterable[Point]):
        for point in points:
            self.canvas.create_line(point.x, point.y, point.x+1, point.y, fill='black')

    def create_figure(self, figure_class: Type[Figure], coordinates: Point, args: tuple, kwargs: dict):
        self.figures.items.append(Container(
            figure_class(*args, **kwargs),
            coordinates
        ))
        self._update_figures()

    def edit_figure(self, container: Container, coordinates: Point, args: tuple, kwargs: dict):
        container.items[0] = type(container.items[0])(*args, **kwargs)
        container.coordinates = coordinates
        self._repaint()

    def on_create_click(self):
        figure_class = self._get_figure_to_create()
        if figure_class is None:
            return

        form = figure_class.get_form()
        FigureDialog(
            self,
            form=form,
            save_callback=partial(self.create_figure, figure_class=figure_class),
        )

    def on_copy_click(self, container: Container):
        self.figures.items.append(deepcopy(container))
        self._update_figures()

    def on_edit_click(self, container: Container):
        figure = container.items[0]
        form = figure.get_instance_form()
        FigureDialog(
            self,
            form=form,
            coordinates=container.coordinates,
            save_callback=partial(self.edit_figure, container=container),
        )

    def on_remove_click(self, container: Container):
        self.figures.items.remove(container)
        self._update_figures()

    def on_save(self):
        path = filedialog.asksaveasfilename(
            initialdir=gui_const.DEFAULT_SAVE_DIR,
            defaultextension='.vi'
        )
        if not path:
            return

        with open(path, mode='wt') as f:
            f.write(TextSerializer().serialize(self.figures))

    def on_open(self):
        path = filedialog.askopenfilename(
            initialdir=gui_const.DEFAULT_SAVE_DIR,
            filetypes=(
                ('images', '*.vi'),
                ('all files', '*.*'),
            )
        )

        with open(path, mode='rt') as f:
            objects_iterator = TextDeserializer(f).decode()
            image = next(objects_iterator)
            rest_of_data = tuple(objects_iterator)

        if not isinstance(image, Container):
            logger.error('Unexpected file content.')
            return

        if rest_of_data:
            logger.warning('Following records will be ignored: %s', rest_of_data)

        self.figures = image
        self._update_figures()
