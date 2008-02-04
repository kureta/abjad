from formatter import _ChordFormatter
from initializer import _ChordInitializer
from .. leaf.leaf import _Leaf
from .. notehead.notehead import _NoteHead
from .. pitch.pitch import Pitch

class Chord(_Leaf):

   def __init__(self, *args):
      self.initializer = _ChordInitializer(self, _Leaf, *args)

   ### REPR ### 

   def __repr__(self):
      return 'Chord(%s, %s)' % (self._summary, self.duration._product)

   def __str__(self):
      return '<%s>%s' % (self._summary, self.duration._product)

   ### OVERRIDES ###

   def __len__(self):
      return len(self._noteheads)

   def __contains__(self, arg):
      if isinstance(arg, (int, float, long)):
         return Pitch(arg) in self.pitches
      elif isinstance(arg, Pitch):
         return arg in self.pitches
      elif isinstance(arg, _NoteHead):
         return arg in self.noteheads
      else:
         return False

   def __getitem__(self, i):
      return self._noteheads[i]

   def __setitem__(self, i, arg):
      if isinstance(arg, (int, long, float)):
         self._noteheads[i] = _NoteHead(self, pitch = arg)
      elif isinstance(arg, Pitch):
         self._noteheads[i] = _NoteHead(self, pitch = arg)
      elif isinstance(arg, _NoteHead):
         self._noteheads[i] = arg

   def __delitem__(self, i):
      del(self._noteheads[i])

   ### HANDLERS ###

   def insert(self, i, arg):
      if isinstance(arg, (int, float, long)):
         self._noteheads.insert(_NoteHead(self, pitch = arg))
      elif isinstance(arg, Pitch):
         self._noteheads.insert(_NoteHead(self, pitch = arg))
      elif isinstance(arg, _NoteHead):
         arg._client = self
         self._noteheads.insert(arg)
      else:
         print 'Can not insert %s into Chord at %s.' % (arg, i)

   def append(self, arg):
      if isinstance(arg, (int, float, long)):
         self._noteheads.append(_NoteHead(self, pitch = arg))
      elif isinstance(arg, Pitch):
         self._noteheads.append(_NoteHead(self, pitch = arg))
      elif isinstance(arg, _NoteHead):
         arg._client = self
         self._noteheads.append(arg)
      else:
         print 'Can not append %s to Chord.' % arg

   def extend(self, arglist):
      assert isinstance(arglist, list)
      for arg in arglist:
         self.append(arg)

   def pop(self, i = -1):
      return self._noteheads.pop(i)

   def remove(self, notehead):
      self._noteheads.remove(notehead)
   
   ### MANAGED ATTRIBUTES ###

   @apply
   def pitches( ):
      def fget(self):
         result = [ ]
         for notehead in self._noteheads:
            if notehead.pitch:
               result.append(notehead.pitch)   
         return result
      def fset(self, arglist):
         self.noteheads = arglist
      return property(**locals( ))

   @apply
   def noteheads( ):
      def fget(self):
         result = [ ]
         for notehead in self._noteheads:
            result.append(notehead)
         return result
      def fset(self, arglist):
         assert isinstance(arglist, (list, tuple))
         arglist = sorted(arglist)
         self._noteheads = [ ]
         for arg in arglist:
            if isinstance(arg, (int, float, long)):
               self._noteheads.append(_NoteHead(self, pitch = arg))
            elif isinstance(arg, Pitch):
               self._noteheads.append(_NoteHead(self, pitch = arg))
            elif isinstance(arg, _NoteHead):
               arg._client = self
               self._noteheads.append(arg)
            else:
               print 'Can not set Chord.noteheads = [..., %s, ...].' % arg
               raise ValueError
      return property(**locals( ))

   ### FORMATTING ###

   @property
   def _summary(self):
      return ' '.join([str(x) for x in self._noteheads])

   ### UTILITY ###

   def _sort(self):
      self._noteheads.sort()
