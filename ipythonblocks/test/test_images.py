"""
Tests for the ability to save images of grids.

"""
import os
import tempfile

import mock
import pytest
from PIL import Image

from ..ipythonblocks import BlockGrid, ImageGrid, colors


@pytest.fixture
def bg():
    grid = BlockGrid(2, 2, block_size=1, lines_on=False)
    grid[0, 0] = colors.Yellow
    grid[0, 1] = colors.Blue
    grid[1, 0] = colors.Red
    grid[1, 1] = colors.Green
    return grid


@pytest.fixture
def ig():
    grid = ImageGrid(2, 2, block_size=1, lines_on=False, origin='lower-left')
    grid[0, 0] = colors.Red
    grid[0, 1] = colors.Yellow
    grid[1, 0] = colors.Green
    grid[1, 1] = colors.Blue
    return grid


@pytest.fixture
def bg_png(request):
    name = tempfile.NamedTemporaryFile(suffix='.png').name

    def fin():
        os.remove(name)
    request.addfinalizer(fin)

    return name


@pytest.fixture
def ig_png(request):
    name = tempfile.NamedTemporaryFile(suffix='.png').name

    def fin():
        os.remove(name)
    request.addfinalizer(fin)

    return name


def test_fixtures_equal(bg, ig):
    assert bg == ig


def test_save_image(bg, ig, bg_png, ig_png):
    bg.save_image(bg_png)
    ig.save_image(ig_png)

    bg_im = Image.open(bg_png)
    ig_im = Image.open(ig_png)

    for im in (bg_im, ig_im):
        assert im.format == 'PNG'
        assert im.size == (bg.width, bg.height)

    for bg_block, bg_pix, ig_pix in zip(bg, bg_im.getdata(), ig_im.getdata()):
        assert bg_block.rgb == bg_pix
        assert bg_block.rgb == ig_pix


def test_show_image(bg, ig):
    from .. import ipythonblocks

    with mock.patch.object(ipythonblocks, 'display') as display:
        bg.show_image()
        display.assert_called_once()

    with mock.patch.object(ipythonblocks, 'display') as display:
        ig.show_image()
        display.assert_called_once()
