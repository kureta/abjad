# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_OctavationSpanner___init___01():
    r'''Initializeempty octavation spanner.
    '''

    octavation = spannertools.OctavationSpanner()
    assert isinstance(octavation, spannertools.OctavationSpanner)
