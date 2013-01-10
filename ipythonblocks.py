"""
ipythonblocks.BlockGrid is a class that displays a colored grid in the
IPython Notebook. The colors can be manipulated, making it useful for
practicing control flow stuctures and quickly seeing the results.

"""

import copy
import numbers

from IPython.display import HTML

__all__ = ['Block', 'BlockGrid', 'InvalidColorSpec']


_TABLE = '<table><tbody>{0}</tbody></table>'
_TR = '<tr>{0}</tr>'
_TD = ('<td style="width: 10px; height: 10px;'
       ' border: 1px solid white; background-color: {0};"></td>')


class InvalidColorSpec(Exception):
    """
    Error for a color value that is not a number.

    """
    pass


class Block(object):
    """
    A class with .red, .green, and .blue attributes.

    """

    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    @staticmethod
    def check_value(value):
        """
        Check that a value is a number and constrain it to [0 - 255].

        """
        if not isinstance(value, numbers.Number):
            raise InvalidColorSpec('value must be a number.')

        return min(255, max(0, value))

    @property
    def red(self):
        return self._red

    @red.setter
    def red(self, value):
        value = self.check_value(value)
        self._red = value

    @property
    def green(self):
        return self._green

    @green.setter
    def green(self, value):
        value = self.check_value(value)
        self._green = value

    @property
    def blue(self):
        return self._blue

    @blue.setter
    def blue(self, value):
        value = self.check_value(value)
        self._blue = value

    @property
    def td(self):
        """
        Return the HTML of a table cell with the background
        color of this Block.

        """
        rgb = 'rgb({0}, {1}, {2})'.format(self._red, self._green, self._blue)
        return _TD.format(rgb)


class BlockGrid(object):
    """
    A grid of squares whose colors can be individually controlled.

    Individual squares have a width and height of 10 screen pixels.
    To get the second Block in the third row use block = grid[1, 2].

    Parameters
    ----------
    width : int
        Number of squares wide to make the grid.
    height : int
        Number of squares high to make the grid.
    fill : tuple of int, optional
        An optional initial color for the grid, defaults to black.
        Specified as a tuple of (red, green, blue). E.g.: (10, 234, 198)

    Attributes
    ----------
    width : int
        Number of squares wide to make the grid.
    height : int
        Number of squares high to make the grid.

    """

    def __init__(self, width, height, fill=(0, 0, 0)):
        self.width = width
        self.height = height
        self._initialize_arrays(fill)

    def _initialize_arrays(self, fill):
        grid = []

        for _ in xrange(self.height):
            grid.append([])

            for _ in xrange(self.width):
                grid[-1].append(Block(*fill))

        self._grid = grid

    def __getitem__(self, index):
        if isinstance(index, tuple):
            if len(index) not in (1, 2):
                s = 'Invalid index, too many dimensions.'
                raise IndexError(s)

            if isinstance(index[0], slice) or isinstance(index[1], slice):
                return self._get_slice(index)

            for i in index:
                if not isinstance(i, int):
                    s = 'Indices must be integers.'
                    raise IndexError(s)

            if len(index) == 1:
                return self._grid[index[0]]
            else:
                return self._grid[index[0]][index[1]]

        elif isinstance(index, int):
            return self._grid[index]

        else:
            raise IndexError('Invalid index.')

    def _get_slice(self, index):
        sl_width = index[0]
        sl_height = index[1]

        if isinstance(sl_width, int):
            sl_width = slice(sl_width, sl_width + 1)

        if isinstance(sl_height, int):
            sl_height = slice(sl_height, sl_height + 1)

        rows = self._grid[sl_height]
        grid = [r[sl_width] for r in rows]

        new_width = len(grid[0])
        new_height = len(grid)

        new_BG = BlockGrid(new_width, new_height)
        new_BG._grid = copy.deepcopy(grid)

        return new_BG

    def _repr_html_(self):
        html = ''

        for row in self._grid:
            tr = ''

            for block in row:
                tr += block.td

            html += _TR.format(tr)

        return _TABLE.format(html)

    def show(self):
        """
        Display blocks as an HTML table.

        """
        return HTML(self._repr_html_())
