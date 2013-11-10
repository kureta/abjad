# -*- encoding: utf-8 -*-
from abjad.tools.marktools.ContextMark import ContextMark


class Clef(ContextMark):
    r'''A clef.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> show(staff) # doctest: +SKIP

    ::

        >>> clef = marktools.Clef('treble')
        >>> attach(clef, staff)
        >>> clef = marktools.Clef('alto')
        >>> attach(clef, staff[1])
        >>> clef = marktools.Clef('bass')
        >>> attach(clef, staff[2])
        >>> clef = marktools.Clef('treble^8')
        >>> attach(clef, staff[3])
        >>> clef = marktools.Clef('bass_8')
        >>> attach(clef, staff[4])
        >>> clef = marktools.Clef('tenor')
        >>> attach(clef, staff[5])
        >>> clef = marktools.Clef('bass^15')
        >>> attach(clef, staff[6])
        >>> clef = marktools.Clef('percussion')
        >>> attach(clef, staff[7])
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \clef "treble"
            c'8
            \clef "alto"
            d'8
            \clef "bass"
            e'8
            \clef "treble^8"
            f'8
            \clef "bass_8"
            g'8
            \clef "tenor"
            a'8
            \clef "bass^15"
            b'8
            \clef "percussion"
            c''8
        }

    Clef marks target the staff context by default.
    '''

    ### CLASS VARIABLES ###

    _default_positional_input_arguments = (
        repr('alto'),
        )

    _format_slot = 'opening'

    ### INITIALIZER ###

    def __init__(self, clef_name):
        from abjad.tools import scoretools
        ContextMark.__init__(self, _target_context=scoretools.Staff)
        if isinstance(clef_name, str):
            self._clef_name = clef_name
        elif isinstance(clef_name, type(self)):
            self._clef_name = clef_name.clef_name
        else:
            message = 'can not initialize clef from {}.'.format(clef_name)
            raise TypeError(message)

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies clef.

        ::

            >>> import copy
            >>> clef_1 = marktools.Clef('alto')
            >>> clef_2 = copy.copy(clef_1)

        ::

            >>> clef_1, clef_2
            (Clef('alto'), Clef('alto'))

        ::

            >>> clef_1 == clef_2
            True

        ::

            >>> clef_1 is clef_2
            False

        Returns new clef.
        '''
        return type(self)(self.clef_name)

    def __eq__(self, arg):
        r'''True when clef name of `arg` equal clef name of clef.
        Otherwise false.

        ::

            >>> clef_1 = marktools.Clef('treble')
            >>> clef_2 = marktools.Clef('alto')

        ::

            >>> clef_1 == clef_1
            True
            >>> clef_1 == clef_2
            False
            >>> clef_2 == clef_1
            False
            >>> clef_2 == clef_2
            True

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            return self._clef_name == arg._clef_name
        return False

    def __format__(self, format_specification=''):
        r'''Formats clef.

        Set `format_specification` to `''`, `'lilypond'` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ::

            >>> clef = marktools.Clef('treble')
            >>> print format(clef)
            marktools.Clef(
                'treble'
                )

        Returns string.
        '''
        superclass = super(Clef, self)
        return superclass.__format__(format_specification=format_specification)

    def __ne__(self, arg):
        r'''True when clef of `arg` does not equal clef name of clef.
        False otherwise.

        ::

            >>> clef_1 = marktools.Clef('treble')
            >>> clef_2 = marktools.Clef('alto')

        ::

            >>> clef_1 != clef_1
            False
            >>> clef_1 != clef_2
            True
            >>> clef_2 != clef_1
            True
            >>> clef_2 != clef_2
            False

        Returns boolean.
        '''
        superclass = super(Clef, self)
        return superclass.__ne__(arg)

    def __repr__(self):
        r'''Interpreter representation of clef.

        ::

            >>> clef = marktools.Clef('treble')
            >>> clef
            Clef('treble')

        Returns string.
        '''
        superclass = super(Clef, self)
        return superclass.__repr__()

    ### PRIVATE PROPERTIES ###

    _clef_name_to_middle_c_position = {
        'treble': -6,
        'alto': 0,
        'tenor': 2,
        'bass': 6,
        'french': -8,
        'soprano': -4,
        'mezzosoprano': -2,
        'baritone': 4,
        'varbaritone': 4,
        'percussion': 0,
        'tab': 0
    }

    @property
    def _contents_repr_string(self):
        return repr(self._clef_name)

    @property
    def _lilypond_format(self):
        return r'\clef "%s"' % self._clef_name

    ### PUBLIC METHODS ###

    @classmethod
    def list_clef_names(cls):
        r'''Lists clef names.

        ::

            >>> for name in marktools.Clef.list_clef_names():
            ...     name
            ...
            'alto'
            'baritone'
            'bass'
            'french'
            'mezzosoprano'
            'percussion'
            'soprano'
            'tab'
            'tenor'
            'treble'
            'varbaritone'

        Returns list of strings.
        '''
        return list(sorted(cls._clef_name_to_middle_c_position))

    ### PUBLIC PROPERTIES ###

    @apply
    def clef_name():
        def fget(self):
            r'''Gets and sets clef name.

            ::

                >>> clef = marktools.Clef('treble')
                >>> clef.clef_name
                'treble'

            ::

                >>> clef.clef_name = 'alto'
                >>> clef.clef_name
                'alto'

            Returns string.
            '''
            return self._clef_name
        def fset(self, clef_name):
            assert isinstance(clef_name, str)
            self._clef_name = clef_name
        return property(**locals())

    @property
    def middle_c_position(self):
        r'''Middle C position of clef.

        ::

            >>> clef = marktools.Clef('treble')
            >>> clef.middle_c_position
            -6

        Returns integer number of stafflines.
        '''
        alteration = 0
        if '_' in self._clef_name:
            base_name, part, suffix = self._clef_name.partition('_')
            if suffix == '8':
                alteration = 7
            elif suffix == '15':
                alteration = 13
            else:
                message = "Bad clef alteration suffix: {!r}"
                message = message.format(suffix)
                raise Exception(message)
        elif '^' in self._clef_name:
            base_name, part, suffix = self._clef_name.partition('^')
            if suffix == '8':
                alteration = -7
            elif suffix == '15':
                alteration = -13
            else:
                message = "Bad clef alteration suffix: {!r}"
                message = message.format(suffix)
                raise Exception(message)
        else:
            base_name = self._clef_name
        return self._clef_name_to_middle_c_position[base_name] + alteration
