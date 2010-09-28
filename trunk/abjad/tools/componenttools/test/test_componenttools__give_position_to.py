from abjad import *
from abjad.tools.componenttools._give_position_to import _give_position_to


def test_componenttools__give_position_to_01( ):
   '''Not composer-safe.'''

   t = Voice(macros.scale(4))
   spannertools.BeamSpanner(t[:])
   notes = macros.scale(2, Fraction(1, 16))

   _give_position_to(t[0:1], notes)

   "Container t is now ..."

   r'''
   \new Voice {
      c'16
      d'16
      d'8
      e'8
      f'8 ]
   }
   '''

   assert t.format == "\\new Voice {\n\tc'16\n\td'16\n\td'8\n\te'8\n\tf'8 ]\n}"

   "Container t now carries a discontiguous spanner."

   assert not componenttools.is_well_formed_component(t)
