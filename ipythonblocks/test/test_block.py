import os
import pytest

from .. import ipythonblocks


@pytest.fixture
def basic_block():
    return ipythonblocks.Block(5, 6, 7, size=20)


def test_basic_api(basic_block):
    """
    Check that inputs are going to the right attributes and that assignment
    works when it should and not when it shouldn't.

    """
    bb = basic_block

    assert bb.rgb == (5, 6, 7)

    assert bb.red == 5
    bb.red = 1
    assert bb.red == 1

    assert bb.green == 6
    bb.green = 2
    assert bb.green == 2

    assert bb.blue == 7
    bb.blue = 3
    assert bb.blue == 3

    assert bb.rgb == (1, 2, 3)

    assert bb.size == 20
    bb.size = 10
    assert bb.size == 10

    assert bb.row is None
    with pytest.raises(AttributeError):
        bb.row = 5

    assert bb.col is None
    with pytest.raises(AttributeError):
        bb.col = 5


def test_attribute_limits(basic_block):
    """
    Color and size attributes have some builtin limits, test that they
    are respected.

    """
    bb = basic_block

    bb.red = -50
    assert bb.red == 0

    bb.green = 1000
    assert bb.green == 255

    bb.size = -200
    assert bb.size == ipythonblocks._SMALLEST_BLOCK


def test_check_value(basic_block):
    """
    Test the Block._check_value method that enforces color limits,
    converts to int, and checks values are numbers.

    """
    bb = basic_block

    bb.red = 4.56
    assert isinstance(bb.red, int)
    assert bb.red == 5

    bb.blue = 200.1
    assert isinstance(bb.blue, int)
    assert bb.blue == 200

    with pytest.raises(ipythonblocks.InvalidColorSpec):
        bb.green = 'green'


def test_set_colors(basic_block):
    """
    Test the Block.set_colors method.

    """
    bb = basic_block

    bb.set_colors(200, 201, 202)

    assert bb.red == 200
    assert bb.green == 201
    assert bb.blue == 202


def test_rgb_attr(basic_block):
    """
    Test out the .rgb attribute.

    """
    bb = basic_block

    assert bb.rgb == (5, 6, 7)

    bb.rgb = (1, 2, 3)
    assert bb.rgb == (1, 2, 3)
    assert bb._red == 1
    assert bb._green == 2
    assert bb._blue == 3

    with pytest.raises(ValueError):
        bb.rgb = (1, 2)

    with pytest.raises(ValueError):
        bb.rgb = (4, 5, 6, 7, 8)


def test_td(basic_block):
    """
    Test the Block._td proerty that returns an HTML table cell.

    """
    bb = basic_block

    bb._row = 1
    bb._col = 2

    title = ipythonblocks._TITLE.format(bb._row, bb._col,
                                        bb.red, bb.green, bb.blue)
    rgb = ipythonblocks._RGB.format(bb.red, bb.green, bb.blue)
    td = ipythonblocks._TD.format(title, bb.size, rgb)

    assert bb._td == td


def test_repr_html(basic_block, monkeypatch):
    """
    Test the Block._repr_html_ method that returns a single cell HTML table.

    """
    from .test_blockgrid import uuid, fake_uuid

    bb = basic_block

    monkeypatch.setattr(uuid, 'uuid4', fake_uuid)

    table = ipythonblocks._TABLE.format(fake_uuid(), 0,
                                        ipythonblocks._TR.format(bb._td))

    assert bb._repr_html_() == table


def test_str1(basic_block):
    """
    Test the Block.__str__ method used with print.

    """
    bb = basic_block

    s = os.linesep.join(['Block', 'Color: (5, 6, 7)'])

    assert bb.__str__() == s


def test_str2(basic_block):
    """
    Test the Block.__str__ method used with print.

    """
    bb = basic_block
    bb._row = 8
    bb._col = 9

    s = os.linesep.join(['Block [8, 9]', 'Color: (5, 6, 7)'])

    assert bb.__str__() == s

def test_repr(basic_block):
    assert repr(basic_block) == "Block(5, 6, 7, size=20)"

def test_eq():
    b1 = ipythonblocks.Block(0, 0, 0)
    b2 = ipythonblocks.Block(0, 0, 0)
    b3 = ipythonblocks.Block(1, 1, 1)
    b4 = ipythonblocks.Block(0, 0, 0, size=30)

    assert b1 == b1
    assert b1 == b2
    assert b1 != b3
    assert b1 != b4
    assert b1 != 42

def test_hash(basic_block):
    with pytest.raises(TypeError):
        set([basic_block])

def test_update():
    b1 = ipythonblocks.Block(0, 0, 0)
    b2 = ipythonblocks.Block(1, 1, 1, size=30)

    b1._update((42, 42, 42))
    assert b1.rgb == (42, 42, 42)

    b1._update(b2)
    assert b1.rgb == b2.rgb
    assert b1.size == b2.size

    with pytest.raises(ValueError):
        b1._update((1, 2, 3, 4))
