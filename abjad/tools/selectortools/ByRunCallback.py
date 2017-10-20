import collections
from abjad.tools.abctools import AbjadValueObject


class ByRunCallback(AbjadValueObject):
    r'''By-run callback.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        '_prototype',
        )

    ### INITIALIZER ###

    def __init__(self, prototype=None):
        prototype = prototype or ()
        if isinstance(prototype, collections.Sequence):
            prototype = tuple(prototype)
            assert all(isinstance(_, type) for _ in prototype)
        assert isinstance(prototype, (tuple, type))
        self._prototype = prototype

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        r'''Calls callback on `argument`.

        Returns list of runs.
        '''
        import abjad
        result = []
        prototype = self.prototype
        if not isinstance(prototype, tuple):
            prototype = (prototype,)
        for run in abjad.iterate(argument).by_run(prototype):
            assert isinstance(run, abjad.Selection)
            result.append(run)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def prototype(self):
        r'''Gets prototype.

        Return tuple of classes.
        '''
        return self._prototype
