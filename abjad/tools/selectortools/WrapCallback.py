from abjad.tools.abctools import AbjadValueObject


class WrapCallback(AbjadValueObject):
    r'''Wrap callback.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls callback on `argument`.

        Wraps `argument` in list.

        Returns list.
        '''
        return [argument]
