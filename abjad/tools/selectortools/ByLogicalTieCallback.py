import collections
from abjad.tools.abctools import AbjadValueObject


class ByLogicalTieCallback(AbjadValueObject):
    r'''By-logical-tie callback.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        '_pitched',
        '_trivial',
        )

    ### INITIALIZER ###

    def __init__(self, pitched=True, trivial=True):
        self._pitched = bool(pitched)
        self._trivial = bool(trivial)

    ### SPECIAL METHODS ###

    def __call__(self, argument, rotation=None):
        r'''Calls callback on `argument`.

        Returns selection of logical ties.
        '''
        import abjad
        result = []
        for logical_tie in abjad.iterate(argument).by_logical_tie():
            if self.pitched and not logical_tie.is_pitched:
                continue
            if not self.trivial and logical_tie.is_trivial:
                continue
            result.append(logical_tie)
        return abjad.Selection(result)

    ### PUBLIC PROPERTIES ###

    @property
    def pitched(self):
        r'''Is true if callback iterates pitched logical ties.

        Returns true or false.
        '''
        return self._pitched

    @property
    def trivial(self):
        r'''Is true if callback iterates trivial logical ties.

        Returns true or false.
        '''
        return self._trivial
