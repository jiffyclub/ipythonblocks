import os
import uuid
import pytest

from .. import ipythonblocks


def fake_uuid():
    return 'abc'


@pytest.fixture
def basic_grid():
    return ipythonblocks.BlockGrid(5, 6, (1, 2, 3), 20, True)


def test_basic_api(basic_grid):
    """
    Check that inputs are going to the right attributes and that assignment
    works when it should and not when it shouldn't.

    """
    bg = basic_grid

    assert bg.width == 5
    with pytest.raises(AttributeError):
        bg.width = 20

    assert bg.height == 6
    with pytest.raises(AttributeError):
        bg.height = 20

    assert bg.shape == (5, 6)
    assert bg.block_size == 20
    assert bg.lines_on is True


def test_grid_init(basic_grid):
    """
    Test that the grid is properly initialized.

    """
    bg = basic_grid

    for r in range(bg.height):
        for c in range(bg.width):
            assert bg[r, c].size == 20
            assert bg[r, c].red == 1
            assert bg[r, c].green == 2
            assert bg[r, c].blue == 3
            assert bg[r, c].row == r
            assert bg[r, c].col == c


def test_change_block_size(basic_grid):
    """
    Test that all blocks are properly resized when changing the
    BlockGrid.block_size attribute.

    """
    bg = basic_grid

    bg.block_size = 10
    assert bg.block_size == 10

    for block in bg:
        assert block.size == 10


def test_change_lines_on(basic_grid):
    """
    Test changing the BlockGrid.lines_on attribute.

    """
    bg = basic_grid

    assert bg.lines_on is True

    bg.lines_on = False
    assert bg.lines_on is False

    with pytest.raises(ValueError):
        bg.lines_on = 5

    with pytest.raises(ValueError):
        bg.lines_on = 'asdf'


def test_view(basic_grid):
    """
    Check that getting a new BlockGrid object via slicing returns a view
    and not a copy.

    """
    bg = basic_grid
    ng = bg[:2, :2]

    ng[1, 1].set_colors(200, 201, 202)

    for block in (ng[1, 1], bg[1, 1]):
        assert block.red == 200
        assert block.green == 201
        assert block.blue == 202


def test_view_coords(basic_grid):
    """
    Make sure that when we get a view that it has its own appropriate
    coordinates.

    """
    ng = basic_grid[-2:, -2:]

    coords = ((0, 0), (0, 1), (1, 0), (1, 1))

    for b, c in zip(ng, coords):
        assert b.row == c[0]
        assert b.col == c[1]


def test_copy(basic_grid):
    """
    Check that getting a new BlockGrid via BlockGrid.copy returns a totally
    independent copy and not a view.

    """
    bg = basic_grid
    ng = bg[:2, :2].copy()

    ng[1, 1].set_colors(200, 201, 202)

    assert ng[1, 1].red == 200
    assert ng[1, 1].green == 201
    assert ng[1, 1].blue == 202
    assert bg[1, 1].red == 1
    assert bg[1, 1].green == 2
    assert bg[1, 1].blue == 3


def test_str(basic_grid):
    """
    Test the BlockGrid.__str__ method used with print.

    """
    bg = basic_grid

    s = os.linesep.join(['BlockGrid', 'Shape: (5, 6)'])

    assert bg.__str__() == s


def test_repr_html(monkeypatch):
    """
    HTML repr should be the same for a 1, 1 BlockGrid as for a single Block.
    (As long as the BlockGrid border is off.)

    """
    bg = ipythonblocks.BlockGrid(1, 1, lines_on=False)

    monkeypatch.setattr(uuid, 'uuid4', fake_uuid)

    assert bg._repr_html_() == bg[0, 0]._repr_html_()


def test_iter():
    """
    Test that we do complete, row first iteration.

    """
    bg = ipythonblocks.BlockGrid(2, 2)

    coords = ((0, 0), (0, 1), (1, 0), (1, 1))

    for b, c in zip(bg, coords):
        assert b.row == c[0]
        assert b.col == c[1]


def test_bad_index(basic_grid):
    """
    Test for the correct errors with bad indices.

    """
    bg = basic_grid

    with pytest.raises(IndexError):
        bg[1, 2, 3, 4]

    with pytest.raises(IndexError):
        bg[{4: 5}]

    with pytest.raises(TypeError):
        bg[1, ]

    with pytest.raises(IndexError):
        bg[0, 5]

    with pytest.raises(IndexError):
        bg[6, 0]


