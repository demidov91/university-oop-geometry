import tkinter as tk
from typing import Type

from geometry.core import Point
from geometry.forms import FigureForm, FigureField
from geometry.gui.widgets import PointWidget, DecimalWidget


class FigureDialog(tk.Toplevel):
    def __init__(self, master, form: FigureForm):
        super().__init__(master)
        self.form = form
        self._widgets = {}
        self._coordinates_widget = None
        self._build_window()

    def _build_window(self):
        for field in self.form.fields:
            line, widget = self._build_field(field)
            self._widgets[field.name] = widget
            line.pack(side=tk.TOP)

        line, self._coordinates_widget = self._build_field(FigureField('coordinates', Point))
        line.pack(side=tk.TOP, pady=(15, 0))

        self.save_button = tk.Button(self, text='Save', command=self.on_save)
        self.save_button.pack(side=tk.TOP)

    def _build_field(self, field):
        line = tk.Frame(self)


        label = tk.Label(line, text=field.label)
        input_widget = self._create_widget(line, field.input_class)

        label.pack(side=tk.LEFT)
        input_widget.pack(side=tk.LEFT)

        return line, input_widget

    def on_save(self):
        data = (
            {name: self._widgets[name].get_value() for name in self._widgets}
        )
        coordinates = self._coordinates_widget.get_value() or Point(0, 0)
        args, kwargs = self.form.as_args_kwargs(data)
        self.master.create_figure(
            coordinates,
            args,
            kwargs
        )
        self.destroy()

    def _create_widget(self, master, data_type: Type):
        if type(data_type) is type and issubclass(data_type, Point):
            return PointWidget(master)
        return DecimalWidget(master)