# -*- encoding: utf-8 -*-
def delete_contents_of_container_starting_before_or_at_offset(container, prolated_offset):
    r'''.. versionadded:: 2.0

    Delete contents of `container` starting before or at `prolated_offset`:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> spannertools.BeamSpanner(staff.select_leaves())
        BeamSpanner(c'8, d'8, e'8, f'8)

    ::

        >>> f(staff)
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
        }

    ::

        >>> containertools.delete_contents_of_container_starting_before_or_at_offset(
        ...     staff, Duration(1, 8))
        Staff{2}

    ::

        >>> f(staff)
        \new Staff {
            e'8 [
            f'8 ]
        }

    Return `container`.
    '''
    from abjad.tools import containertools

    # get index
    try:
        element = containertools.get_first_element_starting_before_or_at_offset(container, prolated_offset)
        index = container.index(element)

    # return container if no index
    except ValueError:
        return container

    # delete elements
    del(container[:index+1])

    # return container
    return container
