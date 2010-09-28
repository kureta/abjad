from abjad import *
import py.test


def test_containertools_set_container_multiplier_01( ):
   '''Set multiplier on fixed-duration tuplet 
      by adjusting target duration.'''

   t = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
   assert t.duration.target == Fraction(2, 8)
   assert t.duration.multiplier == Fraction(2, 3)

   containertools.set_container_multiplier(t, Fraction(5, 8))
   assert t.duration.target == Fraction(15, 64)
   assert t.duration.multiplier == Fraction(5, 8)


def test_containertools_set_container_multiplier_02( ):
   '''Set multiplier on rigid measure by adjusting meter.'''

   t = Measure((3, 8), macros.scale(3))
   assert marktools.get_effective_time_signature(t).duration == Fraction(3, 8)

   containertools.set_container_multiplier(t, Fraction(2, 3))
   assert marktools.get_effective_time_signature(t).duration == Fraction(2, 8)
   assert py.test.raises(OverfullMeasureError, 't.format')
