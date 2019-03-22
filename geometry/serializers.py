from typing import Iterable, Union

from geometry.core import Figure, Container, Point


def get_indentation(level: int) -> str:
    return '\t' * level


class TextSerializer:
    def serialize(self, object: Union[Container, Figure], level: int=0):
        if isinstance(object, Container):
            return self.serialize_container(object, level=level)
        if isinstance(object, Figure):
            return self.serialize_figure(object, level=level)

        raise ValueError(type(object))

    def serialize_container(self, container: Container, *, level: int=0):
        indentation = get_indentation(level)
        return f'{indentation}Container\n' \
               f'{self.serialize_data({"coordinates": container.coordinates}, level=level+1)}\n' \
               f'{self.serialize_container_items(container.items, level+1)}'

    def serialize_container_items(self, items: Iterable[Union[Container, Figure]], level: int=0):
        return f'{get_indentation(level)}items:\n' + '\n'.join(self.serialize(x, level+1) for x in items)

    def serialize_figure(self, figure: Figure, *, level: int=0):
        object_type = figure.get_display_name()
        data = figure.get_data()
        return self.serialize_parsed_figure(object_type, data, level=level)

    def serialize_parsed_figure(self, object_type: str, data: dict, *, level: int=0):
        indentation = get_indentation(level)
        return f'{indentation}{object_type}\n{self.serialize_data(data, level+1)}'

    def serialize_data(self, data: dict, level: int=0) -> str:
        indentation = get_indentation(level)
        return '\n'.join(
            f'{indentation}{key}: {self.serialize_value(value)}'
            for key, value in data.items()
        )

    def serialize_value(self, value):
        if isinstance(value, Point):
            return f'{value.x} {value.y}'
        return str(value)




