import collections
import itertools
from abjad.tools.abctools import AbjadValueObject


class ByLogicalMeasureCallback(AbjadValueObject):
    r'''By-logical-measure callback.

    ..  container:: example

        Score for examples 1 - 3:

        ::

            >>> staff = abjad.Staff("c'8 d' e' f' g' a' b' c''")
            >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
            >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
            >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])
            >>> show(staff) # doctest: +SKIP

    ..  container:: example

        Selects the leaves of every logical measure:

        ::

            >>> selector = abjad.select()
            >>> selector = selector.by_leaf()
            >>> selector = selector.by_logical_measure()
            >>> for selection in selector(staff):
            ...     selection
            ...
            Selection([Note("c'8"), Note("d'8")])
            Selection([Note("e'8"), Note("f'8")])
            Selection([Note("g'8"), Note("a'8"), Note("b'8")])
            Selection([Note("c''8")])

    ..  container:: example

        Selects the first leaf of every logical measure:

        ::

            >>> selector = abjad.select()
            >>> selector = selector.by_leaf()
            >>> selector = selector.by_logical_measure()
            >>> selector = selector.map(abjad.select().get_item(0))
            >>> selector(staff)
            [Note("c'8"), Note("e'8"), Note("g'8"), Note("c''8")]

    ..  container:: example

        Selects the last leaf of every logical measure:

        ::

            >>> selector = abjad.select()
            >>> selector = selector.by_leaf()
            >>> selector = selector.by_logical_measure()
            >>> selector = selector.map(abjad.select().get_item(-1))
            >>> selector(staff)
            [Note("d'8"), Note("f'8"), Note("b'8"), Note("c''8")]

    ..  container:: example

        Works with implicit time signatures:

        ::

            >>> staff = abjad.Staff("c'4 d' e' f' g' a' b' c''")
            >>> score = abjad.Score([staff])
            >>> scheme = abjad.SchemeMoment((1, 16))
            >>> abjad.setting(score).proportional_notation_duration = scheme
            >>> show(score) # doctest: +SKIP

        ::

            >>> selector = abjad.select()
            >>> selector = selector.by_leaf()
            >>> selector = selector.by_logical_measure()
            >>> for selection in selector(score):
            ...     selection
            ...
            Selection([Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4")])
            Selection([Note("g'4"), Note("a'4"), Note("b'4"), Note("c''4")])

    Groups components by logical measure of component start offset.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __call__(self, argument, rotation=None):
        r'''Calls callback on `argument`.

        Returns list of selections.
        '''
        selections = []
        logical_measures = self._group(argument)
        selections.extend(logical_measures)
        return selections

    ### PRIVATE METHODS ###

    def _get_first_component(self, argument):
        import abjad
        if isinstance(argument, abjad.Component):
            return argument
        else:
            component = argument[0]
            assert isinstance(component, abjad.Component)
            return component

    def _get_logical_measure_number(self, argument):
        first_component = self._get_first_component(argument)
        assert first_component._logical_measure_number is not None
        return first_component._logical_measure_number

    def _group(self, argument):
        import abjad
        selections = []
        first_component = self._get_first_component(argument)
        first_component._update_logical_measure_numbers()
        pairs = itertools.groupby(
            argument,
            lambda _: self._get_logical_measure_number(_),
            )
        for value, group in pairs:
            selection = abjad.Selection(list(group))
            selections.append(selection)
        return tuple(selections)
