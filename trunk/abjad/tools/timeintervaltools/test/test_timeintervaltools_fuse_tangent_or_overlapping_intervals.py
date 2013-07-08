from abjad import *
from abjad.tools.timeintervaltools import *
import py.test


def test_timeintervaltools_fuse_tangent_or_overlapping_intervals_01():
    tree = TimeIntervalTree(timeintervaltools.make_test_intervals())
    fused_tree = fuse_tangent_or_overlapping_intervals(tree)
    target_signatures = [(0, 3), (5, 13), (15, 23), (25, 30), (32, 37)]
    actual_signatures = [interval.signature for interval in fused_tree]
    assert target_signatures == actual_signatures
    assert tree.duration == fused_tree.duration
