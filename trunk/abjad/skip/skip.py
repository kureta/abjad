from abjad.leaf.leaf import _Leaf
from abjad.skip.initializer import _SkipInitializer


class Skip(_Leaf):

   def __init__(self, *args):
      self._initializer = _SkipInitializer(self, _Leaf, *args)
      
   ## OVERLOADS ##

   def __repr__(self):
      return 'Skip(%s)' % self.duration._product

   def __str__(self):
      return 's%s' % self.duration._product

   ## PRIVATE ATTRIBUTES ##
  
   @property
   def _body(self):
      return 's%s' % self.duration._product

   ## PUBLIC ATTRIBUTES ##

   @property
   def pairs(self):
      return ( )

   @property
   def pitches(self):
      return ( )
