from abjad.components import Rest


def fuse_leaves_in_container_once_by_counts_into_little_endian_rests(container, counts):
   '''.. versionadded:: 1.1.1

   Fuse leaves in `container` once by `counts` into little-endian rests.
   '''
   from abjad.tools.leaftools._fuse_leaves_in_container_once_by_counts \
      import _fuse_leaves_in_container_once_by_counts
   
   return _fuse_leaves_in_container_once_by_counts(container, counts,
      target_type = Rest, direction = 'little-endian')
