from abjad.tools.schemetools.format_scheme_value import format_scheme_value
from abjad.tools.schemetools.Scheme import Scheme


class SchemePair(Scheme):
    '''Abjad model of Scheme pair::

        >>> schemetools.SchemePair('spacing', 4)
        SchemePair(('spacing', 4))

    Initialize Scheme pairs with a tuple, two separate values or another Scheme pair.

    Scheme pairs are immutable.
    '''

    __slots__ = ()

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], SchemePair):
            args = args[0]._value
        elif len(args) == 1 and isinstance(args[0], tuple):
            args = args[0][:]
        elif len(args) == 2:
            args = args
        else:
            raise TypeError('can not initialize Scheme pair from "%s".' % str(args))
        Scheme.__init__(self, *args, **kwargs)

    ### PRIVATE PROPERTIES ###

    @property
    def _formatted_value(self):
        return '(%s . %s)' % tuple([format_scheme_value(x) for x in self._value])

    ### PUBLIC PROPERTIES ###

    @property
    def format(self):
        return "#'%s" % self._formatted_value 
