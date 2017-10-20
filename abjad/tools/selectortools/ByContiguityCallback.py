from abjad.tools.abctools import AbjadValueObject


class ByContiguityCallback(AbjadValueObject):
    r'''By-contiguity callback.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        r'''Calls callback on `argument`.

        Returns list of selections.
        '''
        import abjad
        selections, selection = [], []
        selection.extend(argument[:1])
        for item in argument[1:]:
            try:
                this_timespan = selection[-1]._get_timespan()
            except AttributeError:
                this_timespan = selection[-1].get_timespan()
            try:
                that_timespan = item._get_timespan()
            except AttributeError:
                that_timespan = item.get_timespan()
            if this_timespan.stop_offset == that_timespan.start_offset:
                selection.append(item)
            else:
                selections.append(abjad.Selection(selection))
                selection = [item]
        if selection:
            selections.append(abjad.Selection(selection))
        return selections
