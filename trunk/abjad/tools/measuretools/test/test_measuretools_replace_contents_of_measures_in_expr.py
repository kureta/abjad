# -*- encoding: utf-8 -*-
from abjad import *
import py


def test_measuretools_replace_contents_of_measures_in_expr_01():
    r'''Contents duration less than sum of duration of measures.
    Note spacer skip at end of second measure.
    '''

    t = Staff(measuretools.make_measures_with_full_measure_spacer_skips([(1, 8), (3, 16)]))

    r'''
    \new Staff {
        {
            \time 1/8
            s1 * 1/8
        }
        {
            \time 3/16
            s1 * 3/16
        }
    }
    '''

    notes = [Note("c'16"), Note("d'16"), Note("e'16"), Note("f'16")]
    measuretools.replace_contents_of_measures_in_expr(t, notes)

    r'''
    \new Staff {
        {
            \time 1/8
            c'16
            d'16
        }
        {
            \time 3/16
            e'16
            f'16
            s1 * 1/16
        }
    }
    '''

    assert select(t).is_well_formed()
    assert t.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 1/8\n\t\tc'16\n\t\td'16\n\t}\n\t{\n\t\t\\time 3/16\n\t\te'16\n\t\tf'16\n\t\ts1 * 1/16\n\t}\n}"


def test_measuretools_replace_contents_of_measures_in_expr_02():
    r'''Some contents too big for some measures.
    Small measures skipped.
    '''

    t = Staff(measuretools.make_measures_with_full_measure_spacer_skips([(1, 16), (3, 16), (1, 16), (3, 16)]))

    r'''
    \new Staff {
        {
            \time 1/16
            s1 * 1/16
        }
        {
            \time 3/16
            s1 * 3/16
        }
        {
            \time 1/16
            s1 * 1/16
        }
        {
            \time 3/16
            s1 * 3/16
        }
    }
    '''

    notes = [Note("c'8"), Note("d'8")]
    measuretools.replace_contents_of_measures_in_expr(t, notes)

    r'''
    \new Staff {
        {
            \time 1/16
            s1 * 1/16
        }
        {
            \time 3/16
            c'8
            s1 * 1/16
        }
        {
            \time 1/16
            s1 * 1/16
        }
        {
            \time 3/16
            d'8
            s1 * 1/16
        }
    }
    '''

    assert select(t).is_well_formed()
    assert t.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 1/16\n\t\ts1 * 1/16\n\t}\n\t{\n\t\t\\time 3/16\n\t\tc'8\n\t\ts1 * 1/16\n\t}\n\t{\n\t\t\\time 1/16\n\t\ts1 * 1/16\n\t}\n\t{\n\t\t\\time 3/16\n\t\td'8\n\t\ts1 * 1/16\n\t}\n}"


def test_measuretools_replace_contents_of_measures_in_expr_03():
    r'''Raise MissingMeasureError when input expression
    contains no measures.
    '''

    t = Note("c'4")
    notes = [Note("c'8"), Note("d'8")]

    assert py.test.raises(MissingMeasureError, 'measuretools.replace_contents_of_measures_in_expr(t, notes)')


def test_measuretools_replace_contents_of_measures_in_expr_04():
    r'''Raise StopIteration when not enough measures.
    '''

    t = Staff(measuretools.make_measures_with_full_measure_spacer_skips([(1, 8), (1, 8)]))
    notes = [Note("c'16"), Note("d'16"), Note("e'16"), Note("f'16"), Note("g'16"), Note("a'16")]

    assert py.test.raises(StopIteration,
        'measuretools.replace_contents_of_measures_in_expr(t, notes)')


def test_measuretools_replace_contents_of_measures_in_expr_05():
    r'''Populate measures even when not enough total measures.
    '''

    t = Staff(measuretools.make_measures_with_full_measure_spacer_skips([(1, 8), (1, 8)]))
    measuretools.set_always_format_time_signature_of_measures_in_expr(t)
    notes = [Note("c'16"), Note("d'16"), Note("e'16"), Note("f'16"), Note("g'16"), Note("a'16")]

    try:
        measuretools.replace_contents_of_measures_in_expr(t, notes)
    except StopIteration:
        pass

    r'''
    \new Staff {
        {
            \time 1/8
            c'16
            d'16
        }
        {
            \time 1/8
            e'16
            f'16
        }
    }
    '''

    assert select(t).is_well_formed()
    assert t.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 1/8\n\t\tc'16\n\t\td'16\n\t}\n\t{\n\t\t\\time 1/8\n\t\te'16\n\t\tf'16\n\t}\n}"


def test_measuretools_replace_contents_of_measures_in_expr_06():
    r'''Preserve ties.
    '''

    maker = rhythmmakertools.NoteRhythmMaker()
    durations = [(5, 16), (3, 16)]
    leaf_lists = maker(durations)
    leaves = sequencetools.flatten_sequence(leaf_lists)

    measures = measuretools.make_measures_with_full_measure_spacer_skips(durations)
    staff = Staff(measures)
    measures = measuretools.replace_contents_of_measures_in_expr(staff, leaves)

    r'''
    \new Staff {
        {
            \time 5/16
            c'4 ~
            c'16
        }
        {
            \time 3/16
            c'8.
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 5/16\n\t\tc'4 ~\n\t\tc'16\n\t}\n\t{\n\t\t\\time 3/16\n\t\tc'8.\n\t}\n}"
