# -*- encoding: utf-8 -*-
import types
from abjad.tools import selectiontools


def all_are_components_in_same_thread(expr, classes=None, allow_orphans=True):
    '''.. versionadded:: 1.1

    True when elements in `expr` are all components in same thread. 
    Otherwise false:

    ::

        >>> voice = Voice("c'8 d'8 e'8")
        >>> componenttools.all_are_components_in_same_thread(voice.select_leaves())
        True

    True when elements in `expr` are all `classes` in same thread. 
    Otherwise false:

    ::

        >>> voice = Voice("c'8 d'8 e'8")
        >>> componenttools.all_are_components_in_same_thread(
        ...     voice.select_leaves(), classes=Note)
        True

    Return boolean.
    '''
    from abjad.tools import componenttools

    allowable_types = (
        list,
        tuple,
        types.GeneratorType,
        selectiontools.SequentialSelection,
        )

    if not isinstance(expr, allowable_types):
        return False

    if classes is None:
        classes = componenttools.Component

    if len(expr) == 0:
        return True

    first = expr[0]
    if not isinstance(first, classes):
        return False

    orphan_components = True
    if not first.select_parentage().is_orphan:
        orphan_components = False

    same_thread = True

    first_signature = first.select_parentage().containment_signature
    for component in expr[1:]:
        if not component.select_parentage().is_orphan:
            orphan_components = False
        if component.select_parentage().containment_signature != first_signature:
            same_thread = False
        if not allow_orphans and not same_thread:
            return False
        if allow_orphans and not orphan_components and not same_thread:
            return False

    return True
