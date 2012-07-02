from experimental.selectortools.BackgroundElementSliceSelector import BackgroundElementSliceSelector


class DivisionSliceSelector(BackgroundElementSliceSelector):
    r'''.. versionadded:: 1.0

    Select all ``'Voice 1'`` divisions in score::

        >>> from experimental import selectortools

    ::

        >>> selectortools.DivisionSliceSelector('Voice 1')
        DivisionSliceSelector('Voice 1')

    Select all ``'Voice 1'`` divisions starting during segment ``'red'``::

        >>> from experimental import timespantools

    ::

        >>> segment = selectortools.SegmentSelector(index='red')
        >>> timespan = segment.timespan
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=timespan)

    ::

        >>> divisions = selectortools.DivisionSliceSelector('Voice 1', inequality=inequality)

    ::

        >>> z(divisions)
        selectortools.DivisionSliceSelector(
            'Voice 1',
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.Timespan(
                    selector=selectortools.SegmentSelector(
                        index='red'
                        )
                    )
                )
            )

    Select the last two ``'Voice 1'`` divisions starting during segment ``'red'``::

        >>> divisions = selectortools.DivisionSliceSelector('Voice 1', inequality=inequality, start=-2)

    ::

        >>> z(divisions)
        selectortools.DivisionSliceSelector(
            'Voice 1',
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.Timespan(
                    selector=selectortools.SegmentSelector(
                        index='red'
                        )
                    )
                ),
            start=-2
            )

    Division slice selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, voice, inequality=None, start=None, stop=None):
        from experimental import specificationtools
        BackgroundElementSliceSelector.__init__(self, specificationtools.Division,
            inequality=inequality, start=start, stop=stop)
        voice = specificationtools.expr_to_component_name(voice)     
        self._voice = voice

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def voice(self):
        '''Name of division slice selector voice initialized by user.

        Return string.
        '''
        return self._voice
