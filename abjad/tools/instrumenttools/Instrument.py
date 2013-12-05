# -*- encoding: utf-8 -*-
import copy
import inspect
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class Instrument(AbjadObject):
    '''A musical instrument.
    '''

    ### CLASS VARIABLES ###

    _format_slot = 'opening'

    # TODO: change _default_performer_names to just _performer_names
    __slots__ = (
        '_allowable_clefs',
        '_default_performer_names',
        '_default_scope',
        '_instrument_name',
        '_instrument_name_markup',
        '_is_primary_instrument',
        '_pitch_range',
        '_short_instrument_name',
        '_short_instrument_name_markup',
        '_sounding_pitch_of_written_middle_c',
        '_starting_clefs',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name=None,
        short_instrument_name=None,
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range=None,
        sounding_pitch_of_written_middle_c=None,
        ):
        from abjad.tools import scoretools
        self._default_scope = scoretools.Staff

        self._instrument_name = instrument_name
        self._instrument_name_markup = instrument_name_markup
        self._short_instrument_name = short_instrument_name
        self._short_instrument_name_markup = short_instrument_name_markup

        sounding_pitch_of_written_middle_c = \
            sounding_pitch_of_written_middle_c or pitchtools.NamedPitch("c'")
        sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch(sounding_pitch_of_written_middle_c)

        allowable_clefs = allowable_clefs or ['treble']
        allowable_clefs = indicatortools.ClefInventory(allowable_clefs)

        self._default_performer_names = ['instrumentalist']

        self._allowable_clefs = allowable_clefs

        pitch_range = pitch_range or pitchtools.PitchRange('[A0, C8]')
        pitch_range = pitchtools.PitchRange(pitch_range)
        self._pitch_range = pitch_range
        self._sounding_pitch_of_written_middle_c = \
            sounding_pitch_of_written_middle_c

        self._is_primary_instrument = False
        self._starting_clefs = None

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies instrument.

        Returns new instrument.
        '''
        return type(self)(
            instrument_name=self.instrument_name,
            short_instrument_name=self.short_instrument_name,
            instrument_name_markup=self.instrument_name_markup,
            short_instrument_name_markup=self.short_instrument_name_markup,
            allowable_clefs=self.allowable_clefs,
            pitch_range=self.pitch_range,
            sounding_pitch_of_written_middle_c=\
                self.sounding_pitch_of_written_middle_c,
            )

    def __eq__(self, arg):
        r'''True when `arg` is an instrument with instrument name, short
        instrument name, instrument name markup, short instrument name markup,
        allowable clefs, pitch range and sounding pitch all equal to those of
        this instrument. Otherwise false.

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            if self.instrument_name == arg.instrument_name and \
                self.short_instrument_name == arg.short_instrument_name:
                #self.instrument_name_markup == arg.instrument_name_markup and \
                #self.short_instrument_name_markup == \
                #    arg.short_instrument_name_markup and \
                #self.allowable_clefs == arg.allowable_clefs and \
                #self.pitch_range == arg.pitch_range and \
                #self.sounding_pitch_of_written_middle_c == \
                #    arg.sounding_pitch_of_written_middle_c:
                return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats instrument.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __hash__(self):
        '''Hash value of instrument.

        Returns integer.
        '''
        return hash((
            type(self).__name__,
            self.instrument_name, 
            self.short_instrument_name,
            #self.instrument_name_markup,
            #self.short_instrument_name_markup,
            #self.allowable_clefs,
            #self.pitch_range,
            #self.sounding_pitch_of_written_middle_c,
            ))

    def __makenew__(
        self,
        instrument_name=None,
        short_instrument_name=None,
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range=None,
        sounding_pitch_of_written_middle_c=None,
        ):
        r'''Makes new instrument with optional keyword arguments.

        Returns new instrument.
        '''
        instrument_name = instrument_name or self.instrument_name
        short_instrument_name = short_instrument_name or \
            self._short_instrument_name
        instrument_name_markup = instrument_name_markup or \
            self.instrument_name_markup
        short_instrument_name_markup = short_instrument_name_markup or \
            self.short_instrument_name_markup
        allowable_clefs = allowable_clefs or self.allowable_clefs
        pitch_range = pitch_range or self.pitch_range
        sounding_pitch_of_written_middle_c = \
            sounding_pitch_of_written_middle_c or \
            self.sounding_pitch_of_written_middle_c
        new = type(self)(
            instrument_name=instrument_name,
            short_instrument_name=short_instrument_name,
            instrument_name_markup=instrument_name_markup,
            short_instrument_name_markup=short_instrument_name_markup,
            allowable_clefs=allowable_clefs,
            pitch_range=pitch_range,
            sounding_pitch_of_written_middle_c=\
                sounding_pitch_of_written_middle_c,
            )
        return new

    def __repr__(self):
        r'''Interpreter representation of instrument.

        Returns string.
        '''
        return '{}()'.format(type(self).__name__)

    ### PRIVATE PROPERTIES ###

