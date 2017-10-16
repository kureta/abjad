import collections
from abjad.tools.abctools import AbjadValueObject


class PartitionByCountsCallback(AbjadValueObject):
    r'''Partition-by-counts callback.

    ..  container:: example

        Initializes callback by hand:

        ::

            >>> callback = abjad.PartitionByCountsCallback([3])
            >>> f(callback)
            abjad.PartitionByCountsCallback(
                counts=abjad.CyclicTuple(
                    [3]
                    ),
                cyclic=True,
                fuse_overhang=False,
                nonempty=False,
                overhang=True,
                rotate=True,
                )

    ..  container:: example

        Selects components:

        ::

            >>> selector = abjad.select()
            >>> selector = selector.by_leaf()
            >>> selector = selector.partition_by_counts([3])
            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8 b'8 r8 c''8")
            >>> selector(staff)
            [Selection([Note("c'8"), Rest('r8'), Note("d'8")])]

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        '_counts',
        '_cyclic',
        '_fuse_overhang',
        '_overhang',
        '_rotate',
        '_nonempty',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        counts=(3,),
        cyclic=True,
        fuse_overhang=False,
        nonempty=False,
        overhang=True,
        rotate=True,
        ):
        import abjad
        counts = abjad.CyclicTuple(int(_) for _ in counts)
        self._counts = counts
        self._cyclic = bool(cyclic)
        self._fuse_overhang = bool(fuse_overhang)
        self._overhang = bool(overhang)
        self._rotate = bool(rotate)
        self._nonempty = bool(nonempty)

    ### SPECIAL METHODS ###

    def __call__(self, argument, rotation=None):
        r'''Calls callback on `argument`.

        Returns list of selections.
        '''
        import abjad
        if rotation is None:
            rotation = 0
        rotation = int(rotation)
        result = []
        counts = self.counts
        if self.rotate:
            counts = abjad.Sequence(counts).rotate(n=-rotation)
            counts = abjad.CyclicTuple(counts)
        groups = abjad.Sequence(argument).partition_by_counts(
            [abs(_) for _ in counts],
            cyclic=self.cyclic,
            overhang=self.overhang,
            )
        groups = list(groups)
        if self.overhang and self.fuse_overhang and 1 < len(groups):
            last_count = counts[(len(groups) - 1) % len(counts)]
            if len(groups[-1]) != last_count:
                last_group = groups.pop()
                groups[-1] += last_group
        subresult = []
        for i, group in enumerate(groups):
            try:
                count = counts[i]
            except:
                raise Exception(counts, i)
            if count < 0:
                continue
            items = abjad.Selection(group)
            subresult.append(items)
        if self.nonempty and not subresult:
            group = abjad.Selection(groups[0])
            subresult.append(group)
        result.extend(subresult)
        if self.rotate:
            counts = abjad.Sequence(counts).rotate(n=-1)
            counts = abjad.CyclicTuple(counts)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def counts(self):
        r'''Gets counts.

        Returns tuple.
        '''
        return self._counts

    @property
    def cyclic(self):
        r'''Is true when callback partitions cyclically.

        Returns true or false.
        '''
        return self._cyclic

    @property
    def fuse_overhang(self):
        r'''Is true when callback fuses overhang.

        Returns ordinal constant.
        '''
        return self._fuse_overhang

    @property
    def nonempty(self):
        r'''Gets nonempty flag.

        Returns true or false.
        '''
        return self._nonempty

    @property
    def overhang(self):
        r'''Is true when callback returns overhang.

        Returns true or false.
        '''
        return self._overhang

    @property
    def rotate(self):
        r'''Gets rotation.

        Returns true or false.
        '''
        return self._rotate
