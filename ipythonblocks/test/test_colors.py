"""
Tests for ipythonblocks' color conveniences.

"""

import pytest

from .. import ipythonblocks


def test_color():
    color = ipythonblocks.Color(1, 2, 3)

    assert color == (1, 2, 3)
    assert color.red == 1
    assert color.green == 2
    assert color.blue == 3


@pytest.mark.parametrize(
    'colors, color_name',
    [
        (ipythonblocks.colors, 'Crimson'),
        (ipythonblocks.fui_colors, 'Carrot'),
    ]
)
def test_colors(colors, color_name):
    assert isinstance(colors, ipythonblocks._ColorBunch)
    assert color_name in colors
    assert hasattr(colors, color_name)
    assert isinstance(colors[color_name], ipythonblocks.Color)
