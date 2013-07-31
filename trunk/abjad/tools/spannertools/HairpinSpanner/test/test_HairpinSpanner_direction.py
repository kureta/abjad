# -*- encoding: utf-8 -*-
from abjad import *


def test_HairpinSpanner_direction_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    hairpin = spannertools.HairpinSpanner(staff[:], 'p < f', direction=Down)

    r'''
    \new Staff {
        c'8 _ \< _ \p
        d'8
        e'8
        f'8 _ \f
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\tc'8 _ \\< _ \\p\n\td'8\n\te'8\n\tf'8 _ \\f\n}"