#    @property
#    def _contents_repr_string(self):
#        result = []
#        for name in (
#            'instrument_name',
#            'instrument_name_markup',
#            'short_instrument_name',
#            'short_instrument_name_markup',
#            'allowable_clefs',
#            'pitch_range',
#            'sounding_pitch_of_written_middle_c',
#            ):
#            value = getattr(self, name)
#            default_keyword_argument_name = '_default_{}'.format(name)
#            default_value = getattr(self, default_keyword_argument_name, None)
#            if value == default_value:
#                value = None
#            if value is not None:
#                string = '{}={!r}'.format(name, value)
#                result.append(string)
#        result = ', '.join(result)
#        return result

#    @property
#    def _keyword_argument_names(self):
#        return (
#            )

    # TODO: _scope_name needs to be taken from IndicatorExpression!
    #       should not be stored on instrument.
    @property
    def _lilypond_format(self):
        result = []
        line = r'\set {!s}.instrumentName = {!s}'
        line = line.format(
            self._scope_name, 
            self.instrument_name_markup,
            )
        result.append(line)
        line = r'\set {!s}.shortInstrumentName = {!s}'
        line = line.format(
            self._scope_name, 
            self.short_instrument_name_markup,
            )
        result.append(line)
        return result

    @property
    def _one_line_menuing_summary(self):
        return self.instrument_name

    @property
    def _scope_name(self):
        if isinstance(self._default_scope, type):
            return self._default_scope.__name__
        else:
            return type(self._default_scope).__name__

