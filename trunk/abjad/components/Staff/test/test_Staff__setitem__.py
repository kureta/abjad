from abjad import *
from py.test import raises


def test_Staff__setitem___01( ):
   t = Staff([Note(0, (1, 4)),
         Rest((1, 4)),
         Chord([2, 3, 4], (1, 4)),
         Skip((1, 4)),
         tuplettools.FixedDurationTuplet((5, 16), Note(0, (1, 16)) * 4)])
   assert len(t) == 5
   assert componenttools.is_well_formed_component(t)
   assert isinstance(t[0], Note)
   assert isinstance(t[1], Rest)
   assert isinstance(t[2], Chord)
   assert isinstance(t[3], Skip)
   assert isinstance(t[4], tuplettools.FixedDurationTuplet)
   t[1] = Chord([12, 13, 15], (1, 4))
   assert len(t) == 5
   assert componenttools.is_well_formed_component(t)
   assert isinstance(t[0], Note)
   assert isinstance(t[1], Chord)
   assert isinstance(t[2], Chord)
   assert isinstance(t[3], Skip)
   assert isinstance(t[4], tuplettools.FixedDurationTuplet)
   t[0] = Rest((1, 4))
   assert len(t) == 5
   assert componenttools.is_well_formed_component(t)
   assert isinstance(t[0], Rest)
   assert isinstance(t[1], Chord)
   assert isinstance(t[2], Chord)
   assert isinstance(t[3], Skip)
   assert isinstance(t[4], tuplettools.FixedDurationTuplet)
   t[-2] = tuplettools.FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3)
   assert len(t) == 5
   assert componenttools.is_well_formed_component(t)
   assert isinstance(t[0], Rest)
   assert isinstance(t[1], Chord)
   assert isinstance(t[2], Chord)
   assert isinstance(t[3], tuplettools.FixedDurationTuplet)
   assert isinstance(t[4], tuplettools.FixedDurationTuplet)
   t[-1] = Note(13, (1, 4))
   assert len(t) == 5
   assert componenttools.is_well_formed_component(t)
   assert isinstance(t[0], Rest)
   assert isinstance(t[1], Chord)
   assert isinstance(t[2], Chord)
   assert isinstance(t[3], tuplettools.FixedDurationTuplet)
   assert isinstance(t[4], Note)
   t[-3] = Skip((1, 4))
   assert len(t) == 5
   assert componenttools.is_well_formed_component(t)
   assert isinstance(t[0], Rest)
   assert isinstance(t[1], Chord)
   assert isinstance(t[2], Skip)
   assert isinstance(t[3], tuplettools.FixedDurationTuplet)
   assert isinstance(t[4], Note)


def test_Staff__setitem___02( ):
   '''Reassign the *entire* contents of t.'''
   t = Staff(Note(0, (1, 4)) * 4)
   assert t.duration.contents == Fraction(4, 4)
   t[:] = Note(0, (1, 8)) * 4
   assert t.duration.contents == Fraction(4, 8)


def test_Staff__setitem___03( ):
   '''Item-assign an empty container to t.'''
   t = Staff(Note(0, (1, 4)) * 4)
   t[0] = Voice([ ])


def test_Staff__setitem___04( ):
   '''Slice-assign empty containers to t.'''
   t = Staff(Note(0, (1, 4)) * 4)
   t[0:2] = [Voice([ ]), Voice([ ])]


def test_Staff__setitem___05( ):
   '''Bark when user assigns a slice to an item.'''
   t = Staff(Note(0, (1, 4)) * 4)
   assert raises(AssertionError, 't[0] = [Note(2, (1, 4)), Note(2, (1, 4))]')


def test_Staff__setitem___06( ):
   '''Bark when user assigns an item to a slice.'''
   t = Staff(Note(0, (1, 4)) * 4)
   assert raises(TypeError, 't[0:2] = Note(2, (1, 4))')


def test_Staff__setitem___07( ):
   '''Slice-assign notes.'''
   t = Staff(Note(0, (1, 8)) * 8)
   t[0:4] = Note(2, (1, 8)) * 4
   assert len(t) == 8
   for x in t[0:4]:
      assert x.pitch.number == 2
   for x in t[4:8]:
      assert x.pitch.number == 0
   assert componenttools.is_well_formed_component(t)


def test_Staff__setitem___08( ):
   '''Slice-assign chords.'''
   t = Staff(Note(0, (1, 8)) * 8)
   t[0:4] = Chord([2, 3, 4], (1, 4)) * 4
   assert len(t) == 8
   for x in t[0:4]:
      assert x.duration.written == Fraction(1, 4)
   for x in t[4:8]:
      assert x.duration.written == Fraction(1, 8)
   assert componenttools.is_well_formed_component(t)


def test_Staff__setitem___09( ):
   '''Slice-assign tuplets.'''
   t = Staff(Note(0, (1, 8)) * 8)
   t[0:4] = tuplettools.FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3) * 2
   assert len(t) == 6
   for i, x in enumerate(t):
      if i in [0, 1]:
         assert isinstance(x, tuplettools.FixedDurationTuplet)
      else:
         assert isinstance(x, Note)
   assert componenttools.is_well_formed_component(t)


def test_Staff__setitem___10( ):
   '''Slice-assign measures.'''
   t = Staff(Note(0, (1, 8)) * 8)
   t[0:4] = Measure((2, 8), Note(0, (1, 8)) * 2) * 2
   assert len(t) == 6
   for i, x in enumerate(t):
      if i in [0, 1]:
         assert isinstance(x, Measure)
      else:
         assert isinstance(x, Note)
   assert componenttools.is_well_formed_component(t)
