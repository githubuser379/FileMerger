# -*- coding: utf-8 -*-

import pytest
from isetools.skeleton import fib

__author__ = "John Smith"
__copyright__ = "John Smith"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
