from typing import Dict, Type, List


class FigureField:
    def __init__(self, name: str, input_class: Type, *, label: str=None, value=None):
        self.name = name
        self.input_class = input_class
        self.label = label if label is not None else name
        self.value = value


class FigureForm:
    def __init__(self, field_types: Dict[str, Type], text_labels: Dict[str, str]):
        self.fields = []    # type: List[FigureField]

        for name, input_class in field_types.items():
            self.fields.append(FigureField(name, input_class, label=text_labels.get(name, '?')))

    def as_args_kwargs(self, data: dict):
        return (), data

    def as_data(self, figure):
        return {
            f.name: getattr(figure, f.name)
            for f in self.fields
        }

    def is_valid(self, data: dict):
        return all(x is not None for x in data.values())


