import collections
from abjad.tools.abctools import AbjadValueObject


class PartitionByRatioCallback(AbjadValueObject):
    r'''Partition-by-ratio callback.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        '_ratio',
        )

    ### INITIALIZER ###

    def __init__(self, ratio=None):
        import abjad
        ratio = ratio or abjad.Ratio((1,))
        ratio = abjad.Ratio(ratio)
        self._ratio = ratio

    ### SPECIAL METHODS ###

    def __call__(self, argument, rotation=None):
        r'''Calls callback on `argument`.

        Returns list of selections.
        '''
        import abjad
        counts = abjad.mathtools.partition_integer_by_ratio(
            len(argument),
            self.ratio,
            )
        parts = abjad.Sequence(argument).partition_by_counts(counts=counts)
        selections = [abjad.Selection(_) for _ in parts]
        return selections

    ### PUBLIC PROPERTIES ###

    @property
    def ratio(self):
        r'''Gets ratio.

        Returns ratio.
        '''
        return self._ratio
