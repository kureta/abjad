import collections
from abjad.tools import pitchtools
from abjad.tools.abctools import AbjadValueObject


class ByPitchCallback(AbjadValueObject):
    r'''By-pitch callback.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        '_pitches',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pitches=None,
        ):
        if pitches is not None:
            if not isinstance(pitches, collections.Iterable):
                pitches = [pitches]
            pitches = pitchtools.PitchSet(
                items=pitches,
                item_class=pitchtools.NumberedPitch,
                )
        self._pitches = pitches

    ### SPECIAL METHODS ###

    def __call__(self, argument, rotation=None):
        r'''Calls callback on `argument`.

        Returns selection.
        '''
        import abjad
        if not self.pitches:
            return ()
        result = []
        for item in argument:
            pitch_set = pitchtools.PitchSet.from_selection(
                item,
                item_class=pitchtools.NumberedPitch,
                )
            if self.pitches.intersection(pitch_set):
                result.append(item)
        return abjad.Selection(result)

    ### PUBLIC PROPERTIES ###

    @property
    def pitches(self):
        r'''Gets pitch set of pitch selector callback.

        Returns pitch set.
        '''
        return self._pitches
