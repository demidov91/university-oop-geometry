import tkinter as tk
from typing import Type, Callable

from geometry.core import Point
from geometry.forms import FigureForm, FigureField
from geometry.gui.widgets import PointWidget, DecimalWidget


class FigureDialog(tk.Toplevel):
    def __init__(self, master, *, form: FigureForm, save_callback: Callable, coordinates: Point=None):
        super().__init__(master)
        self.form = form
        self.save_callback = save_callback
        self.coordinates = coordinates
        self._widgets = {}
        self._coordinates_widget = None
        self._build_window()

    def _build_window(self):
        for field in self.form.fields:
            line, widget = self._build_field(field)
            self._widgets[field.name] = widget
            line.pack(side=tk.TOP)

        line, self._coordinates_widget = self._build_field(
            FigureField('coordinates', Point, value=self.coordinates)
        )
        line.pack(side=tk.TOP, pady=(15, 0))

        self.save_button = tk.Button(self, text='Save', command=self.on_save)
        self.save_button.pack(side=tk.TOP)

    def _build_field(self, field):
        line = tk.Frame(self)

        label = tk.Label(line, text=field.label)
        input_widget = self._create_widget(line, field.input_class)
        if field.value:
            input_widget.set_value(field.value)

        label.pack(side=tk.LEFT)
        input_widget.pack(side=tk.LEFT)

        return line, input_widget

    def on_save(self):
        data = (
            {name: self._widgets[name].get_value() for name in self._widgets}
        )
        coordinates = self._coordinates_widget.get_value() or Point(0, 0)
        if not self.form.is_valid(data):
            self.save_button.configure(text='Save (There were invalid values)')
            return

        args, kwargs = self.form.as_args_kwargs(data)

        self.save_callback(
            coordinates=coordinates,
            args=args,
            kwargs=kwargs
        )
        self.destroy()

    def _create_widget(self, master, data_type: Type):
        if type(data_type) is type and issubclass(data_type, Point):
            return PointWidget(master)
        return DecimalWidget(master)
