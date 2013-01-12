v 1.1.1
=======

* convert assigned floating point numbers to integers for HTML compatibility
* added the ability to change the size of individual blocks

v 1.1
=====

* Python 3 support (thanks to Thomas Kluyver)
* ``for block in grid`` style iteration
* ``Block`` now has an HTML representation for displaying individual blocks
* ``__str__`` methods on ``Block`` and ``BlockGrid``
* Ability to control block size via ``block_size`` keyword and attribute
  on ``BlockGrid``
