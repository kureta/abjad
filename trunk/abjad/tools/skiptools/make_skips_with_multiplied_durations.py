# -*- encoding: utf-8 -*-
from abjad.tools import durationtools


def make_skips_with_multiplied_durations(written_duration, multiplied_durations):
    '''.. versionadded:: 2.0

    Make `written_duration` skips with `multiplied_durations`:

    ::

        >>> skiptools.make_skips_with_multiplied_durations(
        ...     Duration(1, 4), [(1, 2), (1, 3), (1, 4), (1, 5)])
        [Skip('s4 * 2'), Skip('s4 * 4/3'), Skip('s4 * 1'), Skip('s4 * 4/5')]

    Useful for making invisible layout voices.

    Return list of skips.
    '''
    from abjad.tools import skiptools

    # initialize skips and written duration
    skips = []
    written_duration = durationtools.Duration(written_duration)

    # make skips
    for multiplied_duration in multiplied_durations:
        multiplied_duration = durationtools.Duration(multiplied_duration)
        skip = skiptools.Skip(written_duration)
        multiplier = multiplied_duration / written_duration
        skip.duration_multiplier = multiplier
        skips.append(skip)

    # return skips
    return skips
