# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_DynamicTextSpanner___init___01():
    r'''Initializeempty dynamic text spanner.
    '''

    spanner = spannertools.DynamicTextSpanner()
    assert isinstance(spanner, spannertools.DynamicTextSpanner)
