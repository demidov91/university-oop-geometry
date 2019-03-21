from decimal import Decimal
from typing import Dict, Type, List


class FigureField:
    def __init__(self, name: str, input_class: Type, *, label: str=None):
        self.name = name
        self.input_class = input_class
        self.label = label if label is not None else name


class FigureForm:
    def __init__(self, field_types: Dict[str, Type], text_labels: Dict[str, str]):
        self.fields = []    # type: List[FigureField]

        for name, input_class in field_types.items():
            self.fields.append(FigureField(name, input_class, label=text_labels.get(name, '?')))

    def as_args_kwargs(self, data: dict):
        return (), data


