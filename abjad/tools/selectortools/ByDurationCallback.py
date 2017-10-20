import collections
from abjad.tools import durationtools
from abjad.tools.abctools import AbjadValueObject


class ByDurationCallback(AbjadValueObject):
    r'''By-duration callback.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        '_duration',
        '_preprolated',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        duration=durationtools.Duration(1, 4),
        preprolated=None,
        ):
        import abjad
        prototype = (abjad.Duration, abjad.DurationInequality)
        if not isinstance(duration, prototype):
            duration = abjad.Duration(duration)
        self._duration = duration
        if preprolated is not None:
            preprolated = bool(preprolated)
        self._preprolated = preprolated

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        r'''Calls callback on `argument`.

        Returns tuple in which each item is a selection or component.
        '''
        import abjad
        assert isinstance(argument, collections.Iterable), repr(argument)
        inequality = self.duration
        if not isinstance(inequality, abjad.DurationInequality):
            inequality = abjad.DurationInequality(
                duration=inequality,
                operator_string='==',
                )
        result = []
        for item in argument:
            if not self.preprolated:
                if isinstance(item, abjad.Component):
                    duration = item._get_duration()
                else:
                    duration = item.get_duration()
            else:
                if isinstance(item, abjad.Component):
                    item._update_now(offsets=True)
                    duration = item._get_preprolated_duration()
                else:
                    durations = []
                    for x in item:
                        if isinstance(x, abjad.Component):
                            x._update_now(offsets=True)
                        duration = x._get_preprolated_duration()
                        durations.append(x._get_preprolated_duration())
                    duration = sum(durations)
            if inequality(duration):
                result.append(item)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        r'''Gets duration selector callback duration.

        Returns duration or duration inequality.
        '''
        return self._duration

    @property
    def preprolated(self):
        r'''Is true if duration selector callback should be tested against the
        preprolated duration of components in selections. Otherwise false.

        Returns boolean or none.
        '''
        return self._preprolated
