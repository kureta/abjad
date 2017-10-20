from abjad.tools.abctools import AbjadValueObject


class TopCallback(AbjadValueObject):
    r'''Top callback.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls callback on `argument`.

        Returns selection.
        '''
        import abjad
        result = []
        for component in abjad.iterate(argument).by_class(abjad.Component):
            parentage = abjad.inspect(component).get_parentage()
            for component_ in parentage:
                if isinstance(component_, abjad.Context):
                    break
                parent = abjad.inspect(component_).get_parentage().parent
                if isinstance(parent, abjad.Context) or parent is None:
                    if component_ not in result:
                        result.append(component_)
                    break
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def depth(self):
        r'''Gets depth.

        Returns integer.
        '''
        return self._depth
