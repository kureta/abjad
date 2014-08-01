# -*- encoding: utf-8 -*-


def list_all_scoremanager_classes(modules=None):
    r'''Lists all public classes defined in Abjad.

    ::

        >>> all_classes = documentationtools.list_all_scoremanager_classes()

    '''
    from abjad.tools import documentationtools
    return documentationtools.list_all_classes('scoremanager')