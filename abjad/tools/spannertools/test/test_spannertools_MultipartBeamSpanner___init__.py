# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_MultipartBeamSpanner___init___01():
    r'''Initializeempty multipart beam spanner.
    '''

    beam = spannertools.MultipartBeamSpanner()
    assert isinstance(beam, spannertools.MultipartBeamSpanner)
