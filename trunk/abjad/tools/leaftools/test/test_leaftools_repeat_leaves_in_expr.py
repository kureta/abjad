# -*- encoding: utf-8 -*-
from abjad import *


def test_leaftools_repeat_leaves_in_expr_01():
    r'''Multiply each leaf in voice by 1.
    '''

    t = Voice("c'8 d'8 e'8")
    p = spannertools.BeamSpanner(t[:])
    leaftools.repeat_leaves_in_expr(t, total=2)

    r'''
    \new Voice {
      c'8 [
      c'8
      d'8
      d'8
      e'8
      e'8 ]
    }
    '''

    assert select(t).is_well_formed()
    assert t.lilypond_format == "\\new Voice {\n\tc'8 [\n\tc'8\n\td'8\n\td'8\n\te'8\n\te'8 ]\n}"


def test_leaftools_repeat_leaves_in_expr_02():
    r'''Multiply each leaf in voice by 2.
    '''

    t = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(t[:])
    leaftools.repeat_leaves_in_expr(t, total=3)

    r'''
    \new Voice {
      c'8 [
      c'8
      c'8
      d'8
      d'8
      d'8
      e'8
      e'8
      e'8 ]
    }
    '''

    assert select(t).is_well_formed()
    assert t.lilypond_format == "\\new Voice {\n\tc'8 [\n\tc'8\n\tc'8\n\td'8\n\td'8\n\td'8\n\te'8\n\te'8\n\te'8 ]\n}"
