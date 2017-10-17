from abjad.tools.abctools import AbjadValueObject


class FlattenCallback(AbjadValueObject):
    r'''Flatten callback.
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
        argument = abjad.Sequence(argument)
        argument = argument.flatten(depth=self.depth)
        return abjad.Selection(argument)

    ### PUBLIC PROPERTIES ###

    @property
    def depth(self):
        r'''Gets depth.

        Returns integer.
        '''
        return self._depth
