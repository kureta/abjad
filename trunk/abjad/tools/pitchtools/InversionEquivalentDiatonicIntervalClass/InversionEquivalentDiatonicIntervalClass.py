from abjad.core import Fraction
from abjad.tools.pitchtools._DiatonicInterval import _DiatonicInterval


class InversionEquivalentDiatonicIntervalClass(_DiatonicInterval):
   '''.. versionadded:: 1.1.2

   Inversion-equivalent diatonic interval class::

      abjad> pitchtools.InversionEquivalentDiatonicIntervalClass('major', 2)
      InversionEquivalentDiatonicIntervalClass(major second)

   ::

      abjad> pitchtools.InversionEquivalentDiatonicIntervalClass('major', -2)
      InversionEquivalentDiatonicIntervalClass(major second)

   ::

      abjad> pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 7)
      InversionEquivalentDiatonicIntervalClass(major second)

   ::

      abjad> pitchtools.InversionEquivalentDiatonicIntervalClass('minor', -7)
      InversionEquivalentDiatonicIntervalClass(major second)

   ::

      abjad> pitchtools.InversionEquivalentDiatonicIntervalClass('major', 9)
      InversionEquivalentDiatonicIntervalClass(major second)

   ::

      abjad> pitchtools.InversionEquivalentDiatonicIntervalClass('major', -9)
      InversionEquivalentDiatonicIntervalClass(major second)

   ::

      abjad> pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 14)
      InversionEquivalentDiatonicIntervalClass(major second)

   ::

      abjad> pitchtools.InversionEquivalentDiatonicIntervalClass('minor', -14)
      InversionEquivalentDiatonicIntervalClass(major second)
   '''

   def __init__(self, *args):
      if len(args) == 1 and isinstance(args[0], type(self)):
         self._init_by_self_reference(args[0])
      elif len(args) == 1 and isinstance(args[0], tuple):
         self.__init__(*args[0])
      elif len(args) == 2:
         self._init_by_quality_string_and_number(*args)
      else:
         raise ValueError('can not initialize diatonic interval class.')

   ## PRIVATE METHODS ##

   def _init_by_quality_string_and_number(self, quality_string, number):
      if number == 0:
         raise ValueError('diatonic intervals can not equal zero.')
      elif abs(number) == 1:
         number = 1
      elif abs(number) % 7 == 0:
         number = 7
      elif abs(number) % 7 == 1:
         number = 8
      else:
         number = abs(number) % 7
      if self._is_representative_number(number):
         quality_string = quality_string
         number = number
      else:
         quality_string = self._invert_quality_string(quality_string)
         number = 9 - number
         #self._quality_string = quality_string
         #self._number = number
      object.__setattr__(self, '_quality_string', quality_string)
      object.__setattr__(self, '_number', number)

   def _init_by_self_reference(self, reference):
      quality_string = reference.quality_string
      number = reference.number
      self.__init__(quality_string, number)

   def _invert_quality_string(self, quality_string):
      inversions = {'major': 'minor', 'minor': 'major', 'perfect': 'perfect',
         'augmented': 'diminished', 'diminished': 'augmented'}
      return inversions[quality_string]

   def _is_representative_number(self, arg):
      if isinstance(arg, (int, long, float, Fraction)):
         if 1 <= arg <= 4 or arg == 8:
            return True
      return False 

   ## PUBLIC ATTRIBUTES ##

   ## TODO: implement inversion-equivalent ChromaticIntervalClass
   #@property
   #def chromatic_interval_class(self):
   #   pass
