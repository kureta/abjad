import collections
import itertools
from abjad.tools.abctools import AbjadValueObject


class GroupByPitchCallback(AbjadValueObject):
    r'''Group-by-pitch callback.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        '_allow_discontiguity',
        )

    ### INITIALIZER ###

    def __init__(self, allow_discontiguity=False):
        if allow_discontiguity is not None:
            allow_discontiguity = bool(allow_discontiguity)
        self._allow_discontiguity = allow_discontiguity

    ### SPECIAL METHODS ###

    def __call__(self, music=None):
        r'''Calls callback on `music`.

        Returns selection or list.
        '''
        import abjad
        groups = self._group_by(music, self._get_written_pitches)
        groups = self._map_contiguity(groups)
        return abjad.Selection._manifest(groups)

    ### PRIVATE METHODS ###

    @staticmethod
    def _get_written_pitches(argument):
        import abjad
        if isinstance(argument, abjad.Note):
            return argument.written_pitch
        elif isinstance(argument, abjad.Chord):
            return argument.written_pitches
        elif (isinstance(argument, abjad.LogicalTie) and
            isinstance(argument.head, abjad.Note)):
            return argument.head.written_pitch
        elif (isinstance(argument, abjad.LogicalTie) and
            isinstance(argument.head, abjad.Chord)):
            return argument.head.written_pitches
        else:
            return None

    @staticmethod
    def _group_by(iterable, predicate):
        import abjad
        groups = []
        grouper = itertools.groupby(iterable, predicate)
        for label, generator in grouper:
            group = abjad.Selection._manifest(generator)
            groups.append(group)
        return groups

    # TODO: reimplement with self.map(); then remove
    def _map_contiguity(self, groups):
        import abjad
        if self.allow_discontiguity:
            return groups
        selector = abjad.ByContiguityCallback()
        result = []
        for group in groups:
            subgroups = selector(group)
            result.extend(subgroups)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def allow_discontiguity(self):
        r'''Is true when selector allow discontiguity.

        Otherwise selector further groups by contiguity.

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        '''
        return self._allow_discontiguity
