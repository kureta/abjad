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
        '_with_grace_notes',
        )

    ### INITIALIZER ###

    def __init__(self, pitched=True, trivial=True, with_grace_notes=False):
        self._pitched = bool(pitched)
        self._trivial = bool(trivial)
        self._with_grace_notes = bool(with_grace_notes)

    ### SPECIAL METHODS ###

    def __call__(self, argument, rotation=None):
        r'''Calls callback on `argument`.

        Returns list of logical ties.
        '''
        import abjad
        result = []
        for logical_tie in abjad.iterate(argument).by_logical_tie(
            with_grace_notes=self.with_grace_notes,
            ):
            if self.pitched and not logical_tie.is_pitched:
                continue
            if not self.trivial and logical_tie.is_trivial:
                continue
            result.append(logical_tie)
        return result

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

    @property
    def with_grace_notes(self):
        r'''Is true if callback iterates logical ties with grace notes.

        Returns true or false.
        '''
        return self._with_grace_notes
