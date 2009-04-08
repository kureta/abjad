from abjad.tools import clone
from abjad.tools import mathtools
from abjad.helpers.leaf_scale_binary import leaf_scale_binary
from abjad.leaf.leaf import _Leaf
from abjad.rational.rational import Rational


def leaf_split_binary(leaf, split_dur):
   assert isinstance(leaf, _Leaf)
   assert isinstance(split_dur, Rational)
   unprolated_split_dur = split_dur / leaf.duration.prolation
   denominator = unprolated_split_dur._d
   assert mathtools.is_power_of_two(denominator)
   if unprolated_split_dur == 0 or \
      leaf.duration.written <= unprolated_split_dur:
      return [leaf]
   new_leaf = clone.unspan([leaf])[0]
   leaf.splice([new_leaf])
   new_leaf.grace.after = None
   leaf.grace.before = None
   leaf.articulations = None
   leaf.dynamics.mark = None
   l1 = leaf_scale_binary(new_leaf, unprolated_split_dur)
   l2 = leaf_scale_binary(leaf, leaf.duration.written-unprolated_split_dur)
   result = [l1, l2] 
   return result
