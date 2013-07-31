# -*- encoding: utf-8 -*-
from abjad import *


def test_iterationtools_iterate_tuplets_in_expr_01():

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    tuplet_0 = Tuplet(Fraction(2, 3), staff[:3])
    tuplet_1 = Tuplet(Fraction(2, 3), staff[-3:])

    tuplets = list(iterationtools.iterate_tuplets_in_expr(staff, reverse=True))

    assert tuplets[0] is tuplet_1
    assert tuplets[1] is tuplet_0
from abjad import *


def test_iterationtools_iterate_tuplets_in_expr_02():

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    tuplet_0 = Tuplet(Fraction(2, 3), staff[:3])
    tuplet_1 = Tuplet(Fraction(2, 3), staff[-3:])

    tuplets = list(iterationtools.iterate_tuplets_in_expr(staff))

    assert tuplets[0] is tuplet_0
    assert tuplets[1] is tuplet_1
