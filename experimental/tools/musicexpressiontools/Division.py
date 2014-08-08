# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import timespantools
from abjad.tools.mathtools.BoundedObject import BoundedObject
from abjad.tools.mathtools.NonreducedFraction import NonreducedFraction


class Division(NonreducedFraction, BoundedObject):
    r'''Division.

    A division is a bounded nonreduced fraction that is optionally
    offset-positioned.

    ..  container:: example::
    
        Example 1. Initializes from string:

        ::

            >>> musicexpressiontools.Division('[5, 8)')
            Division('[5, 8)')

    ..  container:: example::

        Example 2. Initializes from other division:

        ::

            >>> division = musicexpressiontools.Division(
            ...     '[5, 8)', 
            ...     start_offset=Offset(1, 8),
            ...     )
            >>> musicexpressiontools.Division(division)
            Division('[5, 8)', start_offset=Offset(1, 8))

    Divisions model any block of time that is divisible into parts: beats,
    complete measures or arbitrary spans of time.
    '''

    ### CLASS VARIABLES ###

    # slots definition does nothing here because multiple inheritance
    # breaks with multiple slots base classes
    __slots__ = (
        '_is_left_closed',
        '_is_left_open',
        '_is_right_closed',
        '_is_right_open',
        '_start_offset',
        )

    ### CONSTRUCTOR ###

    def __new__(
        cls,
        arg,
        start_offset=None,
        ):
        if isinstance(arg, str):
            triple = Division.parse_interval_range_string(arg)
            pair, is_left_open, is_right_open = triple
        elif isinstance(arg, cls):
            pair = arg
        elif hasattr(arg, 'duration'):
            pair = (arg.duration.numerator, arg.duration.denominator)
        else:
            pair = arg
        self = NonreducedFraction.__new__(cls, pair)

        self._is_left_closed = True
        self._is_left_open = False
        self._is_right_open = True
        self._is_right_closed = False

        if start_offset is None:
            start_offset = getattr(pair, 'start_offset', None)
        self._start_offset = start_offset

        # MIGRATION:
        assert self.is_left_closed, repr(self)
        assert not self.is_left_open, repr(self)
        assert self.is_right_open, repr(self)
        assert not self.is_right_closed, repr(self)

        return self

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        return type(self)(
            self.pair,
            start_offset=self.start_offset,
            )

    # TODO: remove?
    __deepcopy__ = __copy__

    def __repr__(self):
        if self.start_offset is not None:
            return '{}({!r}, start_offset={!r})'.format(
                type(self).__name__, 
                str(self),
                self.start_offset,
                )
        else:
            return '{}({!r})'.format(type(self).__name__, str(self))

    def __str__(self):
        return '[{}, {})'.format(
            self.numerator, 
            self.denominator, 
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        keyword_argument_names = []
        if self.start_offset is not None:
            keyword_argument_names.append('start_offset')
        positional_argument_values = (
            str(self),
            )
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            positional_argument_values=positional_argument_values,
            )

    ### PRIVATE METHODS ###

    # TODO: maybe keep only _get_timespan?
    def _get_timespan(self):
        return timespantools.Timespan(self.start_offset, self.stop_offset)

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        r'''Division duration.

        Returns duration.
        '''
        return durationtools.Duration(self.numerator, self.denominator)

    # TODO: remove in favor of self.timespan
    @property
    def start_offset(self):
        r'''Division start offset specified at initialization.

        .. note:: remove in favor of ``self.timespan``.

        Returns offset or none.
        '''
        return self._start_offset

    # TODO: remove in favor of self.timespan
    @property
    def stop_offset(self):
        r'''Division stop offset defined equal to start offset plus duration
        when start offset is not none.

        .. note:: remove in favor of ``self.timespan``.

        Defined equal to none when start offset is none.

        Returns offset or none.
        '''
        if self.start_offset is not None:
            return self.start_offset + self.duration

    # TODO: remove in favor of self.get_timespan()
    @property
    def timespan(self):
        r'''Division timespan.

        Returns timespan.

        .. note:: Deprecated. Use get_timespan() instead.
        '''
        return timespantools.Timespan(self.start_offset, self.stop_offset)

    ### PUBLIC METHODS ###

    def get_timespan(self):
        '''Get timespan of division.

        Returns timespan.
        '''
        return timespantools.Timespan(self.start_offset, self.stop_offset)

    @staticmethod
    def parse_interval_range_string(interval_range_string):
        r'''Parses `interval_range_string` into interval pair, boolean start
        and boolean stop.

        ::

            >>> musicexpressiontools.Division.parse_interval_range_string(
            ...     '[5, 8)')
            ((5, 8), False, True)

        Parses square brackets as closed interval bounds.

        Parses parentheses as open interval bounds.

        Returns triple.
        '''
        assert isinstance(interval_range_string, str)
        assert interval_range_string.startswith('[')
        assert interval_range_string.endswith(')')
        numbers = interval_range_string[1:-1]
        comma_index = numbers.index(',')
        start = numbers[:comma_index]
        start = int(start)
        stop = numbers[comma_index+1:]
        stop = int(stop)
        pair = (start, stop)
        return pair, False, True