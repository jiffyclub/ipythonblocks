import os
import pytest

from .. import ipythonblocks


@pytest.fixture
def basic_pixel():
    return ipythonblocks.Pixel(5, 6, 7, size=20)


def test_xy(basic_pixel):
    """
    Test the .x and .y attributes.

    """
    bp = basic_pixel

    assert bp.x is None
    assert bp.y is None

    bp._row = 1
    bp._col = 2

    assert bp.x == 2
    assert bp.y == 1


def test_td(basic_pixel):
    """
    Test the Pixel._td proerty that returns an HTML table cell.

    """
    bp = basic_pixel

    bp._row = 1
    bp._col = 2

    title = ipythonblocks._TITLE.format(bp._col, bp._row,
                                        bp.red, bp.green, bp.blue)
    rgb = ipythonblocks._RGB.format(bp.red, bp.green, bp.blue)
    td = ipythonblocks._TD.format(title, bp.size, rgb)

    assert bp._td == td


def test_str1(basic_pixel):
    """
    Test the Block.__str__ method used with print.

    """
    bp = basic_pixel

    s = os.linesep.join(['Pixel', 'Color: (5, 6, 7)'])

    assert bp.__str__() == s


def test_str2(basic_pixel):
    """
    Test the Block.__str__ method used with print.

    """
    bp = basic_pixel
    bp._row = 8
    bp._col = 9

    s = os.linesep.join(['Pixel [9, 8]', 'Color: (5, 6, 7)'])

    assert bp.__str__() == s
