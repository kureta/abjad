from abjad.tools.abctools import AbjadValueObject


class WithLeafCallback(AbjadValueObject):
    r'''With-leaf callback.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        '_with_next_leaf',
        '_with_previous_leaf',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        with_next_leaf=False,
        with_previous_leaf=False,
        ):
        self._with_next_leaf = bool(with_next_leaf)
        self._with_previous_leaf = bool(with_previous_leaf)

    ### SPECIAL METHODS ###

    def __call__(self, argument, rotation=None):
        r'''Calls callback on `argument`.

        Returns selection.
        '''
        import abjad
        selection = []
        leaves = abjad.select(argument).by_leaf()
        if self.with_previous_leaf:
            previous_leaf = leaves[0]._get_leaf(-1)
            if previous_leaf is not None:
                selection.append(previous_leaf)
        selection.extend(leaves)
        if self.with_next_leaf:
            next_leaf = leaves[-1]._get_leaf(1)
            if next_leaf is not None:
                selection.append(next_leaf)
        return abjad.Selection(selection)

    ### PUBLIC PROPERTIES ###

    @property
    def with_next_leaf(self):
        r'''Gets next leaf inclusion.

        Returns true or false.
        '''
        return self._with_next_leaf

    @property
    def with_previous_leaf(self):
        r'''Gets previous leaf inclusion.

        Returns true or false.
        '''
        return self._with_previous_leaf
