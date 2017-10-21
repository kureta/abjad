from abjad.tools.abctools import AbjadValueObject


class ByPatternCallback(AbjadValueObject):
    r'''By-pattern callback.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        '_pattern',
        )

    ### INITIALIZER ###

    def __init__(self, pattern=None):
        import abjad
        if pattern is not None:
            assert isinstance(pattern, abjad.Pattern)
        self._pattern = pattern

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        r'''Calls callback on `argument`.

        Returns selection.
        '''
        import abjad
        if not self.pattern:
            return argument
        result = []
        length = len(argument)
        for index, item in enumerate(argument):
            if self.pattern.matches_index(index, length):
                result.append(item)
        return abjad.Selection._manifest(result)

    ### PUBLIC PROPERTIES ###

    @property
    def pattern(self):
        r'''Gets pattern.

        Returns pattern.
        '''
        return self._pattern
