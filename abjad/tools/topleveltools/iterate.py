def iterate(client=None):
    r'''Makes iteration agent.

    ..  container:: example

        Example staff:

        ::

            >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                c'4
                e'4
                d'4
                f'4
            }

    ..  container:: example

        Iterates pitches:

            >>> for pitch in abjad.iterate(staff).by_pitch():
            ...     pitch
            ...
            NamedPitch("c'")
            NamedPitch("e'")
            NamedPitch("d'")
            NamedPitch("f'")

    ..  container:: example

        Returns iteration:

        ::

            >>> abjad.iterate(staff)
            Iteration(client=Staff("c'4 e'4 d'4 f'4"))

    '''
    import abjad
    if client is not None:
        return abjad.Iteration(client=client)
    expression = abjad.Expression()
    expression = expression.iterate()
    return expression
