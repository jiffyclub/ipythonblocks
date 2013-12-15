``ipythonblocks``
=================

``ipythonblocks`` is a teaching tool for use with the IPython_ Notebook.
It provides a ``BlockGrid`` object whose representation is an HTML table.
Individual table cells are represented by ``Block`` objects that have ``.red``,
``.green``, and ``.blue`` attributes by which the color of that cell can be
specified.

``ipythonblocks`` allows students to experiment with Python flow control concepts
and immediately see the effects of their code represented in a colorful,
attractive way. ``BlockGrid`` objects can be indexed and sliced like 2D NumPy
arrays making them good practice for learning how to access arrays.

See these demo notebooks for more on using ``ipythonblocks``:

* `Practicing with RGB`_
* `Basic usage`_ with explanations
* `Fun examples`_
* `Animation`_
* `ImageGrid`_
* Going from a `JPEG to BlockGrid`_ and text
* A programatic `firework animation`_

Install
-------

``ipythonblocks`` can be installed with ``pip``::

    pip install ipythonblocks

or ``easy_install``::

    easy_install ipythonblocks

However, the package is contained in a single ``.py`` file and if you prefer
you can just grab `ipythonblocks.py`_ and copy it to wherever you
want to use it (useful for packaging with other teaching materials).

Dependencies
------------

Required dependencies:

* Python_ >= 2.6
* IPython_

Optional dependencies:

* requests_ >= 1.0 (for posting and getting to/from `ipythonblocks.org`_)

Testing dependencies:

* pytest_ >= 2.3, (for the test suite, see below)
* responses_ >= 0.1
* mock_ (dependency of responses)

Demo dependencies:

* PIL_ (for ``starry_night_to_text.ipynb``)


Testing
-------

The test suite is written using pytest_, so you can run the test suite
with::

    py.test

.. _IPython: http://ipython.org
.. _Practicing with RGB: http://nbviewer.ipython.org/urls/raw.github.com/jiffyclub/ipythonblocks/master/demos/learning_colors.ipynb
.. _Basic usage: http://nbviewer.ipython.org/urls/raw.github.com/jiffyclub/ipythonblocks/master/demos/ipythonblocks_demo.ipynb
.. _Fun examples: http://nbviewer.ipython.org/urls/raw.github.com/jiffyclub/ipythonblocks/master/demos/ipythonblocks_fun.ipynb
.. _Animation: http://nbviewer.ipython.org/urls/raw.github.com/jiffyclub/ipythonblocks/master/demos/ipythonblocks_animation.ipynb
.. _ImageGrid: http://nbviewer.ipython.org/urls/raw.github.com/jiffyclub/ipythonblocks/master/demos/ipythonblocks_imagegrid.ipynb
.. _JPEG to BlockGrid: http://nbviewer.ipython.org/urls/raw.github.com/jiffyclub/ipythonblocks/master/demos/starry_night_to_text.ipynb
.. _firework animation: http://nbviewer.ipython.org/urls/raw.github.com/jiffyclub/ipythonblocks/master/demos/Firework.ipynb
.. _ipythonblocks.py: https://github.com/jiffyclub/ipythonblocks/blob/master/ipythonblocks/ipythonblocks.py
.. _Python: http://python.org/
.. _pytest: http://pytest.org/
.. _requests: http://docs.python-requests.org/en/latest/
.. _PIL: http://www.pythonware.com/products/pil/
.. _responses: https://github.com/dropbox/responses
.. _mock: http://www.voidspace.org.uk/python/mock/
.. _ipythonblocks.org: http://ipythonblocks.org
