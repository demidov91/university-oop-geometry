from decimal import Decimal
from unittest import mock

import pytest

from geometry.core import Point, Figure, Container
from geometry.serializers import TextSerializer, TextLine, TextDeserializer, parse_line


class TestTextSerializer:
    @pytest.mark.parametrize('value,expected', [
        (1, '1'),
        (Point(3, -1), '3 -1'),
        (Point(Decimal('2.5'), Decimal('3.14')), '2.5 3.14'),

    ])
    def test_serialize_value(self, value, expected):
        assert TextSerializer().serialize_value(value) == expected


    def test_serialize_data(self):
        assert TextSerializer().serialize_data({
            'hello': 1,
            'hi': 4,
        }) == 'hello: 1\n' \
              'hi: 4'

    @mock.patch('geometry.serializers.TextSerializer.serialize_data', return_value='\t\t\tfield_1: 1')
    def test_serialize_parsed_figure(self, patched_method):
        data = {'any': 'thing'}

        assert (
            TextSerializer().serialize_parsed_figure('SomeFigure', data, level=2) ==
            '\t\tSomeFigure\n\t\t\tfield_1: 1'
        )

        patched_method.assert_called_once_with(data, 3)

    @mock.patch('geometry.serializers.TextSerializer.serialize_parsed_figure',
                return_value='Expected Value')
    def test_serialize_figure(self, patched_method):
        figure = mock.Mock(
            get_display_name=mock.Mock(return_value='AnotherFigure'),
            get_data=mock.Mock(return_value={'field': 42})
        )

        assert TextSerializer().serialize_figure(figure, level=1) == 'Expected Value'

        figure.get_display_name.assert_called_once()
        figure.get_data.assert_called_once()
        patched_method.assert_called_once_with('AnotherFigure', {'field': 42}, level=1)

    @mock.patch('geometry.serializers.TextSerializer.serialize_container', return_value='C')
    @mock.patch('geometry.serializers.TextSerializer.serialize_figure', return_value='F')
    def test_serialize__figure(self, figure_patched, container_patched):
        f = Figure()

        assert TextSerializer().serialize(f, level=12) == 'F'

        figure_patched.assert_called_once_with(f, level=12)
        assert not container_patched.called

    @mock.patch('geometry.serializers.TextSerializer.serialize_container', return_value='C')
    @mock.patch('geometry.serializers.TextSerializer.serialize_figure', return_value='F')
    def test_serialize__container(self, figure_patched, container_patched):
        c = Container()

        assert TextSerializer().serialize(c, level=12) == 'C'

        container_patched.assert_called_once_with(c, level=12)
        assert not figure_patched.called

    @mock.patch('geometry.serializers.TextSerializer.serialize_container_items',
                return_value='\titems:\n\t\tany:thing')
    def test_serialize_container(self, patched_method):
        items = [mock.Mock(), mock.Mock()]

        c = Container(items, Point(3, '14.15'))

        assert TextSerializer().serialize(c) == 'Container\n' \
                                                '\tcoordinates: 3 14.15\n' \
                                                '\titems:\n' \
                                                '\t\tany:thing'

        patched_method.assert_called_once_with(items, 1)

    @mock.patch('geometry.serializers.TextSerializer.serialize',
                side_effect=['\tthis', '\tis', '\ta', '\ttest', '\t!'])
    def test_serialize_container_items(self, patched_method):
        assert (
            TextSerializer().serialize_container_items([mock.Mock()] * 5) ==
            'items:\n\tthis\n\tis\n\ta\n\ttest\n\t!'
        )


@pytest.mark.parametrize('line,expected', [
    ('hello', TextLine(0, 'hello')),
    ('hello ', TextLine(0, 'hello')),
    ('hello\n', TextLine(0, 'hello')),
    ('hello \n', TextLine(0, 'hello')),
    ('\tworld !', TextLine(1, 'world !')),
    ('\t\t\thi, there', TextLine(3, 'hi, there')),
])
def test_parse_line(line, expected):
    assert parse_line(line) == expected



