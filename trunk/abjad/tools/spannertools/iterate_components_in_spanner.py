# -*- encoding: utf-8 -*-
from abjad.tools import componenttools


def iterate_components_in_spanner(
    spanner, component_classes=None, reverse=False):
    '''.. versionadded:: 2.10

    Yield components in `spanner` one at a time from left to right:

    ::

        >>> t = Staff("c'8 d'8 e'8 f'8")
        >>> p = spannertools.BeamSpanner(t[2:])

    ::

        >>> notes = spannertools.iterate_components_in_spanner(
        ...     p, component_classes=(Note, ))

    ::

        >>> for note in notes:
        ...   note
        Note("e'8")
        Note("f'8")

    Yield components in `spanner` one at a time from right to left:

    ::

        >>> notes = spannertools.iterate_components_in_spanner(
        ...     p, component_classes=(Note, ), reverse=True)

    ::

        >>> for note in notes:
        ...   note
        Note("f'8")
        Note("e'8")

    Return generator.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import spannertools

    if not isinstance(spanner, spannertools.Spanner):
        raise TypeError

    component_classes = component_classes or (componenttools.Component, )
    if not isinstance(component_classes, tuple):
        component_classes = (component_classes, )

    if not reverse:
        for component in spanner._components:
            dfs = iterationtools.iterate_components_depth_first(component)
            for node in dfs:
                if isinstance(node, component_classes):
                    yield node
    else:
        for component in reversed(spanner._components):
            dfs = iterationtools.iterate_components_depth_first(
                component, direction=Right)
            for node in dfs:
                if isinstance(node, component_classes):
                    yield node
