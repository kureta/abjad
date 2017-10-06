from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools import select


class ContiguitySelectorCallback(AbjadValueObject):
    r'''Contiguity selector callback.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __call__(self, argument, rotation=None):
        r'''Iterates `argument`.

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
