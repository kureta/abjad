import math


def rational_to_flag_count(rational):
   '''.. versionadded:: 1.1.2

   Convert `rational` to nonnegative integer number of flags
   required to notate. ::

      abjad> durtools.rational_to_flag_count(Rational(1, 32))
      3
   '''

   flag_count = max(-int(math.floor(math.log(float(rational._n) /
      rational._d, 2))) - 2, 0)

   return flag_count
