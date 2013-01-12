"""
ipythonblocks provides a BlockGrid class that displays a colored grid in the
IPython Notebook. The colors can be manipulated, making it useful for
practicing control flow stuctures and quickly seeing the results.

"""

# This file is copyright 2013 by Matt Davis and covered by the license at
# https://github.com/jiffyclub/ipythonblocks/blob/master/LICENSE.txt

import copy
import itertools
import numbers
import os

from operator import iadd

from IPython.display import HTML, display

import sys
if sys.version_info[0] >= 3:
    xrange = range
    from functools import reduce

__all__ = ('Block', 'BlockGrid', 'InvalidColorSpec', '__version__')
__version__ = '1.1.1'

_TABLE = '<table><tbody>{0}</tbody></table>'
_TR = '<tr>{0}</tr>'
_TD = ('<td style="width: {0}px; height: {0}px; padding: 0px;'
       'border: 1px solid white; background-color: {1};"></td>')
_RGB = 'rgb({0}, {1}, {2})'

_SINGLE_ITEM = 'single item'
_SINGLE_ROW = 'single row'
_ROW_SLICE = 'row slice'
_DOUBLE_SLICE = 'double slice'

_SMALLEST_BLOCK = 1


class InvalidColorSpec(Exception):
    """
    Error for a color value that is not a number.

    """
    pass


class Block(object):
    """
    A colored square.

    Parameters
    ----------
    red, green, blue : int
        Integers on the range [0 - 255].
    row, col : int, optional
        The zero-based grid position of this `Block`.
    size : int, optional
        Length of the sides of this block in pixels. One is the lower limit.

    Attributes
    ----------
    red, green, blue : int
        The color values for this `Block`. The color of the `Block` can be
        updated by assigning new values to these attributes.
    row, col : int
        The zero-based grid position of this `Block`.
    size : int
        Length of the sides of this block in pixels. The block size can be
        changed by modifying this attribute. Note that one is the lower limit.

    """

    def __init__(self, red, green, blue, row=None, col=None, size=20):
        self.red = red
        self.green = green
        self.blue = blue
        self._row = row
        self._col = col
        self.size = size

    @staticmethod
    def _check_value(value):
        """
        Check that a value is a number and constrain it to [0 - 255].

        """
        if not isinstance(value, numbers.Number):
            s = 'value must be a number. got {0}.'.format(value)
            raise InvalidColorSpec(s)

        return int(round(min(255, max(0, value))))

    @property
    def red(self):
        return self._red

    @red.setter
    def red(self, value):
        value = self._check_value(value)
        self._red = value

    @property
    def green(self):
        return self._green

    @green.setter
    def green(self, value):
        value = self._check_value(value)
        self._green = value

    @property
    def blue(self):
        return self._blue

    @blue.setter
    def blue(self, value):
        value = self._check_value(value)
        self._blue = value

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = max(_SMALLEST_BLOCK, size)

    def set_colors(self, red, green, blue):
        """
        Updated block colors.

        Parameters
        ----------
        red, green, blue : int
            Integers on the range [0 - 255].

        """
        self.red = red
        self.green = green
        self.blue = blue

    @property
    def td(self):
        """
        The HTML for a table cell with the background color of this Block.

        """
        rgb = _RGB.format(self._red, self._green, self._blue)
        return _TD.format(self._size, rgb)

    def _repr_html_(self):
        return _TABLE.format(_TR.format(self.td))

    def show(self):
        display(HTML(self._repr_html_()))

    def __str__(self):
        s = ['Block',
             'Color: ({0}, {1}, {2})'.format(self._red,
                                             self._green,
                                             self._blue)]

        # add position information if we have it
        if self._row is not None:
            s[0] += ' ({0}, {1})'.format(self._row, self._col)

        return os.linesep.join(s)


