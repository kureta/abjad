# -*- encoding: utf-8 -*-
import copy
import inspect
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject


# Note that instruments are the classes in the system that 
# implement default attribute values.
#
# That means that three things are true.
#
# First, all instruments come supplied with a default name and 
# a default short instrument name.
#
# Second, all instruments allow users to override both instrument name 
# and short instrument name.
#
# Third, all instruments 'remember' default values 
# when such values are overridden.
#
# When all three of these things are the case we talk about a class 
# implementing default attribute values.
#
# This is the meaning of the '_has_default_attribute_values' class attribute.
# The impact this currently has in the system concerns the 
# storage format of such objects.
class Instrument(AbjadObject):
    '''A musical instrument.
    '''

    ### CLASS VARIABLES ###

    _format_slot = 'opening'

    _has_default_attribute_values = True

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name=None,
        short_instrument_name=None,
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        ):
        from abjad.tools import scoretools
        self._default_scope = scoretools.Staff
        self._default_instrument_name = instrument_name
        self._default_instrument_name_markup = instrument_name_markup
        self._default_short_instrument_name = short_instrument_name
        self._default_short_instrument_name_markup = \
            short_instrument_name_markup
        self.instrument_name = instrument_name
        self.instrument_name_markup = instrument_name_markup
        self.short_instrument_name = short_instrument_name
        self.short_instrument_name_markup = short_instrument_name_markup
        pitch = pitchtools.NamedPitch("c'")
        clefs = indicatortools.ClefInventory(['treble'])
        self._default_allowable_clefs = copy.deepcopy(clefs)
        self._default_performer_names = ['instrumentalist']
        self._default_sounding_pitch_of_written_middle_c = pitch
        self._default_starting_clefs = copy.deepcopy(clefs)
        self._allowable_clefs = None
        self._is_primary_instrument = False
        self._pitch_range = None
        self._sounding_pitch_of_written_middle_c = None
        self._starting_clefs = None

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies instrument.

        Returns new instrument.
        '''
        return type(self)(
            instrument_name_markup=self.instrument_name_markup, 
            short_instrument_name_markup=self.short_instrument_name_markup,
            )

    def __eq__(self, arg):
        r'''True when instrument equals `arg`.
        Otherwise false.

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            if self.instrument_name == arg.instrument_name:
                if self.short_instrument_name == arg.short_instrument_name:
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
            ))

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        result = []
        for name in (
            'instrument_name',
            'instrument_name_markup',
            'short_instrument_name',
            'short_instrument_name_markup',
            'allowable_clefs',
            'pitch_range',
            'sounding_pitch_of_written_middle_c',
            ):
            value = getattr(self, name)
            default_keyword_argument_name = '_default_{}'.format(name)
            default_value = getattr(self, default_keyword_argument_name, None)
            if value == default_value:
                value = None
            if value is not None:
                string = '{}={!r}'.format(name, value)
                result.append(string)
        result = ', '.join(result)
        return result

    @property
    def _keyword_argument_names(self):
        return (
            )

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

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=(
                'instrument_name',
                'instrument_name_markup',
                'short_instrument_name',
                'short_instrument_name_markup',
                'allowable_clefs',
                'pitch_range',
                'sounding_pitch_of_written_middle_c',
                ),
            )

    ### PRIVATE METHODS ###

    def _copy_default_starting_clefs_to_default_allowable_clefs(self):
        clefs = self._default_starting_clefs
        clefs = indicatortools.ClefInventory(clefs)
        self._default_allowable_clefs = clefs

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
            'alto saxophone'
            'alto trombone'
            'baritone saxophone'
            'baritone voice'
            'bass clarinet'
            'bass flute'
            'bass saxophone'
            'bass trombone'
            'bass voice'
            'bassoon'
            'cello'
            ...

        Returns list.
        '''
        instrument_names = []
        for instrument_class in cls._list_instruments():
            instrument = instrument_class()
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

    def _make_default_name_markups(self):
        string = self._default_instrument_name
        string = stringtools.capitalize_string_start(string)
        markup = markuptools.Markup(string)
        self._default_instrument_name_markup = markup
        string = self._default_short_instrument_name
        string = stringtools.capitalize_string_start(string)
        markup = markuptools.Markup(string)
        self._default_short_instrument_name_markup = markup

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets and sets allowable clefs.

        Returns clef inventory.
        '''
        if self._allowable_clefs is None:
            clefs = self._default_allowable_clefs
            clefs = indicatortools.ClefInventory(clefs)
            self._allowable_clefs = clefs
        return self._allowable_clefs

    @allowable_clefs.setter
    def allowable_clefs(self, clefs):
        if clefs is not None:
            clefs = indicatortools.ClefInventory(clefs)
        self._allowable_clefs = clefs

    @property
    def instrument_name(self):
        r'''Gets and sets instrument name.

        Returns string.
        '''
        if self._instrument_name is None:
            return self._default_instrument_name
        else:
            return self._instrument_name

    @instrument_name.setter
    def instrument_name(self, instrument_name):
        assert isinstance(instrument_name, (str, type(None)))
        self._instrument_name = instrument_name

    @property
    def instrument_name_markup(self):
        r'''Gets and sets instrument name markup.

        Returns markup.
        '''
        if self._instrument_name_markup is None:
            if self._default_instrument_name_markup is None:
                self._make_default_name_markups()
            markup = self._default_instrument_name_markup
            markup = copy.copy(markup)
            self._instrument_name_markup = markup
        return self._instrument_name_markup

    @instrument_name_markup.setter
    def instrument_name_markup(self, instrument_name_markup):
        from abjad.tools.markuptools import Markup
        assert isinstance(
            instrument_name_markup, (str, type(Markup('')), type(None)))
        if instrument_name_markup is None:
            self._instrument_name_markup = instrument_name_markup
        else:
            self._instrument_name_markup = Markup(instrument_name_markup)

    @property
    def pitch_range(self):
        r'''Gets and sets pitch range.

        Returns pitch range.
        '''
        if self._pitch_range is None:
            return self._default_pitch_range
        return self._pitch_range

    @pitch_range.setter
    def pitch_range(self, pitch_range):
        if pitch_range is not None:
            pitch_range = pitchtools.PitchRange(pitch_range)
        self._pitch_range = pitch_range

    @property
    def short_instrument_name(self):
        r'''Gets and sets short instrument name.

        Returns string.
        '''
        if self._short_instrument_name is None:
            return self._default_short_instrument_name
        else:
            return self._short_instrument_name

    @short_instrument_name.setter
    def short_instrument_name(self, short_instrument_name):
        assert isinstance(short_instrument_name, (str, type(None)))
        self._short_instrument_name = short_instrument_name

    @property
    def short_instrument_name_markup(self):
        r'''Gets and sets short instrument name markup.

        Returns markup.
        '''
        if self._short_instrument_name_markup is None:
            if self._default_instrument_name_markup is None:
                self._make_default_name_markups()
            markup = self._default_short_instrument_name_markup
            markup = copy.copy(markup)
            self._short_instrument_name_markup = markup
        return self._short_instrument_name_markup

    @short_instrument_name_markup.setter
    def short_instrument_name_markup(self, short_instrument_name_markup):
        from abjad.tools import markuptools
        prototype = (str, type(markuptools.Markup('')), type(None))
        assert isinstance(short_instrument_name_markup, prototype)
        if short_instrument_name_markup is None:
            markup = short_instrument_name_markup
            self._short_instrument_name_markup = markup
        else:
            markup = markuptools.Markup(short_instrument_name_markup)
            self._short_instrument_name_markup = markup

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets and sets sounding pitch of written middle C.

        Returns named pitch.
        '''
        if self._sounding_pitch_of_written_middle_c is None:
            return self._default_sounding_pitch_of_written_middle_c
        return self._sounding_pitch_of_written_middle_c

    @sounding_pitch_of_written_middle_c.setter
    def sounding_pitch_of_written_middle_c(self, pitch):
        pitch = pitch or self._default_sounding_pitch_of_written_middle_c
        pitch = pitchtools.NamedPitch(pitch)
        self._sounding_pitch_of_written_middle_c = pitch
