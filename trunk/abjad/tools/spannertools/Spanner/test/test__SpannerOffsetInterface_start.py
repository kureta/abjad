from abjad import *


def test__SpannerOffsetInterface_start_01( ):
   '''Return start time of spanner in score.'''

   t = Voice(macros.scale(4))
   beam = spannertools.BeamSpanner(t[1:3])
   glissando = spannertools.GlissandoSpanner([t])

   r'''
   \new Voice {
           c'8 \glissando
           d'8 [ \glissando
           e'8 ] \glissando
           f'8
   }
   '''

   assert beam.offset.start == Fraction(1, 8)
   assert glissando.offset.start == Fraction(0)
