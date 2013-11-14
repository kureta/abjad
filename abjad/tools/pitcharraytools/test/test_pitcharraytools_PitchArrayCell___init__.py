# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_pitcharraytools_PitchArrayCell___init___01():
    r'''Initializeempty.
    '''

    cell = pitcharraytools.PitchArrayCell()
    assert cell.pitches == []
    assert cell.width == 1


def test_pitcharraytools_PitchArrayCell___init___02():
    r'''Initializewith positive integer width.
    '''

    cell = pitcharraytools.PitchArrayCell(2)
    assert cell.pitches == []
    assert cell.width == 2


def test_pitcharraytools_PitchArrayCell___init___03():
    r'''Initializewith pitch instance.
    '''

    cell = pitcharraytools.PitchArrayCell(pitchtools.NamedPitch(0))
    assert cell.pitches == [pitchtools.NamedPitch(0)]
    assert cell.width == 1


def test_pitcharraytools_PitchArrayCell___init___04():
    r'''Initializewith list of pitch tokens.
    '''

    cell = pitcharraytools.PitchArrayCell([0, 2, 4])
    assert cell.pitches == [pitchtools.NamedPitch(0), pitchtools.NamedPitch(2), pitchtools.NamedPitch(4)]
    assert cell.width == 1


def test_pitcharraytools_PitchArrayCell___init___05():
    r'''Initializewith list of pitch instances.
    '''

    cell = pitcharraytools.PitchArrayCell([pitchtools.NamedPitch(0), pitchtools.NamedPitch(2), pitchtools.NamedPitch(4)])
    assert cell.pitches == [pitchtools.NamedPitch(0), pitchtools.NamedPitch(2), pitchtools.NamedPitch(4)]
    assert cell.width == 1


def test_pitcharraytools_PitchArrayCell___init___06():
    r'''Initializewith list of pitch pairs.
    '''

    cell = pitcharraytools.PitchArrayCell([('c', 4), ('d', 4), ('e', 4)])
    assert cell.pitches == [pitchtools.NamedPitch(0), pitchtools.NamedPitch(2), pitchtools.NamedPitch(4)]
    assert cell.width == 1


def test_pitcharraytools_PitchArrayCell___init___07():
    r'''Initializewith pitch token, width pair.
    '''

    cell = pitcharraytools.PitchArrayCell((0, 2))
    assert cell.pitches == [pitchtools.NamedPitch(0)]
    assert cell.width == 2


def test_pitcharraytools_PitchArrayCell___init___08():
    r'''Initializewith pitch instance, width pair.
    '''

    cell = pitcharraytools.PitchArrayCell((pitchtools.NamedPitch(0), 2))
    assert cell.pitches == [pitchtools.NamedPitch(0)]
    assert cell.width == 2


def test_pitcharraytools_PitchArrayCell___init___09():
    r'''Initializewith pitch token list, width pair.
    '''

    cell = pitcharraytools.PitchArrayCell(([0, 2, 4], 2))
    assert cell.pitches == [pitchtools.NamedPitch(0), pitchtools.NamedPitch(2), pitchtools.NamedPitch(4)]
    assert cell.width == 2


def test_pitcharraytools_PitchArrayCell___init___10():
    r'''Initializewith pitch instance list, width pair.
    '''

    cell = pitcharraytools.PitchArrayCell(([pitchtools.NamedPitch(0), pitchtools.NamedPitch(2), pitchtools.NamedPitch(4)], 2))
    assert cell.pitches == [pitchtools.NamedPitch(0), pitchtools.NamedPitch(2), pitchtools.NamedPitch(4)]
    assert cell.width == 2
