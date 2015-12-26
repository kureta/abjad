# -*- encoding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class SplitByRoundedRatiosDivisionCallback(AbjadValueObject):
    r'''Split-by-rounded-ratios division callback.

    ..  container:: example

        **Example 1.** Makes divisions with ``2:1`` ratios:

        ::

            >>> maker = makertools.SplitByRoundedRatiosDivisionCallback(
            ...     ratios=[mathtools.Ratio([2, 1])],
            ...     )
            >>> lists = maker([(7, 4), (6, 4)])
            >>> for list_ in lists:
            ...     list_
            [Division(duration=Duration(5, 4)), Division(duration=Duration(1, 2))]
            [Division(duration=Duration(1, 1)), Division(duration=Duration(1, 2))]

    ..  container:: example

        **Example 2.** Makes divisions with alternating ``2:1`` and ``1:1:1``
        ratios:

        ::

            >>> maker = makertools.SplitByRoundedRatiosDivisionCallback(
            ...     ratios=[mathtools.Ratio([2, 1]), mathtools.Ratio([1, 1, 1])],
            ...     )
            >>> lists = maker([(7, 4), (6, 4), (5, 4), (4, 4)])
            >>> for list_ in lists:
            ...     list_
            [Division(duration=Duration(5, 4)), Division(duration=Duration(1, 2))]
            [Division(duration=Duration(1, 2)), Division(duration=Duration(1, 2)), Division(duration=Duration(1, 2))]
            [Division(duration=Duration(3, 4)), Division(duration=Duration(1, 2))]
            [Division(duration=Duration(1, 4)), Division(duration=Duration(1, 2)), Division(duration=Duration(1, 4))]

    Object model of a partially evaluated function that accepts a (possibly
    empty) list of divisions as input and returns a (possibly empty) nested
    list of divisions as output. Output structured one output list per input
    division.

    Follows the two-step configure-once / call-repeatedly pattern shown here.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_ratios',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        ratios=None,
        ):
        if ratios is not None:
            ratios = ratios or ()
            ratios = [mathtools.Ratio(_) for _ in ratios]
            ratios = tuple(ratios)
        self._ratios = ratios

    ### SPECIAL METHODS ###

    def __call__(self, divisions=None):
        r'''Calls rounded ratio division maker on `division`.

        ..  container:: example

            **Example 1.** Calls maker on nonempty input:

            ::

                >>> maker = makertools.SplitByRoundedRatiosDivisionCallback(
                ...     ratios=[mathtools.Ratio([1, 1])],
                ...     )
                >>> lists = maker([(7, 4), (6, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division(duration=Duration(1, 1)), Division(duration=Duration(3, 4))]
                [Division(duration=Duration(3, 4)), Division(duration=Duration(3, 4))]

            Returns list of division lists.

        ..  container:: example

            **Example 2.** Calls maker on empty input:

            ::

                >>> maker = makertools.SplitByRoundedRatiosDivisionCallback(
                ...     ratios=[mathtools.Ratio([1, 1])],
                ...     )
                >>> maker([])
                []

            Returns empty list.

        Returns possibly empty list of division lists.
        '''
        from experimental import makertools
        input_divisions = divisions or []
        if not input_divisions:
            return []
        output_division_lists = []
        ratios = self._get_ratios()
        for i, input_division in enumerate(input_divisions):
            input_division = mathtools.NonreducedFraction(input_division)
            ratio = ratios[i]
            numerators = mathtools.partition_integer_by_ratio(
                input_division.numerator,
                ratio,
                )
            output_division_list = [
                mathtools.NonreducedFraction(
                    numerator,
                    input_division.denominator,
                    )
                for numerator in numerators
                ]
            output_division_lists.append(output_division_list)
        output_division_lists = makertools.DivisionMaker._to_divisions(
            output_division_lists)
        return output_division_lists

    ### PRIVATE METHODS ###

    def _get_ratios(self):
        if self.ratios:
            ratios = self.ratios
        else:
            ratios = (mathtools.Ratio([1]),)
        ratios = datastructuretools.CyclicTuple(ratios)
        return ratios

    ### PUBLIC PROPERTIES ###

    @property
    def ratios(self):
        r'''Gets ratios of rounded ratio division maker.

        ..  container:: example

            **Example 1.** Gets trivial ratio of ``1``:

            ::

                >>> maker = makertools.SplitByRoundedRatiosDivisionCallback(
                ...     ratios=[mathtools.Ratio([1])],
                ...     )
                >>> lists = maker([(7, 4), (6, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division(duration=Duration(7, 4))]
                [Division(duration=Duration(3, 2))]

            This is default behavior when `ratios` is set to none.

        ..  container:: example

            **Example 2.** Gets ratios equal to ``1:1``:

            ::

                >>> maker = makertools.SplitByRoundedRatiosDivisionCallback(
                ...     ratios=[mathtools.Ratio([1, 1])],
                ...     )
                >>> lists = maker([(7, 4), (6, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division(duration=Duration(1, 1)), Division(duration=Duration(3, 4))]
                [Division(duration=Duration(3, 4)), Division(duration=Duration(3, 4))]

        ..  container:: example

            **Example 3.** Gets ratios equal to ``2:1``:

            ::

                >>> maker = makertools.SplitByRoundedRatiosDivisionCallback(
                ...     ratios=[mathtools.Ratio([2, 1])],
                ...     )
                >>> lists = maker([(7, 4), (6, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division(duration=Duration(5, 4)), Division(duration=Duration(1, 2))]
                [Division(duration=Duration(1, 1)), Division(duration=Duration(1, 2))]

        ..  container:: example

            **Example 4.** Gets ratios equal to ``1:1:1``:

            ::

                >>> maker = makertools.SplitByRoundedRatiosDivisionCallback(
                ...     ratios=[mathtools.Ratio([1, 1, 1])],
                ...     )
                >>> lists = maker([(7, 4), (6, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division(duration=Duration(1, 2)), Division(duration=Duration(3, 4)), Division(duration=Duration(1, 2))]
                [Division(duration=Duration(1, 2)), Division(duration=Duration(1, 2)), Division(duration=Duration(1, 2))]

        ..  container:: example

            **Example 5.** Gets ratios equal to ``2:1`` and ``1:1:1``
            alternately:

            ::

                >>> maker = makertools.SplitByRoundedRatiosDivisionCallback(
                ...     ratios=[mathtools.Ratio([2, 1]), mathtools.Ratio([1, 1, 1])],
                ...     )
                >>> lists = maker([(7, 4), (6, 4), (5, 4), (4, 4)])
                >>> for list_ in lists:
                ...     list_
                [Division(duration=Duration(5, 4)), Division(duration=Duration(1, 2))]
                [Division(duration=Duration(1, 2)), Division(duration=Duration(1, 2)), Division(duration=Duration(1, 2))]
                [Division(duration=Duration(3, 4)), Division(duration=Duration(1, 2))]
                [Division(duration=Duration(1, 4)), Division(duration=Duration(1, 2)), Division(duration=Duration(1, 4))]

        Set to ratios or none.
        '''
        return self._ratios