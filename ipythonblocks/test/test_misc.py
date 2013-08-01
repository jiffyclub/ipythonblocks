"""
Test miscellaneous utility functions in the ipythonblocks module.

"""

from .. import ipythonblocks


def test_flatten():
    # single thing
    for x in ipythonblocks._flatten(1):
        assert x == 1

    # simple list
    thing = range(5)
    for i, x in enumerate(ipythonblocks._flatten(thing)):
        assert x == i

    # nested lists
    thing = [[0], [1, 2], [3], [4, 5, [6]]]
    for i, x in enumerate(ipythonblocks._flatten(thing)):
        assert x == i

