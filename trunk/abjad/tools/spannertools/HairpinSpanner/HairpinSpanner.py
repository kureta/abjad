from abjad.tools.spannertools.HairpinSpanner._HairpinSpannerFormatInterface import _HairpinSpannerFormatInterface
from abjad.tools.spannertools.Spanner import Spanner


class HairpinSpanner(Spanner):

   def __init__(self, music, descriptor, avoid_rests = False):
      Spanner.__init__(self, music)
      self._format = _HairpinSpannerFormatInterface(self)
      self.avoid_rests = avoid_rests
      start, shape, stop = self._parse_descriptor(descriptor)
      self.shape = shape
      self.start = start
      self.stop = stop
   
   ## PRIVATE METHODS ##

   def _parse_descriptor(self, descriptor):
      '''Example descriptors:
         '<'
         'p <'
         'p < f'
      '''
      assert isinstance(descriptor, str)
      parts = descriptor.split( )
      num_parts = len(parts)
      start, shape, stop = None, None, None
      if parts[0] in ('<', '>'):
         assert 1 <= num_parts <= 2
         if num_parts == 1:
            shape = parts[0]
         else:
            shape = parts[0]
            stop = parts[1]
      else:
         assert 2 <= num_parts <= 3
         if num_parts == 2:
            start = parts[0]
            shape = parts[1]
         else:
            start = parts[0]
            shape = parts[1]
            stop = parts[2]
      assert shape in ('<', '>')
      return start, shape, stop

   ## PUBLIC ATTRIBUTES ##

   @apply
   def avoid_rests( ):
      def fget(self):
         return self._avoid_rests
      def fset(self, arg):
         self._avoid_rests = arg
      return property(**locals( ))

   @apply
   def shape( ):
      def fget(self):
         return self._shape
      def fset(self, arg):
         assert arg in ('<', '>')
         self._shape = arg
      return property(**locals( ))

   @apply
   def start( ):
      def fget(self):
         return self._start
      def fset(self, arg):
         self._start = arg
      return property(**locals( ))

   @apply
   def stop( ):
      def fget(self):
         return self._stop
      def fset(self, arg):
         self._stop = arg
      return property(**locals( ))
