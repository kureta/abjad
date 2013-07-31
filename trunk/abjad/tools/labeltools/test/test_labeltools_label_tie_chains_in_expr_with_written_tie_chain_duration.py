# -*- encoding: utf-8 -*-
from abjad import *


def test_labeltools_label_tie_chains_in_expr_with_written_tie_chain_duration_01():

    staff = Staff(notetools.make_repeated_notes(4))
    tuplettools.FixedDurationTuplet(Duration(2, 8), staff[:3])
    spannertools.TieSpanner(staff.select_leaves()[:2])
    spannertools.TieSpanner(staff.select_leaves()[2:])
    labeltools.label_tie_chains_in_expr_with_written_tie_chain_duration(staff)

    r'''
    \new Staff {
        \times 2/3 {
            c'8 ~
                _ \markup {
                    \small
                        1/4
                    }
            c'8
            c'8 ~
                _ \markup {
                    \small
                        1/4
                    }
        }
        c'8
    }
    '''

    assert select(staff).is_well_formed()
    assert staff.lilypond_format == "\\new Staff {\n\t\\times 2/3 {\n\t\tc'8 ~\n\t\t\t_ \\markup {\n\t\t\t\t\\small\n\t\t\t\t\t1/4\n\t\t\t\t}\n\t\tc'8\n\t\tc'8 ~\n\t\t\t_ \\markup {\n\t\t\t\t\\small\n\t\t\t\t\t1/4\n\t\t\t\t}\n\t}\n\tc'8\n}"
