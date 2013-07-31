# -*- encoding: utf-8 -*-
from abjad import *


def test_componenttools_split_components_at_offsets_01():
    r'''Cyclically split note in score. Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(
        staff[0][1:2], 
        [(3, 64)],
        cyclic=True,
        fracture_spanners=False,
        )

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'32. ~
            d'32. ~
            d'32 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert len(parts) == 3
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 [ (\n\t\td'32. ~\n\t\td'32. ~\n\t\td'32 ]\n\t}\n\t{\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_02():
    r'''Cyclically split consecutive notes in score. Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(
        staff.select_leaves(), 
        [(3, 32)], cyclic=True,
        fracture_spanners=False,
        )

    r'''
    \new Staff {
        {
            \time 2/8
            c'16. [ ( ~
            c'32
            d'16. ~
            d'32 ]
        }
        {
            e'16. [ ~
            e'32
            f'8 ] )
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert len(parts) == 6
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'16. [ ( ~\n\t\tc'32\n\t\td'16 ~\n\t\td'16 ]\n\t}\n\t{\n\t\te'32 [ ~\n\t\te'16.\n\t\tf'16. ~\n\t\tf'32 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_03():
    r'''Cyclically split measure in score. Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(staff[:1], [(3, 32)],
        cyclic=True, fracture_spanners=False, tie_split_notes=False)

    r'''
    \new Staff {
        {
            \time 3/32
            c'16. [ (
        }
        {
            c'32
            d'16
        }
        {
            \time 2/32
            d'16 ]
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert len(parts) == 3
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 3/32\n\t\tc'16. [ (\n\t}\n\t{\n\t\tc'32\n\t\td'16\n\t}\n\t{\n\t\t\\time 2/32\n\t\td'16 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_04():
    r'''Cyclically split consecutive measures in score. Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(staff[:], [(3, 32)],
        cyclic=True, fracture_spanners=False, tie_split_notes=False)

    r'''
    \new Staff {
        {
            \time 3/32
            c'16. [ (
        }
        {
            c'32
            d'16
        }
        {
            \time 2/32
            d'16 ]
        }
        {
            \time 1/32
            e'32 [
        }
        {
            \time 3/32
            e'16.
        }
        {
            f'16.
        }
        {
            \time 1/32
            f'32 ] )
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert len(parts) == 6
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 3/32\n\t\tc'16. [ (\n\t}\n\t{\n\t\tc'32\n\t\td'16\n\t}\n\t{\n\t\t\\time 2/32\n\t\td'16 ]\n\t}\n\t{\n\t\t\\time 1/32\n\t\te'32 [\n\t}\n\t{\n\t\t\\time 3/32\n\t\te'16.\n\t}\n\t{\n\t\tf'16.\n\t}\n\t{\n\t\t\\time 1/32\n\t\tf'32 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_05():
    r'''Cyclically split orphan measures. Don't fracture spanners.
    '''

    measures = [Measure((2, 8), "c'8 d'8"), Measure((2, 8), "e'8 f'8")]
    select(measures).attach_spanners(spannertools.BeamSpanner)

    parts = componenttools.split_components_at_offsets(measures, [(3, 32)],
        cyclic=True, fracture_spanners=False, tie_split_notes=False)

    music = sequencetools.flatten_sequence(parts)
    staff = Staff(music)

    r'''
    \new Staff {
        {
            \time 3/32
            c'16. [
        }
        {
            c'32
            d'16
        }
        {
            \time 2/32
            d'16 ]
        }
        {
            \time 1/32
            e'32 [
        }
        {
            \time 3/32
            e'16.
        }
        {
            f'16.
        }
        {
            \time 1/32
            f'32 ]
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert len(parts) == 6
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 3/32\n\t\tc'16. [\n\t}\n\t{\n\t\tc'32\n\t\td'16\n\t}\n\t{\n\t\t\\time 2/32\n\t\td'16 ]\n\t}\n\t{\n\t\t\\time 1/32\n\t\te'32 [\n\t}\n\t{\n\t\t\\time 3/32\n\t\te'16.\n\t}\n\t{\n\t\tf'16.\n\t}\n\t{\n\t\t\\time 1/32\n\t\tf'32 ]\n\t}\n}"


