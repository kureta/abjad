# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ExtentIndicator___init___01():
    r'''Initializefrom number.
    '''

    assert tonalanalysistools.ExtentIndicator(7).number == 7


def test_tonalanalysistools_ExtentIndicator___init___02():
    r'''Initializeby reference.
    '''

    extent_indicator = tonalanalysistools.ExtentIndicator(7)
    new = tonalanalysistools.ExtentIndicator(extent_indicator)

    assert new.number == 7
    assert new == extent_indicator
    assert new is not extent_indicator
