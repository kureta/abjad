# -*- encoding: utf-8 -*-
from abjad import *


def test_MelodicDiatonicIntervalClass___init___01():
    r'''Unisons and octaves are treated differently.
    '''

    mdic = pitchtools.MelodicDiatonicIntervalClass('perfect', -15)
    assert str(mdic) == '-P8'

    mdic = pitchtools.MelodicDiatonicIntervalClass('perfect', -8)
    assert str(mdic) == '-P8'

    mdic = pitchtools.MelodicDiatonicIntervalClass('perfect', 8)
    assert str(mdic) == '+P8'

    mdic = pitchtools.MelodicDiatonicIntervalClass('perfect', 15)
    assert str(mdic) == '+P8'


def test_MelodicDiatonicIntervalClass___init___02():
    r'''Unisons and octaves are treated differently.
    '''

    mdic = pitchtools.MelodicDiatonicIntervalClass('perfect', -1)
    assert str(mdic) == 'P1'

    mdic = pitchtools.MelodicDiatonicIntervalClass('perfect', 1)
    assert str(mdic) == 'P1'
