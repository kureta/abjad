# -*- encoding: utf-8 -*-
from abjad import *


def test_HiddenStaffSpanner___init___01():
    r'''Init empty hidden staff spanner.
    '''

    spanner = spannertools.HiddenStaffSpanner()
    assert isinstance(spanner, spannertools.HiddenStaffSpanner)


def test_HiddenStaffSpanner___init___02():
    r'''Hide staff around one measure.
    '''

    t = Staff(Measure((2, 8), "c'8 d'8") * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    measuretools.set_always_format_time_signature_of_measures_in_expr(t)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            \time 2/8
            e'8
            f'8
        }
        {
            \time 2/8
            g'8
            a'8
        }
    }
    '''

    spannertools.HiddenStaffSpanner(t[1])

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            \time 2/8
            \stopStaff
            e'8
            f'8
            \startStaff
        }
        {
            \time 2/8
            g'8
            a'8
        }
    }
    '''

    assert select(t).is_well_formed()
    assert t.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\t\\stopStaff\n\t\te'8\n\t\tf'8\n\t\t\\startStaff\n\t}\n\t{\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8\n\t}\n}"


def test_HiddenStaffSpanner___init___03():
    r'''Hide staff around one leaf.
    '''

    t = Note(0, (1, 8))
    spannertools.HiddenStaffSpanner(t)

    r'''
    \stopStaff
    c'8
    \startStaff
    '''

    assert select(t).is_well_formed()
    assert t.lilypond_format == "\\stopStaff\nc'8\n\\startStaff"
