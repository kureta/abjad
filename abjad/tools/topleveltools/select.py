def select(argument=None):
    r'''Selects `argument` or makes empty selector.

    ..  container:: example

        Selects first two notes in staff:

        ::

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> selection = abjad.select(staff[:2])
            >>> for note in selection:
            ...     abjad.override(note).note_head.color = 'red'

        ::

            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \once \override NoteHead.color = #red
                c'4
                \once \override NoteHead.color = #red
                d'4
                e'4
                f'4
            }

    ..  container:: example

        Initializes empty selector:

        ::

            >>> abjad.select()
            Selector()

    Returns selector when `argument` is none.

    Returns selection when `argument` is not none.
    '''
    import abjad
    if argument is None:
        return abjad.Selector()
    return abjad.Selection(argument)
