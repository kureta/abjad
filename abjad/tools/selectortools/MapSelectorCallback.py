from abjad.tools.abctools import AbjadValueObject


class MapSelectorCallback(AbjadValueObject):
    r'''Map selector callback.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        '_callback',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        callback=None,
        ):
        self._callback = callback

    ### SPECIAL METHODS ###

    def __call__(self, argument, rotation=None):
        r'''Calls callback on `argument`.

        Returns list.
        '''
        result = []
        for item in argument:
            item_ = self.callback(item)
            result.append(item_)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def callback(self):
        r'''Gets callback.

        Returns callback or none.
        '''
        return self._callback
