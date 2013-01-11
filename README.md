# `ipythonblocks`

`ipythonblocks` is a teaching tool for use with the [IPython][] Notebook.
It provides a `BlockGrid` object whose representation is an HTML table.
Individual table cells are represented by `Block` objects that have `.red`,
`.green`, and `.blue` attributes by which the color of that cell can be
specified.

`ipythonblocks` allows students to experiment with Python flow control concepts
and immediately see the effects of their code represented in a colorful,
attractive way. `BlockGrid` objects can be indexed and sliced like 2D NumPy
arrays making them good practice for learning how to access arrays.

See the [demo notebook][demo] for more on using `ipythonblocks`.

[IPython]: http://ipython.org
[demo]: http://nbviewer.ipython.org/urls/raw.github.com/jiffyclub/ipythonblocks/master/ipythonblocks_demo.ipynb
