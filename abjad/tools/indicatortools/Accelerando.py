from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Accelerando(AbjadValueObject):
    r'''Accelerando.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> score = abjad.Score([staff])
        >>> accelerando = abjad.Accelerando()
        >>> abjad.attach(accelerando, staff[0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score <<
                \new Staff {
                    c'4
                        ^ \markup {
                            \large
                                \upright
                                    accel.
                            }
                    d'4
                    e'4
                    f'4
                }
            >>

    Accelerandi format as LilyPond markup.

    Accelerandi are not followed by any type of dashed line or other spanner.

    Use accelerandi with a metronome mark spanner to generate dashed lines and
    other spanners.

    ..  todo:: add metronome mark spanner example.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_context',
        '_markup',
        )

    ### INITIALIZER ###

    def __init__(self, markup=None):
        import abjad
        self._context = 'Score'
        if markup is not None:
            assert isinstance(markup, abjad.Markup)
        self._markup = markup

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string representation of accelerando.

        ..  container:: example

            String representation of accelerando with default markup:

            >>> print(str(abjad.Accelerando()))
            \markup {
                \large
                    \upright
                        accel.
                }

        ..  container:: example

            String representation of accelerando with custom markup:

            >>> markup = abjad.Markup(r'\bold { \italic { accelerando } }')
            >>> accelerando = abjad.Accelerando(markup=markup)
            >>> print(str(accelerando))
            \markup {
                \bold
                    {
                        \italic
                            {
                                accelerando
                            }
                    }
                }

        Returns string.
        '''
        return str(self._to_markup())

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return str(self)

    @property
    def _default_markup(self):
        from abjad.tools import markuptools
        contents = r'\large \upright accel.'
        return markuptools.Markup(contents=contents)

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        markup = self._to_markup()
        markup = abjad.new(markup, direction=abjad.Up)
        markup_format_pieces = markup._get_format_pieces()
        bundle.right.markup.extend(markup_format_pieces)
        return bundle

    def _to_markup(self):
        if self.markup is not None:
            return self.markup
        return self._default_markup

    ### PUBLIC PROPERTIES ###

    @property
    def context(self):
        r'''Gets default context of accelerando.

        ..  container:: example

            >>> accelerando = abjad.Accelerando()
            >>> accelerando.context
            'Score'

        Returns context or string.
        '''
        return self._context

    @property
    def markup(self):
        r'''Gets markup of accelerando.

        ..  container:: example

            >>> markup = abjad.Markup(r'\bold { \italic { accel. } }')
            >>> accelerando = abjad.Accelerando(markup=markup)
            >>> print(str(accelerando.markup))
            \markup {
                \bold
                    {
                        \italic
                            {
                                accel.
                            }
                    }
                }

        Returns markup or none.
        '''
        return self._markup
