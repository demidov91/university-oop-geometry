from decimal import Decimal
from unittest import mock

import pytest

from geometry.core import Point, Figure, Container
from geometry.serializers import TextSerializer


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
