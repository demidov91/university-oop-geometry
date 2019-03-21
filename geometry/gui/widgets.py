import tkinter as tk
from decimal import Decimal

from geometry.core import Point


import logging
logger = logging.getLogger(__name__)


class PointWidget(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x = DecimalWidget(self, width=10)
        self.y = DecimalWidget(self, width=10)
        self.x.pack(side=tk.LEFT)
        self.y.pack(side=tk.LEFT)

    def get_value(self):

        x = self.x.get_value()
        y = self.y.get_value()

        if x is not None and y is not None:
            return Point(x, y)

        return None

    def set_value(self, value: Point):
        self.x.set_value(value.x)
        self.y.set_value(value.y)


class DecimalWidget(tk.Entry):
    def __init__(self, *args, **kwargs):
        self.text = tk.StringVar()
        super().__init__(*args, textvariable=self.text, **kwargs)

    def get_value(self):
        raw_value = self.text.get()
        if not raw_value:
            return None
        try:
            return Decimal(raw_value)
        except (ValueError, TypeError, ArithmeticError) as e:
            logger.warning(e)
            return None

    def set_value(self, value: Decimal):
        self.text.set(str(value))
