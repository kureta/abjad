# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_HarmonicCounterpointInterval_semitones_01():
    r'''Counterpoint intervals evaluate to no exact number of semitones.
    '''

    hcpi = pitchtools.HarmonicCounterpointInterval(15)

    assert py.test.raises(NotImplementedError, 'hcpi.semitones')