class TestTextDeserializer:
    @mock.patch('geometry.serializers.parse_line',
                side_effect=[
                    TextLine(1, 'one'),
                    TextLine(2, 'two'),
                    TextLine(3, 'three'),
                    TextLine(4, 'four'),
                ])
    def test_next__plain(self, patched_parse):
        tested = TextDeserializer([''] * 4)

        assert tested.next() == TextLine(1, 'one')
        assert tested.next() == TextLine(2, 'two')
        assert tested.next() == TextLine(3, 'three')
        assert tested.next() == TextLine(4, 'four')
        assert tested.next() is None

    @mock.patch('geometry.serializers.parse_line',
                side_effect=lambda x: {
                    'a': TextLine(1, 'one'),
                    'b': TextLine(2, 'two'),
                    'c': TextLine(1, 'three'),
                    'd': TextLine(0, 'four'),
                }[x])
    def test_next__level(self, patched_parse):
        tested = TextDeserializer(['a', 'b', 'c', 'd'])

        assert tested.next(level=1) == TextLine(1, 'one')
        assert tested.next(level=1) == TextLine(2, 'two')
        assert tested.next(level=1) == TextLine(1, 'three')
        assert tested.next(level=1) is None
        assert tested.next(level=0) == TextLine(0, 'four')
        assert tested.next(level=0) is None

    @mock.patch('geometry.serializers.TextDeserializer.next',
                side_effect=[1, 2, 3, 4, 5, None, 6])
    def test_iter_level(self, patched_method):
        assert tuple(TextDeserializer([]).iter_level(1)) == (1, 2, 3, 4, 5)

        patched_method.assert_called_with(level=1)

    @pytest.mark.parametrize('value,expected', [
        ('5', Decimal(5)),
        ('5.5', Decimal('5.5')),
        ('-59.6', Decimal('-59.6')),
        ('1 2.3', Point(Decimal('1'), Decimal('2.3'))),
        ('67.3 -59.6', Point(Decimal('67.3'), Decimal('-59.6'))),
        ('-59.6 67.3', Point(Decimal('-59.6'), Decimal('67.3'))),
    ])
    def test_decode_value(self, value, expected):
        assert TextDeserializer([]).decode_value(value) == expected

    @mock.patch('geometry.serializers.TextDeserializer.decode_value', return_value='V for Vendetta')
    def test_decode_data_line(self, patched_method):
        assert TextDeserializer([]).decode_data_line('name: Vasia ') == ('name', 'V for Vendetta')

        patched_method.assert_called_once_with('Vasia')

    @mock.patch('geometry.serializers.TextDeserializer.iter_level',
                return_value=(
                        mock.Mock(content='a::'),
                        mock.Mock(content='b::'),
                        mock.Mock(content='c::'),
                ))
    @mock.patch('geometry.serializers.TextDeserializer.decode_data_line', side_effect=lambda x:{
        'a::': ('a', 1),
        'b::': ('b', 2),
        'c::': ('c', 42),
    }[x])
    def test_decode_data(self, decode_line_patched, iter_level_patched):
        assert TextDeserializer([]).decode_data(level=2) == {
            'a': 1,
            'b': 2,
            'c': 42,
        }

        iter_level_patched.assert_called_with(2)

    @mock.patch('geometry.serializers.TextDeserializer.next', side_effect=[
        mock.Mock(content='Container', z=1),
        mock.Mock(content='A'),
        mock.Mock(content='B'),
        mock.Mock(content='C'),
        mock.Mock(content='Container'),
        None,
        mock.Mock(content='D'),
    ])
    @mock.patch('geometry.serializers.TextDeserializer.decode_container', return_value='C')
    @mock.patch('geometry.serializers.TextDeserializer.decode_figure', return_value='F')
    def test_decode(self, figure_patched, container_patched, next_patched):
        assert tuple(TextDeserializer([]).decode(level=3)) == ('C', 'F', 'F', 'F', 'C')

        figure_patched.assert_called_with(class_name='C', level=4)
        container_patched.assert_called_with(level=4)
