from decimal import Decimal
from typing import Dict, Type, List


class FigureField:
    def __init__(self, name: str, input_class: Type, *, label: str):
        self.name = name
        self.input_class = input_class
        self.label = label


class FigureForm:
    def __init__(self, field_types: Dict[str, Type], text_labels: Dict[str, str]):
        self.fields = []    # type: List[FigureField]

        for name, input_class in field_types.items():
            self.fields.append(FigureField(name, input_class, label=text_labels.get(name, '?')))


class TriangleForm(FigureForm):
    def __init__(self):
        fields = 'a', 'b', 'c'
        super().__init__(
            field_types={x: Decimal for x in fields},
            text_labels={x: x for x in fields}
        )