from abjad import *
from abjad.tools.timeintervaltools import *
import py.test


def test_timeintervaltools_scale_interval_durations_to_rational_01():
    a = TimeInterval(0, 10, {'a': 1})
    b = TimeInterval(Fraction(5, 3), 10, {'b': 2})
    c = TimeInterval(5, Fraction(61, 7), {'c': 3})
    tree = TimeIntervalTree([a, b, c])
    scalar = Fraction(5, 2)
    scaled = scale_interval_durations_by_rational(tree, scalar)
    assert scaled[0] == TimeInterval(0, Fraction(25, 1), {'a': 1})
    assert scaled[1] == TimeInterval(Fraction(5, 3), Fraction(45, 2), {'b': 2})
    assert scaled[2] == TimeInterval(5, Fraction(100, 7), {'c': 3})

def test_timeintervaltools_scale_interval_durations_to_rational_02():
    tree = TimeIntervalTree([])
    scalar = Fraction(5, 2)
    scaled = scale_interval_durations_by_rational(tree, scalar)
    assert scaled == tree
