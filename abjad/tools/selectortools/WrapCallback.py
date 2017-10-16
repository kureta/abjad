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

    def __call__(self, argument, rotation=None):
        r'''Wraps `argument` in selection.

        Somewhat like the opposite of flattening.

        Ignores `rotation`.

        Returns tuple.
        '''
        import abjad
        if isinstance(argument, abjad.LogicalTie):
            return abjad.Selection([argument])
        else:
            return abjad.Selection(argument)
