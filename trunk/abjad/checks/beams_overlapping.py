from abjad.checks.check import _Check
from abjad.helpers.hasname import hasname
from abjad.helpers.instances import instances


class BeamsOverlapping(_Check):
   '''
   Beams must not overlap.
   '''

   def _run(self, expr):
      violators = [ ]
      for leaf in instances(expr, '_Leaf'):
         #beams = leaf.spanners.get(classname = 'Beam')
         beams = [p for p in leaf.spanners.spanners
            if hasname(p, 'Beam')]
         if len(beams) > 1:
            for beam in beams:
               if beam not in violators:
                  violators.append(beam)
      #total = len(expr.spanners.get(classname = 'Beam'))
      total = len([p for p in expr.spanners.contained if hasname(p, 'Beam')])
      return violators, total
