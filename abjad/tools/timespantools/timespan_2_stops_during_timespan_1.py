def timespan_2_stops_during_timespan_1(
    timespan_1=None,
    timespan_2=None,
    hold=False,
    ):
    r'''Makes time relation indicating that `timespan_2` stops
    during `timespan_1`.

    ..  container:: example

        ::

            >>> relation = abjad.timespantools.timespan_2_stops_during_timespan_1()
            >>> abjad.f(relation)
            abjad.timespantools.TimespanTimespanTimeRelation(
                inequality=abjad.timespantools.CompoundInequality(
                    [
                        abjad.TimespanInequality('timespan_1.start_offset < timespan_2.stop_offset'),
                        abjad.TimespanInequality('timespan_2.stop_offset <= timespan_1.stop_offset'),
                        ],
                    logical_operator='and',
                    ),
                )

    Returns time relation or boolean.
    '''
    from abjad.tools import timespantools

    inequality = timespantools.CompoundInequality([
        'timespan_1.start_offset < timespan_2.stop_offset',
        'timespan_2.stop_offset <= timespan_1.stop_offset'
        ])

    time_relation = timespantools.TimespanTimespanTimeRelation(
        inequality,
        timespan_1=timespan_1,
        timespan_2=timespan_2,
        )

    if time_relation.is_fully_loaded and not hold:
        return time_relation()
    else:
        return time_relation
