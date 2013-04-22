import os
import uuid
import pytest

from .. import ipythonblocks


def fake_uuid():
    return 'abc'


@pytest.fixture
def basic_grid():
    return ipythonblocks.BlockGrid(5, 6, (1, 2, 3), 20, True)


@pytest.fixture
def oneD_grid():
    return ipythonblocks.BlockGrid(5, fill=(1, 2, 3), block_size=11,
                                   lines_on=False)


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


def test_oneD_api(oneD_grid):
    """
    Test the API of a 1D grid.

    """
    odg = oneD_grid

    assert odg.width == 5
    assert odg.height == 0
    assert odg.shape == (5,)
    assert odg.block_size == 11
    assert odg.lines_on is False


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


def test_oneD_init(oneD_grid):
    """
    Test basics of a 1D grid.

    """
    odg = oneD_grid

    for c in range(odg.width):
        assert odg[c].red == 1
        assert odg[c].green == 2
        assert odg[c].blue == 3
        assert odg[c].row == 0
        assert odg[c].col == c


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

    assert isinstance(ng, ipythonblocks.BlockGrid)
    assert ng.shape == (2, 2)

    ng[1, 1].set_colors(200, 201, 202)

    for block in (ng[1, 1], bg[1, 1]):
        assert block.red == 200
        assert block.green == 201
        assert block.blue == 202


def test_oneD_view(oneD_grid):
    """
    Test we get a view slicing a 1D grid.

    """
    odg = oneD_grid
    ng = odg[1:4]

    assert isinstance(ng, ipythonblocks.BlockGrid)
    assert ng.shape == (3,)

    ng[1].set_colors(200, 201, 202)

    for block in (ng[1], odg[2]):
        assert block.red == 200
        assert block.green == 201
        assert block.blue == 202


def test_view_coords(basic_grid):
    """
    Make sure that when we get a view that it has its own appropriate
    coordinates.

    """
    ng = basic_grid[-2:, -2:]

    assert ng.shape == (2, 2)

    coords = ((0, 0), (0, 1), (1, 0), (1, 1))

    for b, c in zip(ng, coords):
        assert b.row == c[0]
        assert b.col == c[1]


def test_oneD_view_coords(oneD_grid):
    """
    Test coords are set correctly in a slice of a 1D grid.

    """
    ng = oneD_grid[1:4]

    for b, c in zip(ng, range(ng.width)):
        assert b.row == 0
        assert b.col == c


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


def test_oneD_str(oneD_grid):
    """
    Test the BlockGrid.__str__ method used with print for 1D grid.

    """
    odg = oneD_grid

    s = os.linesep.join(['BlockGrid', 'Shape: (5,)'])

    assert odg.__str__() == s


def test_repr_html(monkeypatch):
    """
    HTML repr should be the same for a 1, 1 BlockGrid as for a single Block.
    (As long as the BlockGrid border is off.)

    """
    bg = ipythonblocks.BlockGrid(1, 1, lines_on=False)

    monkeypatch.setattr(uuid, 'uuid4', fake_uuid)

    assert bg._repr_html_() == bg[0, 0]._repr_html_()


def test_oneD_repr_html(monkeypatch):
    """
    HTML repr should be the same for a 1, 1 BlockGrid as for a single Block.
    (As long as the BlockGrid border is off.)

    """
    bg = ipythonblocks.BlockGrid(1, lines_on=False)

    monkeypatch.setattr(uuid, 'uuid4', fake_uuid)

    assert bg._repr_html_() == bg[0]._repr_html_()


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

    # single block
    # result is not the same as above because bg[1] returns a 1D grid
    # with a row index of 0.
    block = bg[1][2]

    assert isinstance(block, ipythonblocks.Block)
    assert block.row == 0
    assert block.col == 2

    # single row
    ng = bg[2]

    assert isinstance(ng, ipythonblocks.BlockGrid)
    assert ng.shape == (bg.width,)

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

    # single block
    bg[0][1] = colors
    assert bg[0][1].rgb == colors

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


def test_oneD_getitem(oneD_grid):
    """
    Test indexing with a 1D grid.

    """
    odg = oneD_grid

    # single block
    block = odg[2]
    assert isinstance(block, ipythonblocks.Block)
    assert block.row == 0
    assert block.col == 2

    # single block
    # this is actually not an error because it simplified the internals
    # of BlockGrid to store even 1D grids as a nested list and to support
    # two-integer lookups. of course, the row index has to be zero.
    block = odg[0, 2]
    assert isinstance(block, ipythonblocks.Block)
    assert block.row == 0
    assert block.col == 2

    # slice
    ng = odg[1:4]
    assert isinstance(ng, ipythonblocks.BlockGrid)
    assert ng.shape == (3,)

    # strided slice
    ng = odg[::2]
    assert isinstance(ng, ipythonblocks.BlockGrid)
    assert ng.shape == (3,)


def test_oneD_setitem(oneD_grid):
    """
    Test modifying the colors of blocks in a 1D grid.

    """
    odg = oneD_grid
    colors = (21, 22, 23)

    # single block
    odg[0] = colors
    assert odg[0].rgb == colors

    # single block
    # this is actually not an error because it simplified the internals
    # of BlockGrid to store even 1D grids as a nested list and to support
    # two-integer lookups. of course, the row index has to be zero.
    odg[0, 1] = colors
    assert odg[1].rgb == colors

    # slice
    odg[-2:] = colors
    for block in odg[-2:]:
        assert block.rgb == colors

    # strided slice
    odg[::2] = colors
    for block in odg[::2]:
        assert block.rgb == colors


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


def test_oneD_to_text(capsys):
    """
    Test using the BlockGrid.to_text method with a 1D grid.
    The height written out should be 0.

    """
    bg = ipythonblocks.BlockGrid(2, block_size=20)

    bg[0, 0].rgb = (1, 2, 3)
    bg[0, 1].rgb = (4, 5, 6)

    ref = ['# width height',
           '2 0',
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
