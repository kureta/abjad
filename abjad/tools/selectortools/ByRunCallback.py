import collections
from abjad.tools.abctools import AbjadValueObject
from abjad.tools import selectiontools
from abjad.tools.topleveltools import iterate


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

    def __call__(self, argument, rotation=None):
        r'''Iterates `argument`.

        Returns list of runs.
        '''
        import abjad
        result = []
        prototype = self.prototype
        if not isinstance(prototype, tuple):
            prototype = (prototype,)
        for run in iterate(argument).by_run(prototype):
            assert isinstance(run, abjad.Selection)
            #run = selectiontools.Selection(run)
            result.append(run)
        #return tuple(result)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def prototype(self):
        r'''Gets run selector callback prototype.

        Return tuple of classes.
        '''
        return self._prototype
