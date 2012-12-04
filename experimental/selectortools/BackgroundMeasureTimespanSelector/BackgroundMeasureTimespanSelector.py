from abjad.tools import durationtools
from abjad.tools import measuretools
from experimental.selectortools.TimeRelationTimespanSelector import TimeRelationTimespanSelector
from experimental.selectortools.SliceTimespanSelector import SliceTimespanSelector


class BackgroundMeasureTimespanSelector(SliceTimespanSelector, TimeRelationTimespanSelector):
    r'''.. versionadded:: 1.0

    Select all measures in score::

        >>> from experimental import *

    ::

        >>> selectortools.BackgroundMeasureTimespanSelector()
        BackgroundMeasureTimespanSelector()

    Select measures from ``3`` forward::

        >>> selectortools.BackgroundMeasureTimespanSelector(start_identifier=3)
        BackgroundMeasureTimespanSelector(start_identifier=3)

    Select measures up to but not including ``6``::

        >>> selectortools.BackgroundMeasureTimespanSelector(stop_identifier=6)
        BackgroundMeasureTimespanSelector(stop_identifier=6)

    Select measures from ``3`` up to but not including ``6``::

        >>> selectortools.BackgroundMeasureTimespanSelector(start_identifier=3, stop_identifier=6)
        BackgroundMeasureTimespanSelector(start_identifier=3, stop_identifier=6)

    Select all measures starting during segment ``'red'``::

        >>> timespan = selectortools.SingleSegmentTimespanSelector(identifier='red')
        >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(timespan_1=timespan)

    ::

        >>> selector = selectortools.BackgroundMeasureTimespanSelector(time_relation=time_relation)

    ::

        >>> z(selector)
        selectortools.BackgroundMeasureTimespanSelector(
            time_relation=timerelationtools.TimespanTimespanTimeRelation(
                'timespan_1.start <= timespan_2.start < timespan_1.stop',
                timespan_1=selectortools.SingleSegmentTimespanSelector(
                    identifier='red'
                    )
                )
            )

    Select the last two measures during segment ``'red'``::

        >>> selector = selectortools.BackgroundMeasureTimespanSelector(time_relation=time_relation, start_identifier=-2)

    ::
    
        >>> z(selector)
        selectortools.BackgroundMeasureTimespanSelector(
            time_relation=timerelationtools.TimespanTimespanTimeRelation(
                'timespan_1.start <= timespan_2.start < timespan_1.stop',
                timespan_1=selectortools.SingleSegmentTimespanSelector(
                    identifier='red'
                    )
                ),
            start_identifier=-2
            )

    Select all the measures that start during the three contiguous segments starting with ``'red'``::

        >>> expr = helpertools.SegmentIdentifierExpression("'red' + 3")
        >>> selector = selectortools.SegmentTimespanSelector(start_identifier='red', stop_identifier=expr)
        >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(timespan_1=selector)

    ::
    
        >>> selector = selectortools.BackgroundMeasureTimespanSelector(time_relation=time_relation)

    ::

        >>> z(selector)
        selectortools.BackgroundMeasureTimespanSelector(
            time_relation=timerelationtools.TimespanTimespanTimeRelation(
                'timespan_1.start <= timespan_2.start < timespan_1.stop',
                timespan_1=selectortools.SegmentTimespanSelector(
                    start_identifier='red',
                    stop_identifier=helpertools.SegmentIdentifierExpression("'red' + 3")
                    )
                )
            )

    Select the last two measures that start during the three contiguous segments starting with ``'red'``::

        >>> selector = selectortools.BackgroundMeasureTimespanSelector(time_relation=time_relation, start_identifier=-2)

    ::

        >>> z(selector)
        selectortools.BackgroundMeasureTimespanSelector(
            time_relation=timerelationtools.TimespanTimespanTimeRelation(
                'timespan_1.start <= timespan_2.start < timespan_1.stop',
                timespan_1=selectortools.SegmentTimespanSelector(
                    start_identifier='red',
                    stop_identifier=helpertools.SegmentIdentifierExpression("'red' + 3")
                    )
                ),
            start_identifier=-2
            )

    Measure slice selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, time_relation=None, start_identifier=None, stop_identifier=None, voice_name=None):
        SliceTimespanSelector.__init__(
            self, start_identifier=start_identifier, stop_identifier=stop_identifier, voice_name=voice_name)
        TimeRelationTimespanSelector.__init__(self, time_relation=time_relation)
        self._klass = measuretools.Measure

    ### PUBLIC METHODS ###

    def get_offsets(self, score_specification, context_name):
        r'''Evaluate start and stop offsets when selector is applied
        to `score_specification`.

        Ignore `context_name`.

        Return pair.
        '''
        segment_specification = score_specification.get_start_segment_specification(self)
        segment_name = segment_specification.segment_name
        start, stop = self.identifiers
        start = start or 0
        stop = stop or None
        durations = [durationtools.Duration(x) for x in segment_specification.time_signatures]     
        durations_before = durations[:start]
        duration_before = sum(durations_before)
        start_offset = durationtools.Offset(duration_before)
        start_offset = score_specification.segment_offset_to_score_offset(segment_name, start_offset)
        durations_up_through = durations[:stop]
        duration_up_through = sum(durations_up_through)
        stop_offset = durationtools.Offset(duration_up_through)
        stop_offset = score_specification.segment_offset_to_score_offset(segment_name, stop_offset)
        return start_offset, stop_offset

    def get_selected_objects(self, score_specification, context_name):
        '''Get background measures selected when selector is applied
        to `score_specification`.
    
        Ignore `context_name`.

        Return list.
        '''
        raise NotImplementedError

    def set_segment_identifier(self, segment_identifier):
        '''Delegate to ``self.time_relation.set_segment_identifier()``.
        '''
        self.time_relation.set_segment_identifier(segment_identifier)
