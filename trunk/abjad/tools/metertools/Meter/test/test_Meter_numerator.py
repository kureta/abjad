from abjad import *


def test_Meter_numerator_01( ):
   '''Meters are immutable.
   '''

   t = metertools.Meter(3, 8)

   assert t.numerator == 3
   assert t.denominator == 8
   assert t.duration == Fraction(3, 8)

#   t.numerator = 4
#
#   assert t.numerator == 4
#   assert t.denominator == 8
#   assert t.duration == Fraction(1, 2)
