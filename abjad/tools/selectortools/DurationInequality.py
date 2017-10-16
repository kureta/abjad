from abjad.tools import mathtools
from abjad.tools.selectortools.Inequality import Inequality


class DurationInequality(Inequality):
    r'''Duration inequality.

    ..  container:: example

        ::

            >>> inequality = abjad.DurationInequality('<', (3, 4))
            >>> f(inequality)
            abjad.DurationInequality(
                operator_string='<',
                duration=abjad.Duration(3, 4),
                )

        ::

            >>> inequality(abjad.Duration(1, 2))
            True

        ::

            >>> inequality(abjad.Note("c'4"))
            True

        ::

            >>> inequality(abjad.Container("c'1 d'1"))
            False

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Inequalities'

    __slots__ = (
        '_duration',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        operator_string='<',
        duration=mathtools.Infinity(),
        ):
        import abjad
        Inequality.__init__(self, operator_string=operator_string)
        infinities = (
            abjad.mathtools.Infinity(),
            abjad.mathtools.NegativeInfinity(),
            )
        if duration not in infinities:
            duration = abjad.Duration(duration)
            assert 0 <= duration
        self._duration = duration

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        r'''Calls inequality on `argument`.

        Returns true or false.
        '''
        import abjad
        if isinstance(argument, abjad.Component):
            duration = abjad.inspect(argument).get_duration()
        elif isinstance(argument, abjad.Selection):
            duration = argument.get_duration()
        else:
            duration = abjad.Duration(argument)
        result = self._operator_function(duration, self._duration)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        r'''Gets duration.

        Returns duration.
        '''
        return self._duration
