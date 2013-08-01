import pytest

from .. import ipythonblocks


@pytest.fixture
def upper_left():
    return ipythonblocks.ImageGrid(2, 3, (7, 8, 9), 20, True, 'upper-left')


@pytest.fixture
def lower_left():
    return ipythonblocks.ImageGrid(2, 3, (7, 8, 9), 20, True, 'lower-left')


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


def test_getitem_bad_index_ul(upper_left):
    ul = upper_left

    with pytest.raises(IndexError):
        ul[1]

    with pytest.raises(IndexError):
        ul[1:]

    with pytest.raises(IndexError):
        ul[0, 3]

    with pytest.raises(IndexError):
        ul[2, 0]


def test_getitem_bad_index_ll(lower_left):
    ll = lower_left

    with pytest.raises(IndexError):
        ll[1]

    with pytest.raises(IndexError):
        ll[1:]

    with pytest.raises(IndexError):
        ll[0, 3]

    with pytest.raises(IndexError):
        ll[2, 0]


def test_setitem_bad_index(upper_left):
    ul = upper_left

    with pytest.raises(IndexError):
        ul[1] = (4, 5, 6)

    with pytest.raises(IndexError):
        ul[1:] = (4, 5, 6)


def test_getitem_upper_left_single(upper_left):
    ul = upper_left

    for row in range(ul.height):
        for col in range(ul.width):
            assert ul[col, row] is ul._grid[row][col]


def test_getitem_upper_left_slice(upper_left):
    ul = upper_left

    ng = ul[:1, :2]

    assert ng.width == 1
    assert ng.height == 2
    assert ng._grid == [[ul._grid[0][0]], [ul._grid[1][0]]]


def test_getitem_lower_left_single(lower_left):
    ll = lower_left

    for row in range(ll.height):
        for col in range(ll.width):
            trow = ll.height - row - 1
            assert ll[col, row] is ll._grid[trow][col]


def test_getitem_lower_left_single_neg(lower_left):
    ll = lower_left

    ll[1, 2] = (1, 2, 3)

    pix = ll[-1, -1]

    assert pix.red == 1
    assert pix.green == 2
    assert pix.blue == 3


def test_getitem_lower_left_slice(lower_left):
    ll = lower_left

    ng = ll[:1, :2]

    assert ng.width == 1
    assert ng.height == 2
    assert ng._grid == [[ll._grid[-2][0]], [ll._grid[-1][0]]]


def test_setitem_lower_left_single(lower_left):
    ll = lower_left

    ll[0, 1].set_colors(201, 202, 203)

    assert ll._grid[-2][0].red == 201
    assert ll._grid[-2][0].green == 202
    assert ll._grid[-2][0].blue == 203


def test_setitem_lower_left_slice(lower_left):
    ll = lower_left

    ll[:, ::2] = (201, 202, 203)

    for pix in ll._grid[0]:
        assert pix.red == 201
        assert pix.green == 202
        assert pix.blue == 203

    for pix in ll._grid[2]:
        assert pix.red == 201
        assert pix.green == 202
        assert pix.blue == 203


def test_slice_assignment(lower_left):
    ll = lower_left

    ll[1, 1] = (42, 42, 42)
    ll[0, 0] = ll[1, 1]
    assert ll[0, 0].rgb == (42, 42, 42)


def test_setitem_with_grid_ul(upper_left):
    og = upper_left.copy()
    og[:, :] = (4, 5, 6)

    upper_left[:1, :2] = og[-1:, -2:]

    for b in upper_left:
        if b.col < 1 and b.row < 2:
            assert b.rgb == (4, 5, 6)
        else:
            assert b.rgb == (7, 8, 9)


def test_setitem_with_grid_ll(lower_left):
    og = lower_left.copy()
    og[:, :] = (4, 5, 6)

    lower_left[:1, :2] = og[-1:, -2:]

    for b in lower_left:
        if b.col < 1 and b.row < 2:
            assert b.rgb == (4, 5, 6)
        else:
            assert b.rgb == (7, 8, 9)
