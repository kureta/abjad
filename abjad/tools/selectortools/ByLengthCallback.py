import collections
from abjad.tools.abctools import AbjadValueObject


class ByLengthCallback(AbjadValueObject):
    r'''By-length callback.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        '_length',
        )

    ### INITIALIZER ###

    def __init__(self, length=1):
        import abjad
        prototype = (int, abjad.LengthInequality)
        assert isinstance(length, prototype)
        self._length = length

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        r'''Calls callback on `argument`.

        Returns list in which each item is a selection or component.
        '''
        import abjad
        inequality = self.length
        if not isinstance(inequality, abjad.LengthInequality):
            inequality = abjad.LengthInequality(
                length=inequality,
                operator_string='==',
                )
        result = []
        for item in argument:
            if inequality(item):
                result.append(item)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def length(self):
        r'''Gets length.

        Returns integer or length inequality.
        '''
        return self._length
