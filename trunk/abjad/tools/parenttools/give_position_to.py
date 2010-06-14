from abjad.tools.parenttools.get_with_indices import get_with_indices
from abjad.tools.parenttools.switch import _switch


def _give_position_to(donors, recipients):
   '''When 'donors' has a parent, find parent.
      Then insert all components in 'recipients'
      in parent immediately before 'donors'.
      Then remove 'donors' from parent.

      When 'donors' has no parent, do nothing.

      Return 'donors'.

      Helper implements no spanner-handling at all.
      Helper is not composer-safe and may cause discontiguous spanners.
   '''
   from abjad.tools import componenttools

   assert componenttools.all_are_contiguous_components_in_same_parent(donors)
   assert componenttools.all_are_components(recipients)

   parent, start, stop = get_with_indices(donors)

   if parent is None:
      return donors

   parent._music[start:start] = recipients
   _switch(recipients, parent)
   _switch(donors, None)

   return donors
