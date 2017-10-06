from abjad.tools.abctools import AbjadValueObject


class ItemSelectorCallback(AbjadValueObject):
    r'''Item selector callback.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        '_item',
        )

    ### INITIALIZER ###

    def __init__(self, item=0):
        assert isinstance(item, int)
        self._item = item

    ### SPECIAL METHODS ###

    def __call__(self, argument, rotation=None):
        r'''Gets item from `argument`.

        Returns item.
        '''
        import abjad
        result = self._get_item(argument)
        return result

    ### PRIVATE METHODS ###

    def _get_item(self, argument):
        result = argument.__getitem__(self.item)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def item(self):
        r'''Gets item selector callback item.

        Returns integer.
        '''
        return self._item
