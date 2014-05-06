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


def test_flash_should_clear_first(monkeypatch):
    calls = []
    monkeypatch.setattr(ipythonblocks, "clear_output", lambda: calls.append("clear_output"))
    monkeypatch.setattr(ipythonblocks.BlockGrid, "show", lambda self: calls.append("show"))
    monkeypatch.setattr("time.sleep", lambda interval: calls.append("sleep(%d)" % interval))
    grid = ipythonblocks.BlockGrid(1, 1)
    grid.flash(3)
    assert calls[0] == "clear_output"
    assert calls[1] == "show"
    assert calls[2] == "sleep(3)"
