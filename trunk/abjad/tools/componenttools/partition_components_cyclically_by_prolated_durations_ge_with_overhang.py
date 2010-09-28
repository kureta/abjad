from abjad.tools.componenttools._group_components_by_durations import \
   _group_components_by_durations


def partition_components_cyclically_by_prolated_durations_ge_with_overhang(
   components, prolated_durations):
   r'''Partition `components` cyclically by `prolated_durations` greater than
   or equal. Allow for terminal overhang part::

      abjad> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
      abjad> macros.diatonicize(staff)
      abjad> f(staff)
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
         {
            \time 2/8
            b'8
            c''8
         }
      }
      
   ::
      
      abjad> groups = componenttools.partition_components_cyclically_by_prolated_durations_ge_with_overhang(
         staff.leaves, [Fraction(3, 16), Fraction(1, 16)])

   ::
   
      abjad> for group in groups:
      ...     group
      ... 
      [Note(c', 8), Note(d', 8)]
      [Note(e', 8)]
      [Note(f', 8), Note(g', 8)]
      [Note(a', 8)]
      [Note(b', 8), Note(c'', 8)]

   Return list of lists.

   .. note:: function works not just on components but on any durated objects including spanners.
   '''
   
   parts = _group_components_by_durations('prolated', components, prolated_durations, 
      fill = 'greater', cyclic = True, overhang = True)

   return parts
