v 1.9
=====

* Added ``show_color_triple`` function as a convenience for displaying
  (red, green, blue) triplets without breaking them out into components
* Added ``Color`` wrapper for colors in the ``colors`` and ``fui_colors``
  dictionaries to support ``.red``, ``.green``, and ``.blue`` attribute
  access for the component colors

v 1.8
=====

* Add ``clear`` function
* Use ``clear_output(wait=True)`` to avoid flickering in animations

v 1.7
=====

* Added ``show_image`` and ``save_image`` for embedding an image in the
  Notebook and saving an image to a file, respectively.

v 1.6
=====

* Added ``post_to_web`` and ``from_web`` methods for for communication
  with ipythonblocks.org.
* Added a ``display_time`` keyword to the ``flash()`` method.
* Changed the ``animate`` property to a method so that it can take
  a ``stop_time`` keyword to control the amount of time between loop steps.
* Fixed an error with improperly set attributes on views of grids.
* Fixed negative indexing in lower-left origin ImageGrids.
* Fixed an error that allowed too-large indices in lower-left origin ImageGrids.
* Allow color assignment from Blocks/Pixels, not just tuples. (Thanks @wolever.)

v 1.5
=====

* Fixed an issue with an index of -1 in a 2D slice.
* Fixed a display issue with show_color on Firefox.
* Added a dictionary of HTML colors called ``colors``

v 1.4
=====

* The lines between cells can be toggled on and off. Turning the lines
  off can sometimes improve the aesthetics of grids, especially at small
  block sizes.
* Added a ``BlockGrid.to_text`` method for easily sending grid data to a file.
* Added a ``show_color`` function that just shows a stripe of a given color.
* Added an ``embed_colorpicker`` function that embeds the website
  http://www.colorpicker.com/ in the Notebook.

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
