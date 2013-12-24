"""
Tests for ipythonblocks communication with ipythonblocks.org.

"""

import json
import string
import sys

import pytest
import responses

from .. import ipythonblocks as ipb

A10 = [a for a in string.lowercase[:10]]


def setup_module(module):
    """
    mock out the get_ipython() function for the tests.

    """
    def get_ipython():
        class ip(object):
            user_ns = {'In': A10}
        return ip()
    ipb.get_ipython = get_ipython


def teardown_module(module):
    del ipb.get_ipython


@pytest.fixture
def data_2x2():
    return [[(1, 2, 3, 4), (5, 6, 7, 8)],
            [(9, 10, 11, 12), (13, 14, 15, 16)]]


@pytest.fixture
def block_grid(data_2x2):
    bg = ipb.BlockGrid(2, 2)
    bg[0, 0].rgb = data_2x2[0][0][:3]
    bg[0, 0].size = data_2x2[0][0][3]
    bg[0, 1].rgb = data_2x2[0][1][:3]
    bg[0, 1].size = data_2x2[0][1][3]
    bg[1, 0].rgb = data_2x2[1][0][:3]
    bg[1, 0].size = data_2x2[1][0][3]
    bg[1, 1].rgb = data_2x2[1][1][:3]
    bg[1, 1].size = data_2x2[1][1][3]
    return bg


@pytest.fixture
def image_grid_ll(data_2x2):
    ig = ipb.ImageGrid(2, 2, origin='lower-left')
    ig[0, 0].rgb = data_2x2[1][0][:3]
    ig[0, 0].size = data_2x2[1][0][3]
    ig[0, 1].rgb = data_2x2[0][0][:3]
    ig[0, 1].size = data_2x2[0][0][3]
    ig[1, 0].rgb = data_2x2[1][1][:3]
    ig[1, 0].size = data_2x2[1][1][3]
    ig[1, 1].rgb = data_2x2[0][1][:3]
    ig[1, 1].size = data_2x2[0][1][3]
    return ig


@pytest.fixture
def image_grid_ul(data_2x2):
    ig = ipb.ImageGrid(2, 2, origin='upper-left')
    ig[0, 0].rgb = data_2x2[0][0][:3]
    ig[0, 0].size = data_2x2[0][0][3]
    ig[0, 1].rgb = data_2x2[1][0][:3]
    ig[0, 1].size = data_2x2[1][0][3]
    ig[1, 0].rgb = data_2x2[0][1][:3]
    ig[1, 0].size = data_2x2[0][1][3]
    ig[1, 1].rgb = data_2x2[1][1][:3]
    ig[1, 1].size = data_2x2[1][1][3]
    return ig


class Test_parse_cells_spec(object):
    def test_single_int(self):
        assert ipb._parse_cells_spec(5, 100) == [5]

    def test_single_int_str(self):
        assert ipb._parse_cells_spec('5', 100) == [5]

    def test_multi_int_str(self):
        assert ipb._parse_cells_spec('2,9,4', 100) == [2, 4, 9]

    def test_slice(self):
        assert ipb._parse_cells_spec(slice(2, 5), 100) == [2, 3, 4]

    def test_slice_str(self):
        assert ipb._parse_cells_spec('2:5', 100) == [2, 3, 4]

    def test_slice_and_int(self):
        assert ipb._parse_cells_spec('4,9:12', 100) == [4, 9, 10, 11]
        assert ipb._parse_cells_spec('9:12,4', 100) == [4, 9, 10, 11]
        assert ipb._parse_cells_spec('4,9:12,16', 100) == [4, 9, 10, 11, 16]
        assert ipb._parse_cells_spec('10,9:12', 100) == [9, 10, 11]


class Test_get_code_cells(object):
    def test_single_int(self):
        assert ipb._get_code_cells(5) == [A10[5]]

    def test_single_int_str(self):
        assert ipb._get_code_cells('5') == [A10[5]]

    def test_multi_int_str(self):
        assert ipb._get_code_cells('2,9,4') == [A10[x] for x in [2, 4, 9]]

    def test_slice(self):
        assert ipb._get_code_cells(slice(2, 5)) == [A10[x] for x in [2, 3, 4]]

    def test_slice_str(self):
        assert ipb._get_code_cells('2:5') == [A10[x] for x in [2, 3, 4]]

    def test_slice_and_int(self):
        assert ipb._get_code_cells('1,3:6') == [A10[x] for x in [1, 3, 4, 5]]
        assert ipb._get_code_cells('3:6,1') == [A10[x] for x in [1, 3, 4, 5]]
        assert ipb._get_code_cells('1,3:6,8') == [A10[x] for x in [1, 3, 4, 5, 8]]
        assert ipb._get_code_cells('4,3:6') == [A10[x] for x in [3, 4, 5]]


@pytest.mark.parametrize('fixture, data',
    [(block_grid, data_2x2),
     (image_grid_ll, data_2x2),
     (image_grid_ul, data_2x2)])
def test_to_simple_grid(fixture, data):
    grid = fixture(data())
    assert grid._to_simple_grid() == data()