#    @property
#    def _storage_format_specification(self):
#        from abjad.tools import systemtools
#        return systemtools.StorageFormatSpecification(
#            self,
#            keyword_argument_names=(
#                'instrument_name',
#                'instrument_name_markup',
#                'short_instrument_name',
#                'short_instrument_name_markup',
#                'allowable_clefs',
#                'pitch_range',
#                'sounding_pitch_of_written_middle_c',
#                ),
#            )

    ### PRIVATE METHODS ###

    def _copy_default_starting_clefs_to_default_allowable_clefs(self):
        #clefs = self._default_starting_clefs
        clefs = self._starting_clefs
        clefs = indicatortools.ClefInventory(clefs)
        #self._default_allowable_clefs = clefs
        self._allowable_clefs = clefs

    def _get_default_performer_name(self):
        if self._default_performer_names is None:
            performer_name = '{} player'.format(self._default_instrument_name)
            return performer_name
        else:
            return self._default_performer_names[-1]

    def _get_performer_names(self):
        if self._default_performer_names is None:
            performer_name = '{} player'.format(self._default_instrument_name)
            return [performer_name]
        else:
            return self._default_performer_names[:]

    @classmethod
    def _list_instrument_names(cls):
        r'''Lists instrument names.

        ::

            >>> function = instrumenttools.Instrument._list_instrument_names
            >>> for instrument_name in function():
            ...     instrument_name
            ...
            'accordion'
            'alto flute'
            ...

        Returns list.
        '''
        instrument_names = []
        for instrument_class in cls._list_instruments():
            instrument = instrument_class()
            assert instrument.instrument_name is not None, repr(instrument)
            instrument_names.append(instrument.instrument_name)
        instrument_names.sort(key=lambda x: x.lower())
        return instrument_names

    @staticmethod
    def _list_instruments(classes=None):
        r'''Lists instruments.

        ::

            >>> function = instrumenttools.Instrument._list_instruments
            >>> for instrument in function():
            ...     instrument.__name__
            ...
            'Accordion'
            'AltoFlute'
            'AltoSaxophone'
            'AltoTrombone'
            'BaritoneSaxophone'
            ...

        Returns list.
        '''
        from abjad.tools import instrumenttools
        if classes is None:
            classes = (instrumenttools.Instrument,)
        instruments = []
        for value in instrumenttools.__dict__.itervalues():
            try:
                if issubclass(value, classes):
                    if not value is instrumenttools.Instrument:
                        instruments.append(value)
            except TypeError:
                pass
        instruments.sort(key=lambda x: x.__name__.lower())
        return instruments

    @classmethod
    def _list_primary_instruments(cls):
        primary_instruments = []
        for instrument_class in cls._list_instruments():
            instrument = instrument_class()
            if instrument._is_primary_instrument:
                primary_instruments.append(instrument_class)
        return primary_instruments

    @classmethod
    def _list_secondary_instruments(cls):
        secondary_instruments = []
        for instrument_class in cls._list_instruments():
            instrument = instrument_class()
            if not instrument._is_primary_instrument:
                secondary_instruments.append(instrument_class)
        return secondary_instruments

    def _initialize_default_name_markups(self):
        #string = self._default_instrument_name
        string = self.instrument_name
        string = stringtools.capitalize_string_start(string)
        markup = markuptools.Markup(string)
        #self._default_instrument_name_markup = markup
        self._instrument_name_markup = markup
        #string = self._default_short_instrument_name
        string = self.short_instrument_name
        string = stringtools.capitalize_string_start(string)
        markup = markuptools.Markup(string)
        #self._default_short_instrument_name_markup = markup
        self._short_instrument_name_markup = markup

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets and sets allowable clefs.

        Returns clef inventory.
        '''
        if self._allowable_clefs is None:
            self._allowable_clefs = indicatortools.ClefInventory('treble')
        return self._allowable_clefs

    @property
    def instrument_name(self):
        r'''Gets and sets instrument name.

        Returns string.
        '''
        return self._instrument_name

    @property
    def instrument_name_markup(self):
        r'''Gets and sets instrument name markup.

        Returns markup.
        '''
        if self._instrument_name_markup is None:
            self._initialize_default_name_markups()
        if not isinstance(self._instrument_name_markup, markuptools.Markup):
            markup = markuptools.Markup(self._instrument_name_markup)
            self._instrument_name_markup = markup
        return self._instrument_name_markup

    @property
    def pitch_range(self):
        r'''Gets and sets pitch range.

        Returns pitch range.
        '''
        if self._pitch_range is None:
            return self._default_pitch_range
        return self._pitch_range

    @property
    def short_instrument_name(self):
        r'''Gets and sets short instrument name.

        Returns string.
        '''
        if self._short_instrument_name is None:
            return self._default_short_instrument_name
        else:
            return self._short_instrument_name

    @property
    def short_instrument_name_markup(self):
        r'''Gets and sets short instrument name markup.

        Returns markup.
        '''
        if self._short_instrument_name_markup is None:
            self._initialize_default_name_markups()
        if not isinstance(
            self._short_instrument_name_markup, markuptools.Markup):
            markup = markuptools.Markup(self._short_instrument_name_markup)
            self._short_instrument_name_markup = markup
        return self._short_instrument_name_markup

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets and sets sounding pitch of written middle C.

        Returns named pitch.
        '''
        return self._sounding_pitch_of_written_middle_c
