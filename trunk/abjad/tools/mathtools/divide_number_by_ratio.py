# -*- encoding: utf-8 -*-
from __future__ import division
import fractions
import numbers


def divide_number_by_ratio(number, ratio):
    r'''Divide integer by `ratio`:

    ::

        >>> mathtools.divide_number_by_ratio(1, [1, 1, 3])
        [Fraction(1, 5), Fraction(1, 5), Fraction(3, 5)]

    Divide fraction by `ratio`:

    ::

        >>> mathtools.divide_number_by_ratio(Fraction(1), [1, 1, 3])
        [Fraction(1, 5), Fraction(1, 5), Fraction(3, 5)]

    Divide float by ratio:

    ::

        >>> mathtools.divide_number_by_ratio(1.0, [1, 1, 3]) # doctest: +SKIP
        [0.20000000000000001, 0.20000000000000001, 0.60000000000000009]

    Raise type error on nonnumeric `number`.

    Raise type error on noninteger in `ratio`.

    Return list of fractions or list of floats.
    '''
    from abjad.tools import mathtools

    # check input
    assert isinstance(number, numbers.Number)
    ratio = mathtools.Ratio(ratio)

    # find factors and multiply by factors
    factors = [fractions.Fraction(p, sum(ratio)) for p in ratio]
    result = [factor * number for factor in factors]

    # return result
    return result
