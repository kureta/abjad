# -*- encoding: utf-8 -*-
import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class ChromaticObject(AbjadObject):
    '''..versionadded:: 2.0

    Chromatic object base class.
    '''

    ### CLASS VARIABLES ##

    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass
