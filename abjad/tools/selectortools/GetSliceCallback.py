from abjad.tools.abctools import AbjadValueObject


class GetSliceCallback(AbjadValueObject):
    r'''Get-slice callback.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        '_start',
        '_stop',
        )

    ### INITIALIZER ###

    def __init__(self, start=None, stop=None):
        assert isinstance(start, (int, type(None)))
        assert isinstance(stop, (int, type(None)))
        self._start = start
        self._stop = stop

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        r'''Calls callback on `argument`.

        ..  container:: example

            ::

                >>> string = r"c'4 \times 2/3 { d'8 r8 e'8 } r16 f'16 g'8 a'4"
                >>> staff = abjad.Staff(string)
                >>> show(staff) # doctest: +SKIP

            ::

                >>> selector = abjad.select()
                >>> selector = selector.get_slice(start=-4)
                >>> selector(staff)
                Selection([Rest('r16'), Note("f'16"), Note("g'8"), Note("a'4")])

        Returns object of `argument` type.
        '''
        slice_ = slice(self.start, self.stop)
        return argument.__getitem__(slice_)

    ### PUBLIC PROPERTIES ###

    @property
    def start(self):
        r'''Gets start.

        Returns integer or none.
        '''
        return self._start

    @property
    def stop(self):
        r'''Gets stop.

        Returns integer or none.
        '''
        return self._stop
