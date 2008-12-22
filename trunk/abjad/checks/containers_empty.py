from abjad.checks.check import _Check
#from abjad.helpers.instances import instances
from abjad.helpers.iterate import iterate


class ContainersEmpty(_Check):

   def _run(self, expr):
      violators = [ ]
      #containers = instances(expr, 'Container')
      bad, total = 0, 0
      #for t in containers:
      for t in iterate(expr, 'Container'):
         if len(t) == 0:
            violators.append(t)
            bad += 1
         total += 1
      return violators, total