def test_componenttools_split_components_at_offsets_06():
    r'''Cyclically split note in score. Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(staff[0][1:], [(1, 32)],
        cyclic=True, fracture_spanners=False, tie_split_notes=True)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'32 ~
            d'32 ~
            d'32 ~
            d'32 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert len(parts) == 4
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 [ (\n\t\td'32 ~\n\t\td'32 ~\n\t\td'32 ~\n\t\td'32 ]\n\t}\n\t{\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_07():
    r'''Cyclically split consecutive notes in score. Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(staff.select_leaves(), [(1, 16)],
        cyclic=True, fracture_spanners=False, tie_split_notes=True)

    r'''
    \new Staff {
        {
            \time 2/8
            c'16 [ ( ~
            c'16
            d'16 ~
            d'16 ]
        }
        {
            e'16 [ ~
            e'16
            f'16 ~
            f'16 ] )
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert len(parts) == 8
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'16 [ ( ~\n\t\tc'16\n\t\td'16 ~\n\t\td'16 ]\n\t}\n\t{\n\t\te'16 [ ~\n\t\te'16\n\t\tf'16 ~\n\t\tf'16 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_08():
    r'''Cyclically split measure in score. Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(staff[:1], [(1, 16)],
        cyclic=True, fracture_spanners=False, tie_split_notes=True)

    r'''
    \new Staff {
        {
            \time 1/16
            c'16 [ ( ~
        }
        {
            c'16
        }
        {
            d'16 ~
        }
        {
            d'16 ]
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert len(parts) == 4
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 1/16\n\t\tc'16 [ ( ~\n\t}\n\t{\n\t\tc'16\n\t}\n\t{\n\t\td'16 ~\n\t}\n\t{\n\t\td'16 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_09():
    r'''Cyclically split consecutive measures in score. Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(staff[:], [(3, 32)],
        cyclic=True, fracture_spanners=False, tie_split_notes=True)

    r'''
    \new Staff {
        {
            \time 3/32
            c'16. [ ( ~
        }
        {
            c'32
            d'16 ~
        }
        {
            \time 2/32
            d'16 ]
        }
        {
            \time 1/32
            e'32 [ ~
        }
        {
            \time 3/32
            e'16.
        }
        {
            f'16. ~
        }
        {
            \time 1/32
            f'32 ] )
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert len(parts) == 6
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 3/32\n\t\tc'16. [ ( ~\n\t}\n\t{\n\t\tc'32\n\t\td'16 ~\n\t}\n\t{\n\t\t\\time 2/32\n\t\td'16 ]\n\t}\n\t{\n\t\t\\time 1/32\n\t\te'32 [ ~\n\t}\n\t{\n\t\t\\time 3/32\n\t\te'16.\n\t}\n\t{\n\t\tf'16. ~\n\t}\n\t{\n\t\t\\time 1/32\n\t\tf'32 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_10():
    r'''Cyclically split note in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(
        staff[0][1:2], 
        [(3, 64)], 
        cyclic=True,
        fracture_spanners=True,
        )

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'32. )
            d'32. ( )
            d'64 ( ~
            d'64 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert len(parts) == 3
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 [ (\n\t\td'32. ) ~\n\t\td'32. ( ) ~\n\t\td'32 ] (\n\t}\n\t{\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_11():
    r'''Cyclically split consecutive notes in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(
        staff.select_leaves(), [(3, 32)], cyclic=True, fracture_spanners=True)

    r'''
    \new Staff {
        {
            \time 2/8
            c'16. [ ( ) ~
            c'32 (
            d'16 ) ~
            d'16 ] (
        }
        {
            e'32 [ ) ~
            e'16. (
            f'16. ) ~
            f'32 ] ( )
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert len(parts) == 6
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'16. [ ( ) ~\n\t\tc'32 (\n\t\td'16 ) ~\n\t\td'16 ] (\n\t}\n\t{\n\t\te'32 [ ) ~\n\t\te'16. (\n\t\tf'16. ) ~\n\t\tf'32 ] ( )\n\t}\n}"


def test_componenttools_split_components_at_offsets_12():
    r'''Cyclically split measure in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(staff[:1], [(3, 32)],
        cyclic=True, fracture_spanners=True, tie_split_notes=False)

    r'''
    \new Staff {
        {
            \time 3/32
            c'16. [ ] ( )
        }
        {
            c'32 [ (
            d'16 ] )
        }
        {
            \time 2/32
            d'16 [ ] (
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert len(parts) == 3
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 3/32\n\t\tc'16. [ ] ( )\n\t}\n\t{\n\t\tc'32 [ (\n\t\td'16 ] )\n\t}\n\t{\n\t\t\\time 2/32\n\t\td'16 [ ] (\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_13():
    r'''Cyclically split consecutive measures in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(staff[:], [(3, 32)],
        cyclic=True, fracture_spanners=True, tie_split_notes=False)

    r'''
    \new Staff {
        {
            \time 3/32
            c'16. [ ] ( )
        }
        {
            c'32 [ (
            d'16 ] )
        }
        {
            \time 2/32
            d'16 [ ] (
        }
        {
            \time 1/32
            e'32 [ ] )
        }
        {
            \time 3/32
            e'16. [ ] ( )
        }
        {
            f'16. [ ] ( )
        }
        {
            \time 1/32
            f'32 [ ] ( )
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert len(parts) == 6
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 3/32\n\t\tc'16. [ ] ( )\n\t}\n\t{\n\t\tc'32 [ (\n\t\td'16 ] )\n\t}\n\t{\n\t\t\\time 2/32\n\t\td'16 [ ] (\n\t}\n\t{\n\t\t\\time 1/32\n\t\te'32 [ ] )\n\t}\n\t{\n\t\t\\time 3/32\n\t\te'16. [ ] ( )\n\t}\n\t{\n\t\tf'16. [ ] ( )\n\t}\n\t{\n\t\t\\time 1/32\n\t\tf'32 [ ] ( )\n\t}\n}"


def test_componenttools_split_components_at_offsets_14():
    r'''Cyclically split orphan notes.
    '''

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]

    parts = componenttools.split_components_at_offsets(
        notes, [(3, 32)], cyclic=True, fracture_spanners=True)

    music = sequencetools.flatten_sequence(parts)
    staff = Staff(music)

    r'''
    \new Staff {
        c'16. ~
        c'32
        d'16 ~
        d'16
        e'32 ~
        e'16.
        f'16. ~
        f'32
    }
    '''

    assert select(staff).is_well_formed()
    assert len(parts) == 6
    assert staff.lilypond_format == "\\new Staff {\n\tc'16. ~\n\tc'32\n\td'16 ~\n\td'16\n\te'32 ~\n\te'16.\n\tf'16. ~\n\tf'32\n}"


def test_componenttools_split_components_at_offsets_15():
    r'''Cyclically split orphan measures. Fracture spanners.
    '''

    measures = [Measure((2, 8), "c'8 d'8"), Measure((2, 8), "e'8 f'8")]
    select(measures).attach_spanners(spannertools.BeamSpanner)

    parts = componenttools.split_components_at_offsets(measures, [(3, 32)],
        cyclic=True, fracture_spanners=True, tie_split_notes=False)

    music = sequencetools.flatten_sequence(parts)
    staff = Staff(music)

    r'''
    \new Staff {
        {
            \time 3/32
            c'16. [ ]
        }
        {
            c'32 [
            d'16 ]
        }
        {
            \time 2/32
            d'16 [ ]
        }
        {
            \time 1/32
            e'32 [ ]
        }
        {
            \time 3/32
            e'16. [ ]
        }
        {
            f'16. [ ]
        }
        {
            \time 1/32
            f'32 [ ]
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert len(parts) == 6
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 3/32\n\t\tc'16. [ ]\n\t}\n\t{\n\t\tc'32 [\n\t\td'16 ]\n\t}\n\t{\n\t\t\\time 2/32\n\t\td'16 [ ]\n\t}\n\t{\n\t\t\\time 1/32\n\t\te'32 [ ]\n\t}\n\t{\n\t\t\\time 3/32\n\t\te'16. [ ]\n\t}\n\t{\n\t\tf'16. [ ]\n\t}\n\t{\n\t\t\\time 1/32\n\t\tf'32 [ ]\n\t}\n}"


def test_componenttools_split_components_at_offsets_16():
    r'''Cyclically split note in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(staff[0][1:], [(1, 32)],
        cyclic=True, fracture_spanners=True, tie_split_notes=True)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'32 ) ~
            d'32 ( ) ~
            d'32 ( ) ~
            d'32 ] (
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert len(parts) == 4
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 [ (\n\t\td'32 ) ~\n\t\td'32 ( ) ~\n\t\td'32 ( ) ~\n\t\td'32 ] (\n\t}\n\t{\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_17():
    r'''Cyclically split consecutive notes in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(staff.select_leaves(), [(1, 16)],
        cyclic=True, fracture_spanners=True, tie_split_notes=True)

    r'''
    \new Staff {
        {
            \time 2/8
            c'16 [ ( ) ~
            c'16 (
            d'16 ) ~
            d'16 ] (
        }
        {
            e'16 [ ) ~
            e'16 (
            f'16 ) ~
            f'16 ] ( )
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert len(parts) == 8
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'16 [ ( ) ~\n\t\tc'16 (\n\t\td'16 ) ~\n\t\td'16 ] (\n\t}\n\t{\n\t\te'16 [ ) ~\n\t\te'16 (\n\t\tf'16 ) ~\n\t\tf'16 ] ( )\n\t}\n}"


def test_componenttools_split_components_at_offsets_18():
    r'''Cyclically split measure in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(staff[:1], [(1, 16)],
        cyclic=True, fracture_spanners=True, tie_split_notes=True)

    r'''
    \new Staff {
        {
            \time 1/16
            c'16 [ ] ( ) ~
        }
        {
            c'16 [ ] ( )
        }
        {
            d'16 [ ] ( ) ~
        }
        {
            d'16 [ ] (
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert len(parts) == 4
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 1/16\n\t\tc'16 [ ] ( ) ~\n\t}\n\t{\n\t\tc'16 [ ] ( )\n\t}\n\t{\n\t\td'16 [ ] ( ) ~\n\t}\n\t{\n\t\td'16 [ ] (\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_19():
    r'''Cyclically split consecutive measures in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(staff[:], [(3, 32)],
        cyclic=True, fracture_spanners=True, tie_split_notes=True)

    r'''
    \new Staff {
        {
            \time 3/32
            c'16. [ ] ( ) ~
        }
        {
            c'32 [ (
            d'16 ] ) ~
        }
        {
            \time 2/32
            d'16 [ ] (
        }
        {
            \time 1/32
            e'32 [ ] ) ~
        }
        {
            \time 3/32
            e'16. [ ] ( )
        }
        {
            f'16. [ ] ( ) ~
        }
        {
            \time 1/32
            f'32 [ ] ( )
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert len(parts) == 6
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 3/32\n\t\tc'16. [ ] ( ) ~\n\t}\n\t{\n\t\tc'32 [ (\n\t\td'16 ] ) ~\n\t}\n\t{\n\t\t\\time 2/32\n\t\td'16 [ ] (\n\t}\n\t{\n\t\t\\time 1/32\n\t\te'32 [ ] ) ~\n\t}\n\t{\n\t\t\\time 3/32\n\t\te'16. [ ] ( )\n\t}\n\t{\n\t\tf'16. [ ] ( ) ~\n\t}\n\t{\n\t\t\\time 1/32\n\t\tf'32 [ ] ( )\n\t}\n}"


def test_componenttools_split_components_at_offsets_20():
    r'''Force split measure in score. Do not fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(
        staff[:1], [(1, 32), (3, 32), (5, 32)],
        cyclic=False, fracture_spanners=False, tie_split_notes=False)

    r'''
    \new Staff {
        {
            \time 1/32
            c'32 [ (
        }
        {
            \time 3/32
            c'16.
        }
        {
            \time 4/32
            d'8 ]
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert len(parts) == 3
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 1/32\n\t\tc'32 [ (\n\t}\n\t{\n\t\t\\time 3/32\n\t\tc'16.\n\t}\n\t{\n\t\t\\time 4/32\n\t\td'8 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_21():
    r'''Force split consecutive measures in score. Do not fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    r'''
    \new Staff {
        {
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(
        staff[:], [(1, 32), (3, 32), (5, 32)],
        cyclic=False, fracture_spanners=False, tie_split_notes=False)

    r'''
    \new Staff {
        {
            \time 1/32
            c'32 [ (
        }
        {
            \time 3/32
            c'16.
        }
        {
            \time 4/32
            d'8 ]
        }
        {
            \time 1/32
            e'32 [
        }
        {
            \time 7/32
            e'16.
            f'8 ] )
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert len(parts) == 4
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 1/32\n\t\tc'32 [ (\n\t}\n\t{\n\t\t\\time 3/32\n\t\tc'16.\n\t}\n\t{\n\t\t\\time 4/32\n\t\td'8 ]\n\t}\n\t{\n\t\t\\time 1/32\n\t\te'32 [\n\t}\n\t{\n\t\t\\time 7/32\n\t\te'16.\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_22():
    r'''Force split measure in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(
        staff[:1], [(1, 32), (3, 32), (5, 32)],
        cyclic=False, fracture_spanners=True, tie_split_notes=False)

    r'''
    \new Staff {
        {
            \time 1/32
            c'32 [ ] ( )
        }
        {
            \time 3/32
            c'16. [ ] ( )
        }
        {
            \time 4/32
            d'8 [ ] (
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert len(parts) == 3
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 1/32\n\t\tc'32 [ ] ( )\n\t}\n\t{\n\t\t\\time 3/32\n\t\tc'16. [ ] ( )\n\t}\n\t{\n\t\t\\time 4/32\n\t\td'8 [ ] (\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_23():
    r'''Force split consecutive measures in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    select(staff[:]).attach_spanners(spannertools.BeamSpanner)
    spannertools.SlurSpanner(staff.select_leaves())

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(
        staff[:], [(1, 32), (3, 32), (5, 32)],
        cyclic=False, fracture_spanners=True, tie_split_notes=False)

    r'''
    \new Staff {
        {
            \time 1/32
            c'32 [ ] ( )
        }
        {
            \time 3/32
            c'16. [ ] ( )
        }
        {
            \time 4/32
            d'8 [ ] (
        }
        {
            \time 1/32
            e'32 [ ] )
        }
        {
            \time 7/32
            e'16. [ (
            f'8 ] )
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert len(parts) == 4
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 1/32\n\t\tc'32 [ ] ( )\n\t}\n\t{\n\t\t\\time 3/32\n\t\tc'16. [ ] ( )\n\t}\n\t{\n\t\t\\time 4/32\n\t\td'8 [ ] (\n\t}\n\t{\n\t\t\\time 1/32\n\t\te'32 [ ] )\n\t}\n\t{\n\t\t\\time 7/32\n\t\te'16. [ (\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_24():
    r'''Force split orphan note. Offsets sum to less than note duration.
    '''

    note = Note("c'4")

    parts = componenttools.split_components_at_offsets(
        [note], [(1, 32), (5, 32)],
        cyclic=False, fracture_spanners=True, tie_split_notes=False)

    notes = sequencetools.flatten_sequence(parts)
    staff = Staff(notes)

    r'''
    \new Staff {
        c'32 ~
        c'8 ~
        c'32 ~
        c'16
    }
    '''

    assert select(staff).is_well_formed()
    assert len(parts) == 3
    assert staff.lilypond_format == "\\new Staff {\n\tc'32 ~\n\tc'8 ~\n\tc'32 ~\n\tc'16\n}"


def test_componenttools_split_components_at_offsets_25():
    r'''Force split note in score. Fracture spanners.
    '''

    staff = Staff("c'8 [ ]")

    r'''
    \new Staff {
        c'8 [ ]
    }
    '''

    parts = componenttools.split_components_at_offsets(
        staff[:], [(1, 64), (5, 64)],
        cyclic=False, fracture_spanners=True, tie_split_notes=False)

    r'''
    \new Staff {
        c'64 [ ]
        c'16 [ ~
        c'64 ] ~
        c'32 [ ]
    }
    '''

    assert select(staff).is_well_formed()
    assert staff.lilypond_format == "\\new Staff {\n\tc'64 [ ] ~\n\tc'16 [ ~\n\tc'64 ] ~\n\tc'32 [ ]\n}"
