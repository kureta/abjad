import collections
from abjad.tools import datastructuretools
from abjad.tools.abctools import AbjadValueObject


class FlattenSelectorCallback(AbjadValueObject):
    r'''Flatten selector callback.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        '_depth',
        )

    ### INITIALIZER ###

    def __init__(self, depth=-1):
        self._depth = depth

    ### SPECIAL METHODS ###

    def __call__(self, argument, rotation=None):
        r'''Calls callback on `argument`.

        Returns selection.
        '''
        import abjad
        argument = datastructuretools.Sequence(argument)
        argument = argument.flatten(depth=self.depth)
        return abjad.Selection(argument)

    ### PUBLIC PROPERTIES ###

    @property
    def depth(self):
        r'''Gets depth of callback.

        Returns integer.
        '''
        return self._depth
