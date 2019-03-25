import dataclasses
import re
from decimal import Decimal
from itertools import chain
from typing import Iterator, Union, Iterable, Tuple, Optional

from geometry.core import Figure, Container, Point, FigureRegistry


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


@dataclasses.dataclass
class TextLine:
    level: int
    content: str

    def __hash__(self):
        return self.level

    def __eq__(self, other):
        if not isinstance(other, TextLine):
            return False

        return self.level == other.level and self.content == other.content


indentation_pattern = re.compile(r'(?P<indentation>\t*)(?P<content>.*?)\s*$')

def parse_line(line: str) -> TextLine:
    match = indentation_pattern.match(line)
    return TextLine(match.start('content'), match.group('content'))


class TextDeserializer:
    NO_LAST_LINE = object()
    coordinates_pattern = re.compile(r'([-\d.]+) ([-\d.]+)\s*$')

    def __init__(self, lines_iterable: Union[Iterable[str], str]):
        if isinstance(lines_iterable, str):
            lines_iterable = lines_iterable.split('\n')

        self._last_line = TextDeserializer.NO_LAST_LINE
        self._lines_iterator = iter(lines_iterable)

    def next(self, level: int=0) -> Optional[TextLine]:
        last_line = next(self._lines_iterator, None)
        if last_line is None:
            return None

        record = parse_line(last_line)
        if record.level < level:
            self._lines_iterator = chain((last_line, ), self._lines_iterator)
            return None

        return record

    def iter_level(self, level: int) -> Iterator[TextLine]:
        record = self.next(level=level)

        while record is not None:
            yield record
            record = self.next(level=level)

    def decode(self, level: int=0) -> Iterator[Union[Figure, Container]]:
        record = self.next(level)

        while record is not None:
            if record.content == 'Container':
                yield self.decode_container(level=level+1)
            else:
                yield self.decode_figure(class_name=record.content, level=level+1)

            record = self.next(level)

    def decode_container(self, level: int) -> Container:
        key, point = self.decode_data_line(self.next(level=level).content)
        assert key == 'coordinates'
        assert self.next(level=level).content == 'items:'
        items = list(self.decode(level=level+1))
        return Container(items=items, coordinates=point)

    def decode_figure(self, *, class_name: str, level: int) -> Figure:
        figure_class = FigureRegistry().get_by_name(class_name)
        form = figure_class.get_form()
        args, kwargs = form.as_args_kwargs(self.decode_data(level=level))
        return figure_class(*args, **kwargs)

    def decode_data(self, *, level: int) -> dict:
        data = {}
        for line_record in self.iter_level(level):
            key, value = self.decode_data_line(line_record.content)
            data[key] = value

        return data

    def decode_data_line(self, line) -> Tuple[str, object]:
        separator = line.find(':')
        return line[:separator], self.decode_value(line[separator+1:].strip())

    def decode_value(self, value: str):
        coordinates_match = self.coordinates_pattern.match(value)
        if coordinates_match is not None:
            return Point(
                Decimal(coordinates_match.group(1)),
                Decimal(coordinates_match.group(2))
            )

        return Decimal(value)
