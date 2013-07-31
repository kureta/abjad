# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_Spanner_leaves_01():
    r'''Spanner attaching to container knows about both container and
        also leaves in container.'''

    class MockSpanner(spannertools.Spanner):
        def __init__(self, components=None):
            spannertools.Spanner.__init__(self, components)
        def _copy_keyword_args(self, new):
            pass

    t = Voice(notetools.make_repeated_notes(4))
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(t)
    p = MockSpanner(t)

    assert len(p.components) == 1
    assert p.components[0] is t
    assert len(p.leaves) == 4
    for i, leaf in enumerate(p.leaves):
        assert leaf is t[i]
    assert p.duration == Duration(4, 8)


def test_Spanner_leaves_02():
    r'''Spanner attaching only to leaves makes p.components and p.leaves
        hold the same references.'''

    class MockSpanner(spannertools.Spanner):
        def __init__(self, components=None):
            spannertools.Spanner.__init__(self, components)
        def _copy_keyword_args(self, new):
            pass

    t = Voice(notetools.make_repeated_notes(4))
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(t)
    p = MockSpanner(t[:])

    assert len(p.components) == 4
    assert len(p.leaves) == 4
    for i, leaf in enumerate(p.leaves):
        assert leaf is t[i]
    assert p.duration == Duration(4, 8)


def test_Spanner_leaves_03():
    r'''Spanner attaching to empty container knows about container
        and also about empty leaves.'''

    class MockSpanner(spannertools.Spanner):
        def __init__(self, components=None):
            spannertools.Spanner.__init__(self, components)
        def _copy_keyword_args(self, new):
            pass

    t = Voice([])
    p = MockSpanner(t)

    assert len(p.components) == 1
    assert p.components[0] is t
    assert len(p.leaves) == 0
    assert p.duration == Duration(0)


def test_Spanner_leaves_04():
    r'''Spanner attaching to container with multidimensional contents.
    '''

    class MockSpanner(spannertools.Spanner):
        def __init__(self, components=None):
            spannertools.Spanner.__init__(self, components)
        def _copy_keyword_args(self, new):
            pass

    t = Voice(notetools.make_repeated_notes(4))
    t.insert(1, Container(notetools.make_repeated_notes(2)))
    t.insert(3, Container(notetools.make_repeated_notes(2)))
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(t)
    p = MockSpanner(t)

    r'''
    \new Voice {
        c'8
        {
            cs'8
            d'8
        }
        ef'8
        {
            e'8
            f'8
        }
        fs'8
        g'8
    }
    '''

    assert len(p.components) == 1
    assert len(p.leaves) == 8
    for i, leaf in enumerate(t.select_leaves()):
        assert leaf is t.select_leaves()[i]
    assert p.duration == Duration(8, 8)


def test_Spanner_leaves_05():
    r'''Spanner spanning a mixture of containers and leaves.
    '''

    class MockSpanner(spannertools.Spanner):
        def __init__(self, components=None):
            spannertools.Spanner.__init__(self, components)
        def _copy_keyword_args(self, new):
            pass

    t = Voice(notetools.make_repeated_notes(4))
    t.insert(1, Container(notetools.make_repeated_notes(2)))
    t.insert(3, Container(notetools.make_repeated_notes(2)))
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(t)
    p = MockSpanner(t[0:3])

    r'''
    \new Voice {
        c'8
        {
            cs'8
            d'8
        }
        ef'8
        {
            e'8
            f'8
        }
        fs'8
        g'8
    }
    '''

    assert len(p.components) == 3
    assert p.components[0] is t[0]
    assert p.components[1] is t[1]
    assert p.components[2] is t[2]
    assert len(p.leaves) == 4
    for i, leaf in enumerate(p.leaves):
        assert leaf is t.select_leaves()[i]
    assert p.duration == Duration(4, 8)


def test_Spanner_leaves_06():
    r'''Spanner attaching to container with some parallel contents.
        Spanner absolutely does not descend into parallel container.
        Spanner duration does, however, account for parallel duration.'''

    class MockSpanner(spannertools.Spanner):
        def __init__(self, components=None):
            spannertools.Spanner.__init__(self, components)
        def _copy_keyword_args(self, new):
            pass

    t = Staff(notetools.make_repeated_notes(4))
    t.insert(2, Container(Voice(notetools.make_repeated_notes(2)) * 2))
    t[2].is_parallel = True
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(t)

    r'''
    \new Staff {
        c'8
        cs'8
        <<
            \new Voice {
                d'8
                ef'8
            }
            \new Voice {
                e'8
                f'8
            }
        >>
        fs'8
        g'8
    }
    '''

    assert py.test.raises(AssertionError, 'p = MockSpanner(t)')
#   assert len(p.components) == 1
#   assert p.components[0] is t
#   assert len(p.leaves) == 4
#   assert p.leaves[0] is t[0]
#   assert p.leaves[1] is t[1]
#   assert p.leaves[2] is t[3]
#   assert p.leaves[3] is t[4]
#   assert p.duration == Duration(6, 8)


def test_Spanner_leaves_07():
    r'''Spanner attaching to mixture of parallel and leaf components.
        Spanner absolutely does not descend into parallel container.
        Spanner duration does, however, account for parallel duration.'''

    class MockSpanner(spannertools.Spanner):
        def __init__(self, components=None):
            spannertools.Spanner.__init__(self, components)
        def _copy_keyword_args(self, new):
            pass

    t = Staff(notetools.make_repeated_notes(4))
    t.insert(2, Container(Voice(notetools.make_repeated_notes(2)) * 2))
    t[2].is_parallel = True
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(t)

    r'''
    \new Staff {
        c'8
        cs'8
        <<
            \new Voice {
                d'8
                ef'8
            }
            \new Voice {
                e'8
                f'8
            }
        >>
        fs'8
        g'8
    }
    '''

    assert py.test.raises(AssertionError, 'p = MockSpanner(t[:])')
#   for i, component in enumerate(t[:]):
#      assert component is t[i]
#   assert len(p.leaves) == 4
#   assert p.leaves[0] is t[0]
#   assert p.leaves[1] is t[1]
#   assert p.leaves[2] is t[3]
#   assert p.leaves[3] is t[4]
#   assert p.duration == Duration(6, 8)