class BlockGrid(object):
    """
    A grid of blocks whose colors can be individually controlled.

    Individual blocks have a width and height of 10 screen pixels.
    To get the second Block in the third row use block = grid[1, 2].

    Parameters
    ----------
    width : int
        Number of blocks wide to make the grid.
    height : int
        Number of blocks high to make the grid.
    fill : tuple of int, optional
        An optional initial color for the grid, defaults to black.
        Specified as a tuple of (red, green, blue). E.g.: (10, 234, 198)
    block_size : int, optional
        Length of the sides of grid blocks in pixels. One is the lower limit.

    Attributes
    ----------
    width : int
        Number of blocks along the width of the grid.
    height : int
        Number of blocks along the height of the grid.
    shape : tuple of int
        A tuple of (width, height).
    block_size : int
        Length of the sides of grid blocks in pixels. The block size can be
        changed by modifying this attribute. Note that one is the lower limit.

    """

    def __init__(self, width, height, fill=(0, 0, 0), block_size=20):
        self._width = width
        self._height = height
        self._block_size = block_size
        self._initialize_grid(fill)

    def _initialize_grid(self, fill):
        grid = [[Block(*fill, row=row, col=col, size=self._block_size)
                for col in xrange(self.width)]
                for row in xrange(self.height)]

        self._grid = grid

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def shape(self):
        return (self._width, self._height)

    @property
    def block_size(self):
        return self._block_size

    @block_size.setter
    def block_size(self, size):
        self._block_size = size

        for block in self:
            block.size = size

    @classmethod
    def _view_from_grid(cls, grid):
        """
        Make a new BlockGrid from a list of lists of Block objects.

        """
        new_width = len(grid[0])
        new_height = len(grid)

        new_BG = cls(new_width, new_height)
        new_BG._grid = grid

        return new_BG

    @staticmethod
    def _categorize_index(index):
        """
        Used by __getitem__ and __setitem__ to determine whether the user
        is asking for a single item, single row, or some kind of slice.

        """
        if isinstance(index, int):
            return _SINGLE_ROW

        elif isinstance(index, slice):
            return _ROW_SLICE

        elif isinstance(index, tuple):
            if len(index) not in (1, 2):
                s = 'Invalid index, too many dimensions.'
                raise IndexError(s)

            if isinstance(index[0], slice):
                if isinstance(index[1], (int, slice)):
                    return _DOUBLE_SLICE

            if isinstance(index[1], slice):
                if isinstance(index[0], (int, slice)):
                    return _DOUBLE_SLICE

            elif isinstance(index[0], int) and isinstance(index[0], int):
                return _SINGLE_ITEM

        raise IndexError('Invalid index.')

    def __getitem__(self, index):
        ind_cat = self._categorize_index(index)

        if ind_cat == _SINGLE_ROW:
            return self._grid[index]

        elif ind_cat == _SINGLE_ITEM:
            return self._grid[index[0]][index[1]]

        elif ind_cat == _ROW_SLICE:
            return BlockGrid._view_from_grid(self._grid[index])

        elif ind_cat == _DOUBLE_SLICE:
            new_grid = self._get_double_slice(index)
            return BlockGrid._view_from_grid(new_grid)

    def __setitem__(self, index, value):
        if len(value) != 3:
            s = 'Assigned value must have three integers. got {0}.'
            raise ValueError(s.format(value))

        ind_cat = self._categorize_index(index)

        if ind_cat == _SINGLE_ROW:
            map(lambda b: b.set_colors(*value), self._grid[index])

        elif ind_cat == _SINGLE_ITEM:
            self._grid[index[0]][index[1]].set_colors(*value)

        else:
            if ind_cat == _ROW_SLICE:
                sub_grid = self._grid[index]

            elif ind_cat == _DOUBLE_SLICE:
                sub_grid = self._get_double_slice(index)

            map(lambda b: b.set_colors(*value), itertools.chain(*sub_grid))

    def _get_double_slice(self, index):
        sl_height = index[0]
        sl_width = index[1]

        if isinstance(sl_width, int):
            sl_width = slice(sl_width, sl_width + 1)

        if isinstance(sl_height, int):
            sl_height = slice(sl_height, sl_height + 1)

        rows = self._grid[sl_height]
        grid = [r[sl_width] for r in rows]

        return grid

    def __iter__(self):
        return itertools.chain(*self._grid)

    def _repr_html_(self):
        html = reduce(iadd,
                      (_TR.format(reduce(iadd, (block.td for block in row)))
                       for row in self._grid))

        return _TABLE.format(html)

    def __str__(self):
        s = ['BlockGrid',
             'Shape: {0}'.format(self.shape)]

        return os.linesep.join(s)

    def copy(self):
        """
        Returns an independent copy of this BlockGrid.

        """
        return copy.deepcopy(self)

    def show(self):
        """
        Display colored grid as an HTML table.

        """
        display(HTML(self._repr_html_()))
