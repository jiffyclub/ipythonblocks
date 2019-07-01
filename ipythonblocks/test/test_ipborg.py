"""
Tests for ipythonblocks communication with ipythonblocks.org.

"""

import json
import string
import sys

import mock
import pytest
import responses

from .. import ipythonblocks as ipb

A10 = [a for a in string.ascii_lowercase[:10]]


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


@pytest.fixture(name='block_grid')
def block_grid_fixture(data_2x2):
    return block_grid(data_2x2)


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


@pytest.fixture(name='image_grid_ll')
def image_grid_ll_fixture(data_2x2):
    return image_grid_ll(data_2x2)


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


@pytest.fixture(name='image_grid_ul')
def image_grid_ul_fixture(data_2x2):
    return image_grid_ul(data_2x2)


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


@pytest.mark.parametrize(
    'fixture',
    [block_grid, image_grid_ll, image_grid_ul]
)
def test_to_simple_grid(fixture, data_2x2):
    grid = fixture(data_2x2)
    assert grid._to_simple_grid() == data_2x2


@pytest.mark.parametrize(
    'test_grid, ref_grid',
    [(ipb.BlockGrid(2, 2), block_grid),
     (ipb.ImageGrid(2, 2, origin='upper-left'), image_grid_ul),
     (ipb.ImageGrid(2, 2, origin='lower-left'), image_grid_ll)]
)
def test_load_simple_grid(test_grid, ref_grid, data_2x2):
    ref_grid = ref_grid(data_2x2)
    test_grid._load_simple_grid(data_2x2)
    assert test_grid == ref_grid


@responses.activate
@mock.patch.object(ipb, '__version__', 'ipb_version')
@mock.patch.object(ipb, '_POST_URL', 'http://www.ipythonblocks.org/post_url')
def test_BlockGrid_post_to_web(data_2x2, block_grid):
    expected = {
        'python_version': tuple(sys.version_info),
        'ipb_version': ipb.__version__,
        'ipb_class': 'BlockGrid',
        'code_cells': None,
        'secret': False,
        'grid_data': {
            'lines_on': block_grid.lines_on,
            'width': block_grid.width,
            'height': block_grid.height,
            'blocks': data_2x2
        }
    }
    expected = json.dumps(expected)

    responses.add(responses.POST, ipb._POST_URL,
                  body=json.dumps({'url': 'url'}).encode('utf-8'),
                  status=200, content_type='application/json')

    url = block_grid.post_to_web()

    assert url == 'url'
    assert len(responses.calls) == 1

    req = responses.calls[0].request
    assert req.url == ipb._POST_URL
    assert req.body == expected


@responses.activate
@mock.patch.object(ipb, '__version__', 'ipb_version')
@mock.patch.object(ipb, '_POST_URL', 'http://www.ipythonblocks.org/post_url')
def test_ImageGrid_ul_post_to_web(data_2x2, image_grid_ul):
    expected = {
        'python_version': tuple(sys.version_info),
        'ipb_version': ipb.__version__,
        'ipb_class': 'ImageGrid',
        'code_cells': None,
        'secret': False,
        'grid_data': {
            'lines_on': image_grid_ul.lines_on,
            'width': image_grid_ul.width,
            'height': image_grid_ul.height,
            'blocks': data_2x2
        }
    }
    expected = json.dumps(expected)

    responses.add(responses.POST, ipb._POST_URL,
                  body=json.dumps({'url': 'url'}).encode('utf-8'),
                  status=200, content_type='application/json')

    url = image_grid_ul.post_to_web()

    assert url == 'url'
    assert len(responses.calls) == 1

    req = responses.calls[0].request
    assert req.url == ipb._POST_URL
    assert req.body == expected


@responses.activate
@mock.patch.object(ipb, '_GET_URL_PUBLIC', 'http://www.ipythonblocks.org/get_url/{0}')
def test_BlockGrid_from_web(data_2x2):
    grid_id = 'abc'
    get_url = ipb._GET_URL_PUBLIC.format(grid_id)
    resp = {
        'lines_on': True,
        'width': 2,
        'height': 2,
        'blocks': data_2x2
    }

    responses.add(responses.GET, get_url,
                  body=json.dumps(resp).encode('utf-8'), status=200,
                  content_type='application/json')

    grid = ipb.BlockGrid.from_web(grid_id)

    assert grid.height == resp['height']
    assert grid.width == resp['width']
    assert grid.lines_on == resp['lines_on']
    assert grid._to_simple_grid() == data_2x2

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == get_url


@responses.activate
@mock.patch.object(ipb, '_GET_URL_SECRET', 'http://www.ipythonblocks.org/get_url/{0}')
def test_ImageGrid_ul_from_web(data_2x2):
    grid_id = 'abc'
    get_url = ipb._GET_URL_SECRET.format(grid_id)
    resp = {
        'lines_on': True,
        'width': 2,
        'height': 2,
        'blocks': data_2x2
    }

    responses.add(responses.GET, get_url,
                  body=json.dumps(resp).encode('utf-8'), status=200,
                  content_type='application/json')

    origin = 'upper-left'
    grid = ipb.ImageGrid.from_web(grid_id, secret=True, origin=origin)

    assert grid.height == resp['height']
    assert grid.width == resp['width']
    assert grid.lines_on == resp['lines_on']
    assert grid._to_simple_grid() == data_2x2
    assert grid.origin == origin

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == get_url
