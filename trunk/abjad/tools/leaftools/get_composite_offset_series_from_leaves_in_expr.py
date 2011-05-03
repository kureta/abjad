from abjad.tools.leaftools.iterate_leaves_forward_in_expr import iterate_leaves_forward_in_expr


def get_composite_offset_series_from_leaves_in_expr(expr):
   r'''.. versionadded:: 1.1.2

   Get composite offset series from leaves in `expr`::

      abjad> staff_1 = Staff([tuplettools.FixedDurationTuplet((4, 8), notetools.make_repeated_notes(3))])
      abjad> staff_2 = Staff(notetools.make_repeated_notes(4))
      abjad> score = Score([staff_1, staff_2])
      abjad> macros.diatonicize(score)
      abjad> f(score)
         \new Score <<
                 \new Staff {
                         \times 4/3 {
                                 c'8
                                 d'8
                                 e'8
                         }
                 }
                 \new Staff {
                         f'8
                         g'8
                         a'8
                         b'8
                 }
         >>
      abjad> leaftools.get_composite_offset_series_from_leaves_in_expr(score)
      [Fraction(0, 1), Fraction(1, 8), Fraction(1, 6), Fraction(1, 4), Fraction(1, 3), Fraction(3, 8), (Fraction(1, 2)]

   Equal to list of unique start and stop offsets of leaves in `expr`.

   Return list of fractions.
   '''

   offsets = [ ]

   for leaf in iterate_leaves_forward_in_expr(expr):
      start_offset = leaf._offset.start
      if start_offset not in offsets:
         offsets.append(start_offset)
      stop_offset = leaf._offset.stop
      if stop_offset not in offsets:
         offsets.append(stop_offset)

   offsets.sort( )

   return offsets
