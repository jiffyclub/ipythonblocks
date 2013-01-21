v 1.4
=====

* The lines between cells can be toggled on and off. Turning the lines
  off can sometimes improve the aesthetics of grids, especially at small
  block sizes.
* Added a ``BlockGrid.to_text`` method for easily sending grid data to a file.

v 1.3
=====

* Added ``BlockGrid.animate`` attribute and ``BlockGrid.flash`` method
  to facilitate animation of grid changes in the Notebook.
* Added `Pixel` and `ImageGrid` subclasses that behave more like image
  manipulation libraries.
* Added cell titles so hover the mouse over a block displays the block
  index and color.

v 1.2
=====

* ``Block.row`` and ``Block.col`` are now set by their containing
  ``BlockGrid`` at the time the ``Block`` is returned to the user.
  This means that while iterating over a subgrid the first ``Block``
  will have coordinates (0, 0).
* Getting a single row from a ``BlockGrid`` will return a new ``BlockGrid``
* Raise a TypeError when indexing a ``BlockGrid`` with a length one tuple
* Added a ``Block.colors`` property

v 1.1.1
=======

* Convert assigned floating point numbers to integers for HTML compatibility
* Added the ability to change the size of individual blocks

v 1.1
=====

* Python 3 support (thanks to Thomas Kluyver)
* ``for block in grid`` style iteration
* ``Block`` now has an HTML representation for displaying individual blocks
* ``__str__`` methods on ``Block`` and ``BlockGrid``
* Ability to control block size via ``block_size`` keyword and attribute
  on ``BlockGrid``
