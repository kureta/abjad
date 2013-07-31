# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedChromaticPitchClass___init___01():
    r'''Init from name.
    '''

    assert pitchtools.NamedChromaticPitchClass('c') == 'c'
    assert pitchtools.NamedChromaticPitchClass('cs') == 'cs'
    assert pitchtools.NamedChromaticPitchClass('cf') == 'cf'
    assert pitchtools.NamedChromaticPitchClass('cqs') == 'cqs'
    assert pitchtools.NamedChromaticPitchClass('cqf') == 'cqf'


def test_NamedChromaticPitchClass___init___02():
    r'''Init from other named pitch-class instance.
    '''

    npc = pitchtools.NamedChromaticPitchClass('c')
    new = pitchtools.NamedChromaticPitchClass(npc)

    assert new == npc
    assert new is not npc


def test_NamedChromaticPitchClass___init___03():
    r'''Init from note head instance.
    '''

    chord = Chord([0, 2, 3], (1, 4))
    note_head = chord[0]
    npc = pitchtools.NamedChromaticPitchClass(note_head)

    assert npc == pitchtools.NamedChromaticPitchClass('c')
