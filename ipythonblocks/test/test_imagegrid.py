import pytest

from .. import ipythonblocks


@pytest.fixture
def upper_left():
    return ipythonblocks.ImageGrid(5, 6, (7, 8, 9), 20, 'upper-left')


@pytest.fixture
def lower_left():
    return ipythonblocks.ImageGrid(5, 6, (7, 8, 9), 20, 'lower-left')


def test_init_bad_origin():
    """
    Test for an error with a bad origin keyword.

    """
    with pytest.raises(ValueError):
        ipythonblocks.ImageGrid(5, 6, origin='nowhere')


def test_basic_api(upper_left, lower_left):
    """
    Test basic interfaces different from BlockGrid.

    """
    ul = upper_left
    ll = lower_left

    assert ul.origin == 'upper-left'
    assert ll.origin == 'lower-left'

    with pytest.raises(AttributeError):
        ul.block_size = 50


def test_getitem(upper_left):
    ul = upper_left

    with pytest.raises(IndexError):
        ul[5]

    with pytest.raises(IndexError):
        ul[5:]