def test_bad_colors(basic_grid):
    """
    Make sure this gets the right error when trying to assign something
    other than three integers.

    """
    with pytest.raises(ValueError):
        basic_grid[0, 0] = (1, 2, 3, 4)


def test_getitem(basic_grid):
    """
    Exercise a bunch of different indexing.

    """
    bg = basic_grid

    # single block
    block = bg[1, 2]

    assert isinstance(block, ipythonblocks.Block)
    assert block.row == 1
    assert block.col == 2

    # single row
    ng = bg[2]

    assert isinstance(ng, ipythonblocks.BlockGrid)
    assert ng.shape == (bg.width, 1)

    # two rows
    ng = bg[1:3]

    assert isinstance(ng, ipythonblocks.BlockGrid)
    assert ng.shape == (bg.width, 2)

    # one row via a slice
    ng = bg[2, :]

    assert isinstance(ng, ipythonblocks.BlockGrid)
    assert ng.shape == (bg.width, 1)

    # one column
    ng = bg[:, 2]

    assert isinstance(ng, ipythonblocks.BlockGrid)
    assert ng.shape == (1, bg.height)

    # 2 x 2 subgrid
    ng = bg[:2, :2]

    assert isinstance(ng, ipythonblocks.BlockGrid)
    assert ng.shape == (2, 2)

    # strided slicing
    ng = bg[::3, ::3]

    assert isinstance(ng, ipythonblocks.BlockGrid)
    assert ng.shape == (2, 2)

    # one column / one row with a -1 index
    # testing fix for #7
    ng = bg[-1, :]

    assert isinstance(ng, ipythonblocks.BlockGrid)
    assert ng.shape == (bg.width, 1)

    ng = bg[1:4, -1]

    assert isinstance(ng, ipythonblocks.BlockGrid)
    assert ng.shape == (1, 3)


def test_setitem(basic_grid):
    """
    Test assigning colors to blocks.

    """
    bg = basic_grid
    colors = (21, 22, 23)

    # single block
    bg[0, 0] = colors
    assert bg[0, 0].rgb == colors

    # single row
    bg[2] = colors
    for block in bg[2]:
        assert block.rgb == colors

    # two rows
    bg[3:5] = colors
    for block in bg[3:5]:
        assert block.rgb == colors

    # one row via a slice
    bg[1, :] = colors
    for block in bg[1, :]:
        assert block.rgb == colors

    # one column
    bg[:, 5] = colors
    for block in bg[:, 5]:
        assert block.rgb == colors

    # 2 x 2 subgrid
    bg[:2, :2] = colors
    for block in bg[:2, :2]:
        assert block.rgb == colors

    # strided slicing
    bg[::3, ::3] = colors
    for block in bg[::3, ::3]:
        assert block.rgb == colors


def test_setitem_to_block(basic_grid):
    """
    Test assigning a Block to a BlockGrid.
    """
    bg = basic_grid
    bg[0, 0] = (0, 0, 0)
    bg[1, 1] = bg[0, 0]
    assert bg[0, 0] == bg[1, 1]
    assert bg[1, 1].rgb == (0, 0, 0)


def test_setitem_with_grid(basic_grid):
    og = basic_grid.copy()
    og[:] = (4, 5, 6)

    basic_grid[:1, :2] = og[-1:, -2:]

    for b in basic_grid:
        if b.row < 1 and b.col < 2:
            assert b.rgb == (4, 5, 6)
        else:
            assert b.rgb == (1, 2, 3)


def test_setitem_raises(basic_grid):
    og = basic_grid.copy()

    with pytest.raises(ipythonblocks.ShapeMismatch):
        basic_grid[:, :] = og[:2, :2]

    with pytest.raises(TypeError):
        basic_grid[0, 0] = og[:2, :2]


def test_to_text(capsys):
    """
    Test using the BlockGrid.to_text method.

    """
    bg = ipythonblocks.BlockGrid(2, 1, block_size=20)

    bg[0, 0].rgb = (1, 2, 3)
    bg[0, 1].rgb = (4, 5, 6)

    ref = ['# width height',
           '2 1',
           '# block size',
           '20',
           '# initial color',
           '0 0 0',
           '# row column red green blue',
           '0 0 1 2 3',
           '0 1 4 5 6']
    ref = os.linesep.join(ref) + os.linesep

    bg.to_text()
    out, err = capsys.readouterr()

    assert out == ref
