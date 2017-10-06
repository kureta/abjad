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
        r'''Call callback on `argument`.

        Returns item.
        '''
        return argument.__getitem__(self.item)

    ### PUBLIC PROPERTIES ###

    @property
    def item(self):
        r'''Gets item.

        Returns integer.
        '''
        return self._item
