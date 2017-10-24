import collections
import copy
import inspect
import itertools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Selection(AbjadValueObject):
    r'''Selection of items (components / or other selections).

    ..  container:: example

        Selects leaves:

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> abjad.show(staff) # doctest: +SKIP

            >>> for leaf in abjad.select(staff).by_leaf():
            ...     leaf
            ...
            Note("c'4")
            Note("d'4")
            Note("e'4")
            Note("f'4")

        ..  container:: example expression

            >>> expression = abjad.select().by_leaf()
            >>> result = expression(staff)

            >>> expression.print(result)
            Note("c'4")
            Note("d'4")
            Note("e'4")
            Note("f'4")

            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff \with {
                autoBeaming = ##f
            } {
                \once \override Accidental.color = #red
                \once \override Beam.color = #red
                \once \override Dots.color = #red
                \once \override NoteHead.color = #red
                \once \override Stem.color = #red
                c'4
                \once \override Accidental.color = #blue
                \once \override Beam.color = #blue
                \once \override Dots.color = #blue
                \once \override NoteHead.color = #blue
                \once \override Stem.color = #blue
                d'4
                \once \override Accidental.color = #red
                \once \override Beam.color = #red
                \once \override Dots.color = #red
                \once \override NoteHead.color = #red
                \once \override Stem.color = #red
                e'4
                \once \override Accidental.color = #blue
                \once \override Beam.color = #blue
                \once \override Dots.color = #blue
                \once \override NoteHead.color = #blue
                \once \override Stem.color = #blue
                f'4
            }

    ..  container:: example
    
        Selects note runs:

        ..  container:: example

            >>> string = r"c'4 \times 2/3 { d'8 r8 e'8 } r16 f'16 g'8 a'4"
            >>> staff = abjad.Staff(string)
            >>> abjad.show(staff) # doctest: +SKIP

            >>> for run in abjad.select(staff).by_leaf().by_run(abjad.Note):
            ...     run
            ...
            Selection([Note("c'4"), Note("d'8")])
            Selection([Note("e'8")])
            Selection([Note("f'16"), Note("g'8"), Note("a'4")])

        ..  container:: example expression

            >>> expression = abjad.select().by_leaf().by_run(abjad.Note)
            >>> result = expression(staff)

            >>> expression.print(result)
            Selection([Note("c'4"), Note("d'8")])
            Selection([Note("e'8")])
            Selection([Note("f'16"), Note("g'8"), Note("a'4")])

            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff \with {
                autoBeaming = ##f
            } {
                \once \override Accidental.color = #red
                \once \override Beam.color = #red
                \once \override Dots.color = #red
                \once \override NoteHead.color = #red
                \once \override Stem.color = #red
                c'4
                \times 2/3 {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    d'8
                    r8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    e'8
                }
                r16
                \once \override Accidental.color = #red
                \once \override Beam.color = #red
                \once \override Dots.color = #red
                \once \override NoteHead.color = #red
                \once \override Stem.color = #red
                f'16
                \once \override Accidental.color = #red
                \once \override Beam.color = #red
                \once \override Dots.color = #red
                \once \override NoteHead.color = #red
                \once \override Stem.color = #red
                g'8
                \once \override Accidental.color = #red
                \once \override Beam.color = #red
                \once \override Dots.color = #red
                \once \override NoteHead.color = #red
                \once \override Stem.color = #red
                a'4
            }

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Selections'

    __slots__ = (
        '_expression',
        '_items',
        )

    ### INITIALIZER ###

    def __init__(self, items=None):
        import abjad
        if items is None:
            items = []
        if isinstance(items, abjad.Component):
            items = [items]
        items = tuple(items)
        self._check(items)
        self._items = tuple(items)
        self._expression = None

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        r'''Cocatenates `argument` to selection.

        Returns new selection.
        '''
        assert isinstance(argument, collections.Iterable)
        items = self.items + tuple(argument)
        return type(self)(items=items)

    def __contains__(self, argument):
        r'''Is true when `argument` is in selection. Otherwise false.

        Returns true or false.
        '''
        return argument in self.items

    def __eq__(self, argument):
        r'''Is true when selection and `argument` are of the same type
        and when items in selection equal item in `argument`.
        Otherwise false.

        Returns true or false.
        '''
        if isinstance(argument, type(self)):
            return self.items == argument.items
        elif isinstance(argument, collections.Sequence):
            return self.items == tuple(argument)
        return False

    def __format__(self, format_specification=''):
        r'''Formats duration.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        import abjad
        if format_specification in ('', 'storage'):
            return abjad.StorageFormatManager(self).get_storage_format()
        return str(self)

    def __getitem__(self, argument):
        r'''Gets item, slice or pattern `argument`.

        ..  container:: example

            Gets every other leaf:

            ..  container:: example

                >>> string = r"c'8 d'8 ~ d'8 e'8 ~ e'8 ~ e'8 r8 f'8"
                >>> staff = abjad.Staff(string)
                >>> abjad.show(staff) # doctest: +SKIP

                >>> pattern = abjad.index_every([0], 2)
                >>> for leaf in abjad.select(staff).by_leaf()[pattern]:
                ...     leaf
                ...
                Note("c'8")
                Note("d'8")
                Note("e'8")
                Rest('r8')

            ..  container:: example expression

                >>> expression = abjad.select().by_leaf()[pattern]
                >>> result = expression(staff)

                >>> expression.print(result)
                Note("c'8")
                Note("d'8")
                Note("e'8")
                Rest('r8')

                >>> expression.color(result)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'8
                    d'8 ~
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    d'8
                    e'8 ~
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    e'8 ~
                    e'8
                    \once \override Dots.color = #blue
                    \once \override Rest.color = #blue
                    r8
                    f'8
                }

        ..  container:: example

            Gets every other logical tie:

            ..  container:: example

                >>> string = r"c'8 d'8 ~ d'8 e'8 ~ e'8 ~ e'8 r8 f'8"
                >>> staff = abjad.Staff(string)
                >>> abjad.show(staff) # doctest: +SKIP

                >>> pattern = abjad.index_every([0], 2)
                >>> selection = abjad.select(staff).by_logical_tie(pitched=True)
                >>> for logical_tie in selection[pattern]:
                ...     logical_tie
                ...
                LogicalTie([Note("c'8")])
                LogicalTie([Note("e'8"), Note("e'8"), Note("e'8")])

            ..  container:: example expression

                >>> expression = abjad.select().by_logical_tie(pitched=True)
                >>> expression = expression[pattern]
                >>> result = expression(staff)

                >>> expression.print(result)
                LogicalTie([Note("c'8")])
                LogicalTie([Note("e'8"), Note("e'8"), Note("e'8")])

                >>> expression.color(result)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'8
                    d'8 ~
                    d'8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    e'8 ~
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    e'8 ~
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    e'8
                    r8
                    f'8
                }

        ..  container:: example expression

            Selects note 1 (or nothing) in each pitched logical tie:

            >>> staff = abjad.Staff(r"c'8 d'8 ~ d'8 e'8 ~ e'8 ~ e'8 r8 f'8")

            >>> expression = abjad.select().by_logical_tie(pitched=True)
            >>> get = abjad.select().by_leaf()[abjad.index([1])]
            >>> expression = expression.map(get)
            >>> result = expression(staff)

            >>> expression.print(result)
            Sequence([])
            Sequence([Note("d'8")])
            Sequence([Note("e'8")])
            Sequence([])

            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff \with {
                autoBeaming = ##f
            } {
                c'8
                d'8 ~
                \once \override Accidental.color = #blue
                \once \override Beam.color = #blue
                \once \override Dots.color = #blue
                \once \override NoteHead.color = #blue
                \once \override Stem.color = #blue
                d'8
                e'8 ~
                \once \override Accidental.color = #red
                \once \override Beam.color = #red
                \once \override Dots.color = #red
                \once \override NoteHead.color = #red
                \once \override Stem.color = #red
                e'8 ~
                e'8
                r8
                f'8
            }

        Returns a single item when `argument` is an integer.

        Returns new selection of zero or more items when `argument` is a slice.

        Returns new selection of zero or more items when `argument` is a
        pattern.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        if isinstance(argument, abjad.Pattern):
            result = abjad.sequence(self.items).retain_pattern(argument)
        else:
            result = self.items.__getitem__(argument)
        if isinstance(result, tuple):
            result = Selection(result)
        return result

    def __getstate__(self):
        r'''Gets state of selection.

        Returns dictionary.
        '''
        if hasattr(self, '__dict__'):
            state = vars(self).copy()
        else:
            state = {}
        for class_ in type(self).__mro__:
            for slot in getattr(class_, '__slots__', ()):
                try:
                    state[slot] = getattr(self, slot)
                except AttributeError:
                    pass
        return state

    def __hash__(self):
        r'''Hashes selection.

        Reimplemented together with `__eq__()`.

        Returns integer.
        '''
        return super(Selection, self).__hash__()

    def __illustrate__(self):
        r'''Attempts to illustrate selection.

        Evaluates the storage format of the selection (to sever any references
        to the source score from which the selection was taken). Then tries to
        wrap the result in a staff; in the case that notes of only C4 are found
        then sets the staff context name to ``'RhythmicStaff'``. If this works
        then the staff is wrapped in a LilyPond file and the file is returned.
        If this doesn't work then the method raises an exception.

        The idea is that the illustration should work for simple selections of
        that represent an essentially contiguous snippet of a single voice of
        music.

        Returns LilyPond file.
        '''
        import abjad
        components = abjad.mutate(self).copy()
        staff = abjad.Staff(components)
        found_different_pitch = False
        for pitch in abjad.iterate(staff).by_pitch():
            if pitch != abjad.NamedPitch("c'"):
                found_different_pitch = True
                break
        if not found_different_pitch:
            staff.context_name = 'RhythmicStaff'
        score = abjad.Score([staff])
        lilypond_file = abjad.LilyPondFile.new(score)
        lilypond_file.header_block.tagline = False
        return lilypond_file

    def __len__(self):
        r'''Gets number of items in selection.

        Returns nonnegative integer.
        '''
        return len(self.items)

    def __radd__(self, argument):
        r'''Concatenates selection to `argument`.

        Returns newly created selection.
        '''
        assert isinstance(argument, collections.Iterable)
        items = tuple(argument) + self.items
        return type(self)(items=items)

    def __repr__(self):
        r'''Gets interpreter representation of selection.

        Returns string.
        '''
        import abjad
        return abjad.StorageFormatManager(self).get_repr_format()

    def __setstate__(self, state):
        r'''Sets state of selection.

        Returns none.
        '''
        for key, value in state.items():
            setattr(self, key, value)

    ### PRIVATE METHODS ###

    def _attach_tie_spanner_to_leaf_pair(self, use_messiaen_style_ties=False):
        import abjad
        assert len(self) == 2
        left_leaf, right_leaf = self
        assert isinstance(left_leaf, abjad.Leaf), left_leaf
        assert isinstance(right_leaf, abjad.Leaf), right_leaf
        left_logical_tie = left_leaf._get_logical_tie()
        right_logical_tie = right_leaf._get_logical_tie()
        if left_logical_tie == right_logical_tie:
            return
        try:
            left_tie_spanner = left_leaf._get_spanner(abjad.Tie)
        except MissingSpannerError:
            left_tie_spanner = None
        try:
            right_tie_spanner = right_leaf._get_spanner(abjad.Tie)
        except MissingSpannerError:
            right_tie_spanner = None
        if left_tie_spanner is not None and right_tie_spanner is not None:
            left_tie_spanner._fuse_by_reference(right_tie_spanner)
        elif left_tie_spanner is not None and right_tie_spanner is None:
            left_tie_spanner._append(right_leaf)
        elif left_tie_spanner is None and right_tie_spanner is not None:
            right_tie_spanner._append_left(left_leaf)
        elif left_tie_spanner is None and right_tie_spanner is None:
            tie = abjad.Tie(
                use_messiaen_style_ties=use_messiaen_style_ties,
                )
            leaves = abjad.select([left_leaf, right_leaf])
            abjad.attach(tie, leaves)

    def _attach_tie_spanner_to_leaves(self, use_messiaen_style_ties=False):
        import abjad
        pairs = abjad.sequence(self).nwise()
        for leaf_pair in pairs:
            selection = abjad.select(leaf_pair)
            selection._attach_tie_spanner_to_leaf_pair(
                use_messiaen_style_ties=use_messiaen_style_ties,
                )

    @classmethod
    def _by_class(
        class_,
        argument,
        prototype=None,
        head=None,
        tail=None,
        trim=None,
        ):
        import abjad
        prototype = prototype or abjad.Component
        if not isinstance(prototype, tuple):
            prototype = (prototype,)
        result = []
        generator = abjad.iterate(argument).by_class(prototype)
        components = list(generator)
        if components:
            if trim:
                components = Selection._trim_subresult(components, trim)
            if head is not None:
                components = Selection._head_filter_subresult(components, head)
            if tail is not None:
                components = Selection._tail_filter_subresult(components, tail)
            result.extend(components)
        return class_(result)

    @staticmethod
    def _check(items):
        import abjad
        for item in items:
            if not isinstance(item, (abjad.Component, abjad.Selection)):
                message = 'components / selections only: {!r}.'
                message = message.format(items)
                raise TypeError(message)

    def _copy(self, n=1, include_enclosing_containers=False):
        r'''Copies components in selection and fractures crossing spanners.

        Selection must be logical-voice-contiguous components.

        The steps this function takes are as follows:

            * Deep copy components in selection.

            * Deep copy spanners that attach to any component in selection.

            * Fracture spanners that attach to components not in selection.

            * Returns Python list of copied components.

        ..  container:: example

            Copy components one time:

            >>> staff = abjad.Staff(r"c'8 ( d'8 e'8 f'8 )")
            >>> staff.extend(r"g'8 a'8 b'8 c''8")
            >>> time_signature = abjad.TimeSignature((2, 4))
            >>> abjad.attach(time_signature, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    \time 2/4
                    c'8 (
                    d'8
                    e'8
                    f'8 )
                    g'8
                    a'8
                    b'8
                    c''8
                }

            >>> selection = staff[2:4]
            >>> result = selection._copy()
            >>> new_staff = abjad.Staff(result)
            >>> abjad.show(new_staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(new_staff)
                \new Staff {
                    e'8 (
                    f'8 )
                }

            >>> staff[2] is new_staff[0]
            False

        ..  container:: example

            Copy components multiple times:

            Copy components a total of `n` times:

            >>> selection = staff[2:4]
            >>> result = selection._copy(n=4)
            >>> new_staff = abjad.Staff(result)
            >>> abjad.show(new_staff) # doctest: +SKIP

            >>> abjad.f(new_staff)
            \new Staff {
                e'8 (
                f'8 )
                e'8 (
                f'8 )
                e'8 (
                f'8 )
                e'8 (
                f'8 )
            }

        ..  container:: example

            Copy leaves and include enclosing conatiners:

            >>> voice = abjad.Voice(r"\times 2/3 { c'4 d'4 e'4 }")
            >>> voice.append(r"\times 2/3 { f'4 e'4 d'4 }")
            >>> staff = abjad.Staff([voice])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    \new Voice {
                        \times 2/3 {
                            c'4
                            d'4
                            e'4
                        }
                        \times 2/3 {
                            f'4
                            e'4
                            d'4
                        }
                    }
                }

            >>> leaves = abjad.select(staff).by_leaf()[1:5]
            >>> new_staff = leaves._copy(include_enclosing_containers=True)
            >>> abjad.show(new_staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(new_staff)
                \new Staff {
                    \new Voice {
                        \tweak edge-height #'(0.7 . 0)
                        \times 2/3 {
                            d'4
                            e'4
                        }
                        \tweak edge-height #'(0.7 . 0)
                        \times 2/3 {
                            f'4
                            e'4
                        }
                    }
                }

        Returns contiguous selection.
        '''
        import abjad
        # check input
        assert self.in_contiguous_logical_voice()
        # return empty list when nothing to copy
        if n < 1:
            return []
        new_components = [
            component._copy_with_children_and_indicators_but_without_spanners()
            for component in self
            ]
        if include_enclosing_containers:
            return self._copy_and_include_enclosing_containers()
        new_components = type(self)(new_components)
        # make schema of spanners contained by components
        schema = self._make_spanner_schema()
        # copy spanners covered by components
        for covered_spanner, component_indices in list(schema.items()):
            new_covered_spanner = copy.copy(covered_spanner)
            del(schema[covered_spanner])
            schema[new_covered_spanner] = component_indices
        # reverse schema
        reversed_schema = {}
        for new_covered_spanner, component_indices in list(schema.items()):
            for component_index in component_indices:
                try:
                    reversed_schema[component_index].append(
                        new_covered_spanner)
                except KeyError:
                    reversed_schema[component_index] = [new_covered_spanner]
        # iterate components and add new components to new spanners
        for component_index, new_component in enumerate(
            abjad.iterate(new_components).by_class()):
            try:
                new_covered_spanners = reversed_schema[component_index]
                for new_covered_spanner in new_covered_spanners:
                    new_covered_spanner._append(new_component)
            except KeyError:
                pass
        # repeat as specified by input
        for i in range(n - 1):
            new_components += self._copy()
        # return new components
        return new_components

    def _copy_and_include_enclosing_containers(self):
        import abjad
        assert self.in_contiguous_logical_voice()
        # get governor
        parentage = self[0]._get_parentage(include_self=True)
        governor = parentage._get_governor()
        # find start and stop indices in governor
        governor_leaves = abjad.select(governor).by_leaf()
        for i, x in enumerate(governor_leaves):
            if x is self[0]:
                start_index_in_governor = i
        for i, x in enumerate(governor_leaves):
            if x is self[-1]:
                stop_index_in_governor = i
        # copy governor
        governor_copy = abjad.mutate(governor).copy()
        copied_leaves = abjad.select(governor_copy).by_leaf()
        # find start and stop leaves in copy of governor
        start_leaf = copied_leaves[start_index_in_governor]
        stop_leaf = copied_leaves[stop_index_in_governor]
        # trim governor copy forwards from first leaf
        found_start_leaf = False
        while not found_start_leaf:
            leaf = next(abjad.iterate(governor_copy).by_leaf())
            if leaf is start_leaf:
                found_start_leaf = True
            else:
                leaf._remove_and_shrink_durated_parent_containers()
        # trim governor copy backwards from last leaf
        found_stop_leaf = False
        while not found_stop_leaf:
            reverse_iterator = abjad.iterate(
                governor_copy).by_leaf(reverse=True)
            leaf = next(reverse_iterator)
            if leaf is stop_leaf:
                found_stop_leaf = True
            else:
                leaf._remove_and_shrink_durated_parent_containers()
        # return trimmed governor copy
        return governor_copy

    def _fuse(self):
        import abjad
        assert self.in_contiguous_logical_voice()
        if self.are_leaves():
            return self._fuse_leaves()
        elif all(isinstance(_, abjad.Tuplet) for _ in self):
            return self._fuse_tuplets()
        elif all(isinstance(_, abjad.Measure) for _ in self):
            return self._fuse_measures()
        else:
            message = 'can not fuse.'
            raise Exception(message)

    def _fuse_leaves(self):
        import abjad
        assert self.are_leaves()
        assert self.in_contiguous_logical_voice()
        leaves = self
        if len(leaves) <= 1:
            return leaves
        total_preprolated = leaves._get_preprolated_duration()
        for leaf in leaves[1:]:
            parent = leaf._parent
            if parent:
                index = parent.index(leaf)
                del(parent[index])
        return leaves[0]._set_duration(total_preprolated)

    def _fuse_measures(self):
        import abjad
        assert self.in_same_parent(prototype=abjad.Measure)
        if len(self) == 0:
            return None
        # TODO: instantiate a new measure
        #       instead of returning a reference to existing measure
        if len(self) == 1:
            return self[0]
        implicit_scaling = self[0].implicit_scaling
        assert all(
            x.implicit_scaling == implicit_scaling for x in self)
        selection = abjad.select(self)
        parent, start, stop = selection._get_parent_and_start_stop_indices()
        old_denominators = []
        new_duration = abjad.Duration(0)
        for measure in self:
            effective_time_signature = measure.time_signature
            old_denominators.append(effective_time_signature.denominator)
            new_duration += effective_time_signature.duration
        new_time_signature = measure._duration_to_time_signature(
            new_duration,
            old_denominators,
            )
        components = []
        for measure in self:
            # scale before reassignment to prevent logical tie scale drama
            signature = measure.time_signature
            prolation = signature.implied_prolation
            multiplier = prolation / new_time_signature.implied_prolation
            measure._scale_contents(multiplier)
            measure_components = measure[:]
            measure_components._set_parents(None)
            components += measure_components
        new_measure = abjad.Measure(new_time_signature, components)
        new_measure.implicit_scaling = self[0].implicit_scaling
        if parent is not None:
            self._give_dominant_spanners([new_measure])
        self._set_parents(None)
        if parent is not None:
            parent.insert(start, new_measure)
        return new_measure

    def _fuse_tuplets(self):
        import abjad
        assert self.in_same_parent(prototype=abjad.Tuplet)
        if len(self) == 0:
            return None
        first = self[0]
        first_multiplier = first.multiplier
        first_type = type(first)
        for tuplet in self[1:]:
            if tuplet.multiplier != first_multiplier:
                message = 'tuplets must carry same multiplier.'
                raise ValueError(message)
            if type(tuplet) != first_type:
                message = 'tuplets must be same type.'
                raise TypeError(message)
        assert isinstance(first, abjad.Tuplet)
        new_tuplet = abjad.Tuplet(first_multiplier, [])
        wrapped = False
        if (self[0]._get_parentage().root is not
            self[-1]._get_parentage().root):
            dummy_container = abjad.Container(self)
            wrapped = True
        abjad.mutate(self).swap(new_tuplet)
        if wrapped:
            del(dummy_container[:])
        return new_tuplet

    def _get_component(self, prototype=None, n=0, recurse=True):
        import abjad
        prototype = prototype or (abjad.Component,)
        if not isinstance(prototype, tuple):
            prototype = (prototype,)
        if 0 <= n:
            if recurse:
                components = abjad.iterate(self).by_class(prototype)
            else:
                components = self.items
            for i, x in enumerate(components):
                if i == n:
                    return x
        else:
            if recurse:
                components = abjad.iterate(self).by_class(
                    prototype, reverse=True)
            else:
                components = reversed(self.items)
            for i, x in enumerate(components):
                if i == abs(n) - 1:
                    return x

    def _get_crossing_spanners(self):
        r'''Assert logical-voice-contiguous components.
        Collect spanners that attach to any component in selection.
        Returns unordered set of crossing spanners.
        A spanner P crosses a list of logical-voice-contiguous components C
        when P and C share at least one component and when it is the
        case that NOT ALL of the components in P are also in C.
        In other words, there is some intersection -- but not total
        intersection -- between the components of P and C.
        '''
        import abjad
        assert self.in_contiguous_logical_voice()
        all_components = set(abjad.iterate(self).by_class())
        contained_spanners = set()
        for component in abjad.iterate(self).by_class():
            contained_spanners.update(component._get_spanners())
        crossing_spanners = set([])
        for spanner in contained_spanners:
            spanner_components = set(spanner[:])
            if not spanner_components.issubset(all_components):
                crossing_spanners.add(spanner)
        return crossing_spanners

    def _get_dominant_spanners(self):
        r'''Returns spanners that dominate components in selection.
        Returns set of (spanner, index) pairs.
        Each (spanner, index) pair gives a spanner which dominates
        all components in selection together with the start index
        at which spanner first encounters selection.
        Use this helper to lift spanners temporarily from components
        in selection and perform some action to the underlying
        score tree before reattaching spanners.
        score components.
        '''
        assert self.in_contiguous_logical_voice()
        receipt = set([])
        if len(self) == 0:
            return receipt
        first, last = self[0], self[-1]
        start_components = first._get_descendants_starting_with()
        stop_components = last._get_descendants_stopping_with()
        stop_components = set(stop_components)
        for component in start_components:
            for spanner in component._get_spanners():
                if set(spanner[:]) & stop_components != set([]):
                    index = spanner._index(component)
                    receipt.add((spanner, index))
        return receipt

    def _get_format_specification(self):
        import abjad
        values = []
        if self.items:
            values = [list(self.items)]
        return abjad.FormatSpecification(
            client=self,
            storage_format_args_values=values,
            )

    def _get_offset_lists(self):
        start_offsets, stop_offsets = [], []
        for component in self:
            start_offsets.append(component._get_timespan().start_offset)
            stop_offsets.append(component._get_timespan().stop_offset)
        return start_offsets, stop_offsets

    def _get_parent_and_start_stop_indices(self):
        assert self.in_same_parent()
        if self:
            first, last = self[0], self[-1]
            parent = first._parent
            if parent is not None:
                first_index = parent.index(first)
                last_index = parent.index(last)
                return parent, first_index, last_index
        return None, None, None

    def _get_preprolated_duration(self):
        return sum(component._get_preprolated_duration() for component in self)

    def _get_spanner(self, prototype=None):
        spanners = self._get_spanners(prototype=prototype)
        if not spanners:
            message = 'no spanners found.'
            raise MissingSpannerError(message)
        elif len(spanners) == 1:
            return spanners.pop()
        else:
            message = 'multiple spanners found.'
            raise ExtraSpannerError(message)

    def _get_spanners(self, prototype=None):
        from abjad.tools import spannertools
        prototype = prototype or (spannertools.Spanner,)
        if not isinstance(prototype, tuple):
            prototype = (prototype, )
        assert isinstance(prototype, tuple)
        result = set()
        for component in self:
            spanners = component._get_spanners(prototype)
            result.update(spanners)
        return result

    def _get_timespan(self, in_seconds=False):
        import abjad
        if len(self):
            timespan_ = self[0]._get_timespan(in_seconds=in_seconds)
            start_offset = timespan_.start_offset
            timespan_ = self[-1]._get_timespan(in_seconds=in_seconds)
            stop_offset = timespan_.stop_offset
        else:
            start_offset = abjad.Duration(0)
            stop_offset = abjad.Duration(0)
        return abjad.Timespan(
            start_offset=start_offset,
            stop_offset=stop_offset,
            )

    def _give_dominant_spanners(self, recipients):
        r'''Find all spanners dominating components.
        Insert each component in recipients into each dominant spanner.
        Remove components from each dominating spanner.
        Returns none.
        Not composer-safe.
        '''
        import abjad
        assert self.in_contiguous_logical_voice()
        assert abjad.select(recipients).in_contiguous_logical_voice()
        receipt = self._get_dominant_spanners()
        for spanner, index in receipt:
            for recipient in reversed(recipients):
                spanner._insert(index, recipient)
            for component in self:
                spanner._remove(component)

    def _give_components_to_empty_container(self, container):
        r'''Not composer-safe.
        '''
        import abjad
        assert self.in_same_parent()
        assert isinstance(container, abjad.Container)
        assert not container
        components = []
        for component in self:
            components.extend(getattr(component, 'components', ()))
        container._components.extend(components)
        container[:]._set_parents(container)

    def _give_position_in_parent_to_container(self, container):
        r'''Not composer-safe.
        '''
        import abjad
        assert self.in_same_parent()
        assert isinstance(container, abjad.Container)
        parent, start, stop = self._get_parent_and_start_stop_indices()
        if parent is not None:
            parent._components.__setitem__(slice(start, start), [container])
            container._set_parent(parent)
            self._set_parents(None)

    @staticmethod
    def _head_filter_subresult(result, head):
        import abjad
        result_ = []
        for item in result:
            if isinstance(item, abjad.Component):
                logical_tie = abjad.inspect(item).get_logical_tie()
                if head == (item is logical_tie.head):
                    result_.append(item)
                else:
                    pass
            elif isinstance(item, abjad.Selection):
                if not all(isinstance(_, abjad.Component) for _ in item):
                    raise NotImplementedError(item)
                selection = []
                for component in item:
                    logical_tie = abjad.inspect(component).get_logical_tie()
                    if head == logical_tie.head:
                        selection.append(item)
                    else:
                        pass
                selection = abjad.select(selection)
                result_.append(selection)
            else:
                raise TypeError(item)
        assert isinstance(result_, list), repr(result_)
        return abjad.select(result_)

    def _iterate_components(self, recurse=True, reverse=False):
        import abjad
        if recurse:
            return abjad.iterate(self).by_class()
        else:
            return self._iterate_top_level_components(reverse=reverse)

    def _iterate_top_level_components(self, reverse=False):
        if reverse:
            for component in reversed(self):
                yield component
        else:
            for component in self:
                yield component

    def _make_spanner_schema(self):
        import abjad
        schema = {}
        spanners = set()
        for component in abjad.iterate(self).by_class():
            spanners.update(component._get_spanners())
        for spanner in spanners:
            schema[spanner] = []
        for i, component in enumerate(abjad.iterate(self).by_class()):
            attached_spanners = component._get_spanners()
            for attached_spanner in attached_spanners:
                try:
                    schema[attached_spanner].append(i)
                except KeyError:
                    pass
        return schema

    def _set_parents(self, new_parent):
        r'''Not composer-safe.
        '''
        for component in self.items:
            component._set_parent(new_parent)

    @staticmethod
    def _tail_filter_subresult(result, tail):
        import abjad
        result_ = []
        for item in result:
            if isinstance(item, abjad.Component):
                logical_tie = abjad.inspect(item).get_logical_tie()
                if tail == (item is logical_tie.tail):
                    result_.append(item)
                else:
                    pass
            elif isinstance(item, abjad.Selection):
                if not all(isinstance(_, abjad.Component) for _ in item):
                    raise NotImplementedError(item)
                selection = []
                for component in item:
                    logical_tie = abjad.inspect(component).get_logical_tie()
                    if tail == logical_tie.tail:
                        selection.append(item)
                    else:
                        pass
                selection = abjad.select(selection)
                result_.append(selection)
            else:
                raise TypeError(item)
        assert isinstance(result_, list), repr(result_)
        return abjad.select(result_)

    @staticmethod
    def _trim_subresult(result, trim):
        import abjad
        if trim is True:
            trim = (abjad.MultimeasureRest, abjad.Rest, abjad.Skip)
        result_ = []
        found_good_component = False
        for item in result:
            if isinstance(item, abjad.Component):
                if not isinstance(item, trim):
                    found_good_component = True
            elif isinstance(item, abjad.Selection):
                if not all(isinstance(_, abjad.Component) for _ in item):
                    raise NotImplementedError(item)
                selection = []
                for component in item:
                    if not isinstance(component, trim):
                        found_good_component = True
                    if found_good_component:
                        selection.append(component)
                item = abjad.select(selection)
            else:
                raise TypeError(item)
            if found_good_component:
                result_.append(item)
        result__ = []
        found_good_component = False
        for item in reversed(result_):
            if isinstance(item, abjad.Component):
                if not isinstance(item, trim):
                    found_good_component = True
            elif isinstance(item, abjad.Selection):
                if not all(isinstance(_, abjad.Component) for _ in item):
                    raise NotImplementedError(item)
                selection = []
                for component in reversed(item):
                    if not isinstance(component, trim):
                        found_good_component = True
                    if found_good_component:
                        selection.insert(0, component)
                item = abjad.select(selection)
            else:
                raise TypeError(item)
            if found_good_component:
                result__.insert(0, item)
        assert isinstance(result__, list), repr(result__)
        result = abjad.select(result__)
        return result

    def _update_expression(
        self,
        frame,
        evaluation_template=None,
        map_operand=None,
        ):
        import abjad
        callback = abjad.Expression._frame_to_callback(
            frame,
            evaluation_template=evaluation_template,
            map_operand=map_operand,
            )
        return self._expression.append_callback(callback)

    def _withdraw_from_crossing_spanners(self):
        r'''Not composer-safe.
        '''
        import abjad
        assert self.in_contiguous_logical_voice()
        crossing_spanners = self._get_crossing_spanners()
        components_including_children = abjad.select(self).by_class()
        for crossing_spanner in list(crossing_spanners):
            spanner_components = crossing_spanner.leaves[:]
            for component in components_including_children:
                if component in spanner_components:
                    crossing_spanner._leaves.remove(component)
                    component._spanners.discard(crossing_spanner)

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        r'''Gets items.

        ..  container:: example

            >>> abjad.Staff("c'4 d'4 e'4 f'4")[:].items
            (Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4"))

        Returns tuple of items (components and / or other selections).
        '''
        return self._items

    ### PUBLIC METHODS ###

    def are_leaves(self):
        r'''Is true when components are all leaves.

        ..  container:: example

            >>> abjad.Staff("c'4 d'4 e'4 f'4")[:].are_leaves()
            True

        Returns true or false.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return all(isinstance(_, abjad.Leaf) for _ in self)

    def by_class(
        self,
        prototype=None,
        reverse=False,
        start=0,
        stop=None,
        with_grace_notes=True,
        ):
        r'''Select components by class.

        ..  container:: example

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.Measure((2, 8), "c'8 d'8"))
            >>> staff.append(abjad.Measure((2, 8), "e'8 f'8"))
            >>> staff.append(abjad.Measure((2, 8), "g'8 a'8"))
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    {
                        \time 2/8
                        c'8
                        d'8
                    }
                    {
                        e'8
                        f'8
                    }
                    {
                        g'8
                        a'8
                    }
                }

            >>> for note in abjad.select(staff).by_class(prototype=abjad.Note):
            ...     note
            ...
            Note("c'8")
            Note("d'8")
            Note("e'8")
            Note("f'8")
            Note("g'8")
            Note("a'8")

        ..  container:: example expression

            Selects notes:

            >>> expression = abjad.select()
            >>> expression = expression.by_class(abjad.Note)

            >>> staff = abjad.Staff("c'4 d'8 ~ d'16 e'16 ~ e'8 r4 g'8")
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'4
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    d'8 ~
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    d'16
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    e'16 ~
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    e'8
                    r4
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    g'8
                }

            >>> expression.print(result)
            Note("c'4")
            Note("d'8")
            Note("d'16")
            Note("e'16")
            Note("e'8")
            Note("g'8")

        Returns new selection.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        generator = abjad.iterate(self).by_class(
            prototype=prototype,
            reverse=reverse,
            start=start,
            stop=stop,
            with_grace_notes=with_grace_notes,
            )
        return type(self)(generator)

    def by_contiguity(self):
        r'''Selects by contiguity.

        ..  container:: example expression

            Selects contiguous groups of sixteenth notes:

            >>> expression = abjad.select()
            >>> expression = expression.by_leaf()
            >>> inequality = abjad.DurationInequality('==', (1, 16))
            >>> expression = expression.filter(inequality)
            >>> expression = expression.select()
            >>> expression = expression.by_contiguity()

            >>> staff = abjad.Staff("c'4 d'16 d' d' d' e'4 f'16 f' f' f'")
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    c'4
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    d'16
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    d'16
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    d'16
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    d'16
                    e'4
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    f'16
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    f'16
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    f'16
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    f'16
                }

            >>> expression.print(result)
            Selection([Note("d'16"), Note("d'16"), Note("d'16"), Note("d'16")])
            Selection([Note("f'16"), Note("f'16"), Note("f'16"), Note("f'16")])

        ..  container:: example expression

            Selects the first leaf in each contiguous group of short-duration
            logical ties:

            >>> inequality = abjad.DurationInequality('<', (1, 4))
            >>> expression = abjad.select().by_logical_tie()
            >>> expression = expression.filter(inequality).by_contiguity()
            >>> expression = expression.map(abjad.select().by_leaf()[0])

            >>> staff = abjad.Staff("c'4 d'8 ~ d'16 e'16 ~ e'8 f'4 g'8")
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    c'4
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    d'8 ~
                    d'16
                    e'16 ~
                    e'8
                    f'4
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    g'8
                }

            >>> expression.print(result)
            Note("d'8")
            Note("g'8")

        ..  container:: example expression

            Selects contiguous groups of sixteenth notes:

            >>> expression = abjad.select()
            >>> expression = expression.by_leaf()
            >>> inequality = abjad.DurationInequality('==', (1, 16))
            >>> expression = expression.filter(inequality).select()
            >>> expression = expression.by_contiguity()

            >>> staff = abjad.Staff("c'4 d'16 d' d' d' e'4 f'16 f' f' f'")
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    c'4
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    d'16
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    d'16
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    d'16
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    d'16
                    e'4
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    f'16
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    f'16
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    f'16
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    f'16
                }

            >>> expression.print(result)
            Selection([Note("d'16"), Note("d'16"), Note("d'16"), Note("d'16")])
            Selection([Note("f'16"), Note("f'16"), Note("f'16"), Note("f'16")])

        ..  container:: example expression

            Groups pitched leaves by pitch and then contiguity:

            >>> expression = abjad.select().by_leaf(pitched=True)
            >>> expression = expression.group(abjad.select().get_pitch_set())
            >>> expression = expression.map(abjad.select().by_contiguity())
            >>> expression = expression.flatten(depth=1)

            >>> staff = abjad.Staff(r"""
            ...     c'8 ~ c'16 c'16 r8 c'16 c'16
            ...     d'8 ~ d'16 d'16 r8 d'16 d'16
            ...     """)
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'8 ~
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'16
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'16
                    r8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    c'16
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    c'16
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    d'8 ~
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    d'16
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    d'16
                    r8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    d'16
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    d'16
                }

            >>> expression.print(result)
            Selection([Note("c'8"), Note("c'16"), Note("c'16")])
            Selection([Note("c'16"), Note("c'16")])
            Selection([Note("d'8"), Note("d'16"), Note("d'16")])
            Selection([Note("d'16"), Note("d'16")])

            ..  container:: example expression

                Groups pitched logical ties by contiguity and then pitch:

                >>> expression = abjad.select().by_logical_tie(pitched=True)
                >>> expression = expression.by_contiguity()
                >>> get = abjad.select().group(abjad.select().get_pitch_set())
                >>> expression = expression.map(get)
                >>> expression = expression.flatten(depth=1)

                >>> staff = abjad.Staff(r"""
                ...     c'8 ~ c'16 c'16 r8 c'16 c'16
                ...     d'8 ~ d'16 d'16 r8 d'16 d'16
                ...     """)
                >>> result = expression(staff)
                >>> expression.color(result)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff \with {
                        autoBeaming = ##f
                    } {
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        c'8 ~
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        c'16
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        c'16
                        r8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        c'16
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        c'16
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        d'8 ~
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        d'16
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        d'16
                        r8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        d'16
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        d'16
                    }

                >>> expression.print(result)
                Selection([LogicalTie([Note("c'8"), Note("c'16")]), LogicalTie([Note("c'16")])])
                Selection([LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")])])
                Selection([LogicalTie([Note("d'8"), Note("d'16")]), LogicalTie([Note("d'16")])])
                Selection([LogicalTie([Note("d'16")]), LogicalTie([Note("d'16")])])

        Returns new expression.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        selections, selection = [], []
        selection.extend(self[:1])
        for item in self[1:]:
            try:
                this_timespan = selection[-1]._get_timespan()
            except AttributeError:
                this_timespan = selection[-1].get_timespan()
            try:
                that_timespan = item._get_timespan()
            except AttributeError:
                that_timespan = item.get_timespan()
            if this_timespan.stop_offset == that_timespan.start_offset:
                selection.append(item)
            else:
                selections.append(type(self)(selection))
                selection = [item]
        if selection:
            selections.append(type(self)(selection))
        return type(self)(selections)

    def by_leaf(
        self,
        prototype=None,
        head=None,
        pitched=None,
        reverse=False,
        start=0,
        stop=None,
        tail=None,
        trim=None,
        with_grace_notes=True,
        ):
        r'''Select components by leaf.

        ..  container:: example

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.Measure((2, 8), "<c' bf'>8 <g' a'>8"))
            >>> staff.append(abjad.Measure((2, 8), "af'8 r8"))
            >>> staff.append(abjad.Measure((2, 8), "r8 gf'8"))
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    {
                        \time 2/8
                        <c' bf'>8
                        <g' a'>8
                    }
                    {
                        af'8
                        r8
                    }
                    {
                        r8
                        gf'8
                    }
                }

            >>> for leaf in abjad.select(staff).by_leaf():
            ...     leaf
            ...
            Chord("<c' bf'>8")
            Chord("<g' a'>8")
            Note("af'8")
            Rest('r8')
            Rest('r8')
            Note("gf'8")

        ..  container:: example expression

            Selects leaves:

            >>> expression = abjad.select()
            >>> expression = expression.by_leaf()

            >>> staff = abjad.Staff(r"""
            ...     \times 2/3 { r8 d' e' } f' r
            ...     r f' \times 2/3 { e' d' r8 }
            ...     """)
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \times 2/3 {
                        \once \override Dots.color = #red
                        \once \override Rest.color = #red
                        r8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        d'8
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        e'8
                    }
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    f'8
                    \once \override Dots.color = #red
                    \once \override Rest.color = #red
                    r8
                    \once \override Dots.color = #blue
                    \once \override Rest.color = #blue
                    r8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    f'8
                    \times 2/3 {
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        e'8
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        d'8
                        \once \override Dots.color = #blue
                        \once \override Rest.color = #blue
                        r8
                    }
                }

            >>> expression.print(result)
            Rest('r8')
            Note("d'8")
            Note("e'8")
            Note("f'8")
            Rest('r8')
            Rest('r8')
            Note("f'8")
            Note("e'8")
            Note("d'8")
            Rest('r8')

        ..  container:: example expression

            Selects pitched leaves:

            >>> expression = abjad.select()
            >>> expression = expression.by_leaf(pitched=True)
            >>> selection = expression(staff)

            >>> staff = abjad.Staff(r"""
            ...     \times 2/3 { r8 d' e' } f' r
            ...     r f' \times 2/3 { e' d' r8 }
            ...     """)
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \times 2/3 {
                        r8
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        d'8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        e'8
                    }
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    f'8
                    r8
                    r8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    f'8
                    \times 2/3 {
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        e'8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        d'8
                        r8
                    }
                }

            >>> expression.print(result)
            Note("d'8")
            Note("e'8")
            Note("f'8")
            Note("f'8")
            Note("e'8")
            Note("d'8")

        ..  container:: example expression

            Selects trimmed leaves:

            >>> expression = abjad.select()
            >>> expression = expression.by_leaf(trim=True)

            >>> staff = abjad.Staff(r"""
            ...     \times 2/3 { r8 d' e' } f' r
            ...     r f' \times 2/3 { e' d' r8 }
            ...     """)
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \times 2/3 {
                        r8
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        d'8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        e'8
                    }
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    f'8
                    \once \override Dots.color = #blue
                    \once \override Rest.color = #blue
                    r8
                    \once \override Dots.color = #red
                    \once \override Rest.color = #red
                    r8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    f'8
                    \times 2/3 {
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        e'8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        d'8
                        r8
                    }
                }

            >>> expression.print(result)
            Note("d'8")
            Note("e'8")
            Note("f'8")
            Rest('r8')
            Rest('r8')
            Note("f'8")
            Note("e'8")
            Note("d'8")

            Use trimmed leaves with ottava spanners:

            >>> abjad.attach(abjad.OctavationSpanner(), result)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \times 2/3 {
                        r8
                        \ottava #1
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        d'8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        e'8
                    }
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    f'8
                    \once \override Dots.color = #blue
                    \once \override Rest.color = #blue
                    r8
                    \once \override Dots.color = #red
                    \once \override Rest.color = #red
                    r8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    f'8
                    \times 2/3 {
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        e'8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        d'8
                        \ottava #0
                        r8
                    }
                }

            Regression: selects trimmed leaves (even when there are no rests to
            trim):

            >>> expression = abjad.select()
            >>> expression = expression.by_leaf(trim=True)

            >>> staff = abjad.Staff(r"""
            ...     \times 2/3 { c'8 d' e' } f' r
            ...     r f' \times 2/3 { e' d' c' }
            ...     """)
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \times 2/3 {
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        c'8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        d'8
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        e'8
                    }
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    f'8
                    \once \override Dots.color = #red
                    \once \override Rest.color = #red
                    r8
                    \once \override Dots.color = #blue
                    \once \override Rest.color = #blue
                    r8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    f'8
                    \times 2/3 {
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        e'8
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        d'8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        c'8
                    }
                }

            >>> expression.print(result)
            Note("c'8")
            Note("d'8")
            Note("e'8")
            Note("f'8")
            Rest('r8')
            Rest('r8')
            Note("f'8")
            Note("e'8")
            Note("d'8")
            Note("c'8")

        ..  container:: example expression

            Selects leaves in tuplets:

            >>> expression = abjad.select()
            >>> expression = expression.by_class(abjad.Tuplet)
            >>> expression = expression.by_leaf()

            >>> staff = abjad.Staff(r"""
            ...     \times 2/3 { r8 d' e' } f' r
            ...     r f' \times 2/3 { e' d' r8 }
            ...     """)
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \times 2/3 {
                        \once \override Dots.color = #red
                        \once \override Rest.color = #red
                        r8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        d'8
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        e'8
                    }
                    f'8
                    r8
                    r8
                    f'8
                    \times 2/3 {
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        e'8
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        d'8
                        \once \override Dots.color = #blue
                        \once \override Rest.color = #blue
                        r8
                    }
                }

            >>> expression.print(result)
            Rest('r8')
            Note("d'8")
            Note("e'8")
            Note("e'8")
            Note("d'8")
            Rest('r8')

            Selects trimmed leaves in tuplets:

            >>> expression = abjad.select()
            >>> expression = expression.by_class(abjad.Tuplet)
            >>> expression = expression.by_leaf(trim=True)

            >>> staff = abjad.Staff(r"""
            ...     \times 2/3 { r8 d' e' } f' r
            ...     r f' \times 2/3 { e' d' r8 }
            ...     """)
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \times 2/3 {
                        r8
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        d'8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        e'8
                    }
                    f'8
                    r8
                    r8
                    f'8
                    \times 2/3 {
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        e'8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        d'8
                        r8
                    }
                }

            >>> expression.print(result)
            Note("d'8")
            Note("e'8")
            Note("e'8")
            Note("d'8")

        ..  container:: example expression

            Selects pitched heads in tuplets.

            This is the correct selection for most articulations:

            >>> expression = abjad.select()
            >>> expression = expression.by_class(abjad.Tuplet)
            >>> expression = expression.by_leaf(head=True, pitched=True)

            >>> staff = abjad.Staff(r"""
            ...     \times 2/3 { c'8 d' ~ d' } e' r
            ...     r e' \times 2/3 { d' ~ d' c' }
            ...     """)
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \times 2/3 {
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        c'8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        d'8 ~
                        d'8
                    }
                    e'8
                    r8
                    r8
                    e'8
                    \times 2/3 {
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        d'8 ~
                        d'8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        c'8
                    }
                }

            >>> expression.print(result)
            Note("c'8")
            Note("d'8")
            Note("d'8")
            Note("c'8")

        ..  container:: example expression

            Selects pitched tails in tuplets.

            This is the correct selection for laissez vibrer:

            >>> expression = abjad.select()
            >>> expression = expression.by_class(abjad.Tuplet)
            >>> expression = expression.by_leaf(tail=True, pitched=True)

            >>> staff = abjad.Staff(r"""
            ...     \times 2/3 { c'8 d' ~ d' } e' r
            ...     r e' \times 2/3 { d' ~ d' c' }
            ...     """)
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \times 2/3 {
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        c'8
                        d'8 ~
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        d'8
                    }
                    e'8
                    r8
                    r8
                    e'8
                    \times 2/3 {
                        d'8 ~
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        d'8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        c'8
                    }
                }

            >>> expression.print(result)
            Note("c'8")
            Note("d'8")
            Note("d'8")
            Note("c'8")

        ..  container:: example expression

            Selects chord heads in tuplets.

            This is the correct selection for arpeggios:

            >>> expression = abjad.select()
            >>> expression = expression.by_class(abjad.Tuplet)
            >>> expression = expression.by_leaf(abjad.Chord, head=True)

            >>> staff = abjad.Staff(r"""
            ...     \times 2/3 { <c' e' g'>8 ~ <c' e' g'> d' } e' r
            ...     r <g d' fs'> \times 2/3 { e' <c' d'> ~ <c' d'> }
            ...     """)
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \times 2/3 {
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        <c' e' g'>8 ~
                        <c' e' g'>8
                        d'8
                    }
                    e'8
                    r8
                    r8
                    <g d' fs'>8
                    \times 2/3 {
                        e'8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        <c' d'>8 ~
                        <c' d'>8
                    }
                }

            >>> expression.print(result)
            Chord("<c' e' g'>8")
            Chord("<c' d'>8")

        Returns new selection.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        if pitched:
            prototype = (abjad.Chord, abjad.Note)
        elif prototype is None:
            prototype = abjad.Leaf
        return self._by_class(
            self,
            prototype=prototype,
            head=head,
            tail=tail,
            trim=trim,
            )

    def by_logical_measure(self):
        r'''Selects by logical measure.

        ..  container:: example

            >>> staff = abjad.Staff("c'8 d' e' f' g' a' b' c''")
            >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
            >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
            >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])
            >>> abjad.show(staff) # doctest: +SKIP

        ..  container:: example expression

            Selects the leaves of every logical measure:

            >>> expression = abjad.select()
            >>> expression = expression.by_leaf()
            >>> expression = expression.by_logical_measure()
            >>> for selection in expression(staff):
            ...     selection
            ...
            Selection([Note("c'8"), Note("d'8")])
            Selection([Note("e'8"), Note("f'8")])
            Selection([Note("g'8"), Note("a'8"), Note("b'8")])
            Selection([Note("c''8")])

        ..  container:: example expression

            Selects the first leaf of every logical measure:

            >>> expression = abjad.select()
            >>> expression = expression.by_leaf()
            >>> expression = expression.by_logical_measure()
            >>> expression = expression.map(abjad.select()[0])
            >>> expression(staff)
            Selection([Note("c'8"), Note("e'8"), Note("g'8"), Note("c''8")])

        ..  container:: example expression

            Selects the last leaf of every logical measure:

            >>> expression = abjad.select()
            >>> expression = expression.by_leaf()
            >>> expression = expression.by_logical_measure()
            >>> expression = expression.map(abjad.select()[-1])
            >>> expression(staff)
            Selection([Note("d'8"), Note("f'8"), Note("b'8"), Note("c''8")])

        ..  container:: example

            Works with implicit time signatures:

            >>> staff = abjad.Staff("c'4 d' e' f' g' a' b' c''")
            >>> score = abjad.Score([staff])
            >>> scheme = abjad.SchemeMoment((1, 16))
            >>> abjad.setting(score).proportional_notation_duration = scheme
            >>> abjad.show(score) # doctest: +SKIP

            >>> expression = abjad.select()
            >>> expression = expression.by_leaf()
            >>> expression = expression.by_logical_measure()
            >>> for selection in expression(score):
            ...     selection
            ...
            Selection([Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4")])
            Selection([Note("g'4"), Note("a'4"), Note("b'4"), Note("c''4")])

        Returns new expression.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        def _get_first_component(argument):
            if isinstance(argument, abjad.Component):
                return argument
            else:
                component = argument[0]
                assert isinstance(component, abjad.Component)
                return component
        def _get_logical_measure_number(argument):
            first_component = _get_first_component(argument)
            assert first_component._logical_measure_number is not None
            return first_component._logical_measure_number
        selections = []
        first_component = _get_first_component(self)
        first_component._update_logical_measure_numbers()
        pairs = itertools.groupby(self, _get_logical_measure_number)
        for value, group in pairs:
            selection = type(self)(group)
            selections.append(selection)
        return type(self)(selections)

    def by_logical_tie(
        self,
        nontrivial=False,
        pitched=False,
        reverse=False,
        with_grace_notes=True,
        ):
        r'''Select components by logical tie.

        ..  container:: example

            >>> string = r"c'4 ~ \times 2/3 { c'16 d'8 } e'8 f'4 ~ f'16"
            >>> staff = abjad.Staff(string)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    c'4 ~
                    \times 2/3 {
                        c'16
                        d'8
                    }
                    e'8
                    f'4 ~
                    f'16
                }

            >>> for logical_tie in abjad.select(staff).by_logical_tie():
            ...     logical_tie
            ...
            LogicalTie([Note("c'4"), Note("c'16")])
            LogicalTie([Note("d'8")])
            LogicalTie([Note("e'8")])
            LogicalTie([Note("f'4"), Note("f'16")])

        ..  container:: example expression

            Selects logical ties:

            >>> expression = abjad.select()
            >>> expression = expression.by_logical_tie()

            >>> staff = abjad.Staff("c'8 d' ~ { d' e' r f'~ } f' r")
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    d'8 ~
                    {
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        d'8
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        e'8
                        \once \override Dots.color = #blue
                        \once \override Rest.color = #blue
                        r8
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        f'8 ~
                    }
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    f'8
                    \once \override Dots.color = #blue
                    \once \override Rest.color = #blue
                    r8
                }

            >>> expression.print(result)
            LogicalTie([Note("c'8")])
            LogicalTie([Note("d'8"), Note("d'8")])
            LogicalTie([Note("e'8")])
            LogicalTie([Rest('r8')])
            LogicalTie([Note("f'8"), Note("f'8")])
            LogicalTie([Rest('r8')])

        ..  container:: example expression

            Selects pitched logical ties:

            >>> expression = abjad.select()
            >>> expression = expression.by_logical_tie(pitched=True)

            >>> staff = abjad.Staff("c'8 d' ~ { d' e' r f'~ } f' r")
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    d'8 ~
                    {
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        d'8
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        e'8
                        r8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        f'8 ~
                    }
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    f'8
                    r8
                }

            >>> expression.print(result)
            LogicalTie([Note("c'8")])
            LogicalTie([Note("d'8"), Note("d'8")])
            LogicalTie([Note("e'8")])
            LogicalTie([Note("f'8"), Note("f'8")])

        ..  container:: example expression

            Selects pitched nontrivial logical ties:

            >>> expression = abjad.select()
            >>> expression = expression.by_logical_tie(
            ...     pitched=True,
            ...     nontrivial=True,
            ...     )

            >>> staff = abjad.Staff("c'8 d' ~ { d' e' r f'~ } f' r")
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    c'8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    d'8 ~
                    {
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        d'8
                        e'8
                        r8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        f'8 ~
                    }
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    f'8
                    r8
                }

            >>> expression.print(result)
            LogicalTie([Note("d'8"), Note("d'8")])
            LogicalTie([Note("f'8"), Note("f'8")])

        ..  container:: example expression

            Selects pitched logical ties (starting) in each tuplet:

            >>> expression = abjad.select()
            >>> expression = expression.by_class(abjad.Tuplet)
            >>> get = abjad.select().by_logical_tie(pitched=True)
            >>> expression = expression.map(get)

            >>> staff = abjad.Staff(r"""
            ...     \times 2/3 { c'8 d' e'  ~ } e' f' ~
            ...     \times 2/3 { f' g' a' ~ } a' b' ~
            ...     \times 2/3 { b' c'' d'' }
            ...     """)
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \times 2/3 {
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        c'8
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        d'8
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        e'8 ~
                    }
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    e'8
                    f'8 ~
                    \times 2/3 {
                        f'8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        g'8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        a'8 ~
                    }
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    a'8
                    b'8 ~
                    \times 2/3 {
                        b'8
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        c''8
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        d''8
                    }
                }

            >>> expression.print(result)
            Selection([LogicalTie([Note("c'8")]), LogicalTie([Note("d'8")]), LogicalTie([Note("e'8"), Note("e'8")])])
            Selection([LogicalTie([Note("g'8")]), LogicalTie([Note("a'8"), Note("a'8")])])
            Selection([LogicalTie([Note("c''8")]), LogicalTie([Note("d''8")])])

        ..  container:: example expression

            Selects pitched logical ties (starting) in each of the last two
            tuplets:

            >>> expression = abjad.select()
            >>> expression = expression.by_class(prototype=abjad.Tuplet)
            >>> expression = expression[-2:]
            >>> get = abjad.select().by_logical_tie(pitched=True)
            >>> expression = expression.map(get)

            >>> staff = abjad.Staff(r"""
            ...     \times 2/3 { c'8 d' e'  ~ } e' f' ~
            ...     \times 2/3 { f' g' a' ~ } a' b' ~
            ...     \times 2/3 { b' c'' d'' }
            ...     """)
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \times 2/3 {
                        c'8
                        d'8
                        e'8 ~
                    }
                    e'8
                    f'8 ~
                    \times 2/3 {
                        f'8
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        g'8
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        a'8 ~
                    }
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    a'8
                    b'8 ~
                    \times 2/3 {
                        b'8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        c''8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        d''8
                    }
                }

            >>> expression.print(result)
            Selection([LogicalTie([Note("g'8")]), LogicalTie([Note("a'8"), Note("a'8")])])
            Selection([LogicalTie([Note("c''8")]), LogicalTie([Note("d''8")])])

        Returns new selection.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        generator = abjad.iterate(self).by_logical_tie(
            nontrivial=nontrivial,
            pitched=pitched,
            reverse=reverse,
            with_grace_notes=with_grace_notes,
            )
        return type(self)(generator)

    def by_run(self, prototype=None):
        r'''Select components by run.

        ..  container:: example

            >>> staff = abjad.Staff(r"\times 2/3 { c'8 d'8 r8 }")
            >>> staff.append(r"\times 2/3 { r8 <e' g'>8 <f' a'>8 }")
            >>> staff.extend("g'8 a'8 r8 r8 <b' d''>8 <c'' e''>8")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    \times 2/3 {
                        c'8
                        d'8
                        r8
                    }
                    \times 2/3 {
                        r8
                        <e' g'>8
                        <f' a'>8
                    }
                    g'8
                    a'8
                    r8
                    r8
                    <b' d''>8
                    <c'' e''>8
                }

            >>> prototype = (abjad.Note, abjad.Chord)
            >>> for group in abjad.select(staff[:]).by_run(prototype):
            ...     group
            ...
            Selection([Note("g'8"), Note("a'8")])
            Selection([Chord("<b' d''>8"), Chord("<c'' e''>8")])

        ..  container:: example expression

            Selects pitched runs:

            >>> prototype = (abjad.Chord, abjad.Note)
            >>> expression = abjad.select()
            >>> expression = expression.by_leaf()
            >>> expression = expression.by_run(prototype=prototype)

            >>> string = r"c'8 d' r \times 2/3 { e' r f' } g' a' r"
            >>> staff = abjad.Staff(string)
            >>> staff.extend("r8 <c' e' g'>8 ~ <c' e' g'>4")
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    d'8
                    r8
                    \times 2/3 {
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        e'8
                        r8
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        f'8
                    }
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    g'8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    a'8
                    r8
                    r8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    <c' e' g'>8 ~
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    <c' e' g'>4
                }

            >>> expression.print(result)
            Selection([Note("c'8"), Note("d'8")])
            Selection([Note("e'8")])
            Selection([Note("f'8"), Note("g'8"), Note("a'8")])
            Selection([Chord("<c' e' g'>8"), Chord("<c' e' g'>4")])

        Returns new selection.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        generator = abjad.iterate(self).by_run(prototype=prototype)
        return type(self)(generator)

    def by_timeline(self, prototype=None, reverse=False):
        r'''Select components by timeline.

        ..  container:: example

            >>> score = abjad.Score()
            >>> score.append(abjad.Staff("c'4 d'4 e'4 f'4"))
            >>> score.append(abjad.Staff("g'8 a'8 b'8 c''8"))
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
                \new Score <<
                    \new Staff {
                        c'4
                        d'4
                        e'4
                        f'4
                    }
                    \new Staff {
                        g'8
                        a'8
                        b'8
                        c''8
                    }
                >>

            >>> for leaf in abjad.select(score).by_timeline():
            ...     leaf
            ...
            Note("c'4")
            Note("g'8")
            Note("a'8")
            Note("d'4")
            Note("b'8")
            Note("c''8")
            Note("e'4")
            Note("f'4")

        Returns new selection.
        '''
        import abjad
        generator = abjad.iterate(self).by_timeline(
            prototype=prototype,
            reverse=reverse,
            )
        return type(self)(generator)

    def by_timeline_and_logical_tie(
        self,
        nontrivial=False,
        pitched=False,
        reverse=False,
        ):
        r'''Select components by timeline and logical tie.

        ..  container:: example

            >>> score = abjad.Score()
            >>> score.append(abjad.Staff("c''4 ~ c''8 d''8 r4 ef''4"))
            >>> score.append(abjad.Staff("r8 g'4. ~ g'8 r16 f'8. ~ f'8"))
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
                \new Score <<
                    \new Staff {
                        c''4 ~
                        c''8
                        d''8
                        r4
                        ef''4
                    }
                    \new Staff {
                        r8
                        g'4. ~
                        g'8
                        r16
                        f'8. ~
                        f'8
                    }
                >>

            >>> selection = abjad.select(score)
            >>> for item in selection.by_timeline_and_logical_tie():
            ...     item
            ...
            LogicalTie([Note("c''4"), Note("c''8")])
            LogicalTie([Rest('r8')])
            LogicalTie([Note("g'4."), Note("g'8")])
            LogicalTie([Note("d''8")])
            LogicalTie([Rest('r4')])
            LogicalTie([Rest('r16')])
            LogicalTie([Note("f'8."), Note("f'8")])
            LogicalTie([Note("ef''4")])

        Returns new selection.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        generator = abjad.iterate(self).by_timeline_and_logical_tie(
            nontrivial=nontrivial,
            pitched=pitched,
            reverse=reverse,
            )
        return type(self)(generator)

    def flatten(self, depth=-1):
        r'''Flattens selection to `depth`.

        Returns new selection.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return type(self)(abjad.sequence(self).flatten(depth=depth))

    def filter(self, predicate=None):
        r'''Filters selection by `predicate`.

        ..  container:: example expression

            Selects notes runs with length greater than 1:

            >>> expression = abjad.select()
            >>> expression = expression.by_leaf()
            >>> expression = expression.by_run(abjad.Note)
            >>> inequality = abjad.LengthInequality('>', 1)
            >>> expression = expression.filter(inequality)

            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    c'8
                    r8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    d'8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    e'8
                    r8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    f'8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    g'8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    a'8
                }

            >>> expression.print(result)
            Selection([Note("d'8"), Note("e'8")])
            Selection([Note("f'8"), Note("g'8"), Note("a'8")])

        ..  container:: example expression

            Selects note runs with length less than 3:

            >>> expression = abjad.select()
            >>> expression = expression.by_leaf()
            >>> expression = expression.by_run(abjad.Note)
            >>> inequality = abjad.LengthInequality('<', 3)
            >>> expression = expression.filter(inequality)

            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'8
                    r8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    d'8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                }

            >>> expression.print(result)
            Selection([Note("c'8")])
            Selection([Note("d'8"), Note("e'8")])

        ..  container:: example expression

            Selects note runs with duration equal to 2/8:

            >>> expression = abjad.select()
            >>> expression = expression.by_leaf()
            >>> expression = expression.by_run(abjad.Note)
            >>> inequality = abjad.DurationInequality('==', (2, 8))
            >>> expression = expression.filter(inequality)

            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    c'8
                    r8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    d'8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                }

            >>> expression.print(result)
            Selection([Note("d'8"), Note("e'8")])

        ..  container:: example expression

            Selects note runs with duration less than 3/8:

            >>> inequality = abjad.DurationInequality('<', (3, 8))
            >>> expression = abjad.select()
            >>> expression = expression.by_leaf()
            >>> expression = expression.by_run(abjad.Note)
            >>> expression = expression.filter(inequality)

            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'8
                    r8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    d'8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                }

            >>> expression.print(result)
            Selection([Note("c'8")])
            Selection([Note("d'8"), Note("e'8")])

        ..  container:: example expression

            Selects note runs with duration greater than or equal to 1/4:

            >>> inequality = abjad.DurationInequality('>=', (1, 4))
            >>> expression = abjad.select()
            >>> expression = expression.by_leaf()
            >>> expression = expression.by_run(abjad.Note)
            >>> expression = expression.filter(inequality)

            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    c'8
                    r8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    d'8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    e'8
                    r8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    f'8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    g'8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    a'8
                }

            >>> expression.print(result)
            Selection([Note("d'8"), Note("e'8")])
            Selection([Note("f'8"), Note("g'8"), Note("a'8")])

        ..  container:: example expression

            Selects logical ties with preprolated duration equal to 1/8:

            >>> inequality = abjad.DurationInequality(
            ...     '==', (1, 8), preprolated=True,
            ...     )
            >>> expression = abjad.select()
            >>> expression = expression.by_logical_tie()
            >>> expression = expression.filter(inequality)

            >>> staff = abjad.Staff(r"""
            ...     \times 3/4 { c'16 d'16 ~ d'16 e'16 ~ }
            ...     {e'16 f'16 ~ f'16 g'16 ~ }
            ...     \times 5/4 { g'16 a'16 ~ a'16 b'16 }
            ...     """)
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/4 {
                        c'16
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        d'16 ~
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        d'16
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        e'16 ~
                    }
                    {
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        e'16
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        f'16 ~
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        f'16
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        g'16 ~
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 5/4 {
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        g'16
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        a'16 ~
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        a'16
                        b'16
                    }
                }

            >>> expression.print(result)
            LogicalTie([Note("d'16"), Note("d'16")])
            LogicalTie([Note("e'16"), Note("e'16")])
            LogicalTie([Note("f'16"), Note("f'16")])
            LogicalTie([Note("g'16"), Note("g'16")])
            LogicalTie([Note("a'16"), Note("a'16")])

        ..  container:: example expression

            Selects leaves with C4:

            >>> inequality = abjad.PitchInequality('intersects', 'C4')
            >>> expression = abjad.select().by_leaf()
            >>> expression = expression.filter(inequality)

            >>> staff = abjad.Staff("c'8 d'8 ~ d'8 e'8")
            >>> staff.extend("r8 <c' e' g'>8 ~ <c' e' g'>4")
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'8
                    d'8 ~
                    d'8
                    e'8
                    r8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    <c' e' g'>8 ~
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    <c' e' g'>4
                }

            >>> expression.print(result)
            Note("c'8")
            Chord("<c' e' g'>8")
            Chord("<c' e' g'>4")

        ..  container:: example expression

            Selects leaves with C4 or E4:

            >>> inequality = abjad.PitchInequality('intersects', 'C4 E4')
            >>> expression = abjad.select().by_leaf().filter(inequality)

            >>> staff = abjad.Staff("c'8 d'8 ~ d'8 e'8")
            >>> staff.extend("r8 <c' e' g'>8 ~ <c' e' g'>4")
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'8
                    d'8 ~
                    d'8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    e'8
                    r8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    <c' e' g'>8 ~
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    <c' e' g'>4
                }

            >>> expression.print(result)
            Note("c'8")
            Note("e'8")
            Chord("<c' e' g'>8")
            Chord("<c' e' g'>4")

        ..  container:: example expression

            Selects logical ties with C4:

            >>> inequality = abjad.PitchInequality('intersects', 'C4')
            >>> expression = abjad.select().by_logical_tie()
            >>> expression = expression.filter(inequality)

            >>> staff = abjad.Staff("c'8 d'8 ~ d'8 e'8")
            >>> staff.extend("r8 <c' e' g'>8 ~ <c' e' g'>4")
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'8
                    d'8 ~
                    d'8
                    e'8
                    r8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    <c' e' g'>8 ~
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    <c' e' g'>4
                }

            >>> expression.print(result)
            LogicalTie([Note("c'8")])
            LogicalTie([Chord("<c' e' g'>8"), Chord("<c' e' g'>4")])

        Returns new selection.
        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        if predicate is None:
            return self[:]
        items = []
        for item in self:
            if predicate(item):
                items.append(item)
        return type(self)(items)

    def get_duration(self, in_seconds=False):
        r'''Gets duration of contiguous selection.

        Returns duration.
        '''
        import abjad
        durations = []
        for item in self:
            if hasattr(item, '_get_duration'):
                duration = item._get_duration(in_seconds=in_seconds)
            else:
                duration = abjad.Duration(item)
            durations.append(duration)
        return sum(durations)

    # TODO: remove in favor of abjad.inspect(selection).get_spanners()
    def get_spanners(self, prototype=None):
        r'''Gets spanners attached to any component in selection.

        Returns set.
        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        spanners = set()
        for component in self:
            spanners_ = component._get_spanners(prototype=prototype)
            spanners.update(spanners_)
        return spanners

    def get_pitch_set(self):
        r'''Gets selection pitch set.

        Returns pitch set.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return abjad.PitchSet.from_selection(self)

    def get_timespan(self, in_seconds=False):
        r'''Gets timespan of contiguous selection.

        Returns timespan.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        if in_seconds:
            raise NotImplementedError
        timespan = self[0]._get_timespan()
        start_offset = timespan.start_offset
        stop_offset = timespan.stop_offset
        for x in self[1:]:
            timespan = x._get_timespan()
            if timespan.start_offset < start_offset:
                start_offset = timespan.start_offset
            if stop_offset < timespan.stop_offset:
                stop_offset = timespan.stop_offset
        return abjad.Timespan(start_offset, stop_offset)

    def get_vertical_moment_at(self, offset):
        r'''Select vertical moment at `offset`.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return abjad.VerticalMoment(self, offset)

    def group(self, predicate=None):
        r'''Groups items in selection by `predicate`.

        ..  container:: example

            Groups items in selection by type when `predicate` is none:

            >>> staff = abjad.Staff("c'8 d' e' r r f' g'")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    c'8
                    d'8
                    e'8
                    r8
                    r8
                    f'8
                    g'8
                }

            >>> for selection in staff[:].group(type):
            ...     selection
            ...
            Selection([Note("c'8"), Note("d'8"), Note("e'8")])
            Selection([Rest('r8'), Rest('r8')])
            Selection([Note("f'8"), Note("g'8")])

        ..  container:: example expression

            Groups pitched leaves by pitch:

            >>> expression = abjad.select().by_leaf(pitched=True)
            >>> expression = expression.group(abjad.select().get_pitch_set())

            >>> staff = abjad.Staff(r"""
            ...     c'8 ~ c'16 c'16 r8 c'16 c'16
            ...     d'8 ~ d'16 d'16 r8 d'16 d'16
            ...     """)
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'8 ~
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'16
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'16
                    r8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'16
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'16
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    d'8 ~
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    d'16
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    d'16
                    r8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    d'16
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    d'16
                }

            >>> expression.print(result)
            Selection([Note("c'8"), Note("c'16"), Note("c'16"), Note("c'16"), Note("c'16")])
            Selection([Note("d'8"), Note("d'16"), Note("d'16"), Note("d'16"), Note("d'16")])

        ..  container:: example expression

            Groups pitched logical ties by pitch:

            >>> predicate = abjad.select().by_leaf().pitch_set()
            >>> expression = abjad.select().by_logical_tie(pitched=True)
            >>> expression = expression.group(predicate)

            >>> staff = abjad.Staff(r"""
            ...     c'8 ~ c'16 c'16 r8 c'16 c'16
            ...     d'8 ~ d'16 d'16 r8 d'16 d'16
            ...     """)
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'8 ~
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'16
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'16
                    r8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'16
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'16
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    d'8 ~
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    d'16
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    d'16
                    r8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    d'16
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    d'16
                }

            >>> expression.print(result)
            Selection([LogicalTie([Note("c'8"), Note("c'16")]), LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")])])
            Selection([LogicalTie([Note("d'8"), Note("d'16")]), LogicalTie([Note("d'16")]), LogicalTie([Note("d'16")]), LogicalTie([Note("d'16")])])

        Returns nested selection.
        '''
        if self._expression:
            return self._update_expression(
                inspect.currentframe(),
                evaluation_template='group',
                map_operand=predicate,
                )
        items = []
        if predicate is None:
            pairs = itertools.groupby(self, lambda _: _)
            for count, group in pairs:
                item = type(self)(group)
                items.append(item)
        else:
            pairs = itertools.groupby(self, predicate)
            for count, group in pairs:
                item = type(self)(group)
                items.append(item)
        return type(self)(items)

    def in_contiguous_logical_voice(
        self,
        prototype=None,
        allow_orphans=True,
        ):
        r'''Is true when components are in contiguous logical voice.

        Returns true or false.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        if not isinstance(self, collections.Iterable):
            return False
        prototype = prototype or (abjad.Component,)
        if not isinstance(prototype, tuple):
            prototype = (prototype, )
        assert isinstance(prototype, tuple)
        if len(self) == 0:
            return True
        all_are_orphans_of_correct_type = True
        if allow_orphans:
            for component in self:
                if not isinstance(component, prototype):
                    all_are_orphans_of_correct_type = False
                    break
                if not component._get_parentage().is_orphan:
                    all_are_orphans_of_correct_type = False
                    break
            if all_are_orphans_of_correct_type:
                return True
        if not allow_orphans:
            if any(x._get_parentage().is_orphan for x in self):
                return False
        first = self[0]
        if not isinstance(first, prototype):
            return False
        first_parentage = first._get_parentage()
        first_logical_voice = first_parentage.logical_voice
        first_root = first_parentage.root
        previous = first
        for current in self[1:]:
            current_parentage = current._get_parentage()
            current_logical_voice = current_parentage.logical_voice
            # false if wrong type of component found
            if not isinstance(current, prototype):
                return False
            # false if in different logical voices
            if current_logical_voice != first_logical_voice:
                return False
            # false if components are in same score and are discontiguous
            if current_parentage.root == first_root:
                if not previous._is_immediate_temporal_successor_of(current):
                    return False
            previous = current
        return True

    def in_logical_voice(self, prototype=None, allow_orphans=True):
        r'''Is true when components are in same logical voice.

        Returns true or false.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        prototype = prototype or (abjad.Component,)
        if not isinstance(prototype, tuple):
            prototype = (prototype, )
        assert isinstance(prototype, tuple)
        if len(self) == 0:
            return True
        all_are_orphans_of_correct_type = True
        if allow_orphans:
            for component in self:
                if not isinstance(component, prototype):
                    all_are_orphans_of_correct_type = False
                    break
                if not component._get_parentage().is_orphan:
                    all_are_orphans_of_correct_type = False
                    break
            if all_are_orphans_of_correct_type:
                return True
        first = self[0]
        if not isinstance(first, prototype):
            return False
        orphan_components = True
        if not first._get_parentage().is_orphan:
            orphan_components = False
        same_logical_voice = True
        first_signature = first._get_parentage().logical_voice
        for component in self[1:]:
            parentage = component._get_parentage()
            if not parentage.is_orphan:
                orphan_components = False
            if not allow_orphans and orphan_components:
                return False
            if parentage.logical_voice != first_signature:
                same_logical_voice = False
            if not allow_orphans and not same_logical_voice:
                return False
            if (allow_orphans and
                not orphan_components and
                not same_logical_voice
                ):
                return False
        return True

    def in_same_parent(self, prototype=None, allow_orphans=True):
        r'''Is true when components are all in same parent.

        Returns true or false.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        prototype = prototype or (abjad.Component, )
        if not isinstance(prototype, tuple):
            prototype = (prototype, )
        assert isinstance(prototype, tuple)
        if len(self) == 0:
            return True
        all_are_orphans_of_correct_type = True
        if allow_orphans:
            for component in self:
                if not isinstance(component, prototype):
                    all_are_orphans_of_correct_type = False
                    break
                if not component._get_parentage().is_orphan:
                    all_are_orphans_of_correct_type = False
                    break
            if all_are_orphans_of_correct_type:
                return True
        first = self[0]
        if not isinstance(first, prototype):
            return False
        first_parent = first._parent
        if first_parent is None:
            if allow_orphans:
                orphan_components = True
            else:
                return False
        same_parent = True
        strictly_contiguous = True
        previous = first
        for current in self[1:]:
            if not isinstance(current, prototype):
                return False
            if not current._get_parentage().is_orphan:
                orphan_components = False
            if current._parent is not first_parent:
                same_parent = False
            if not previous._is_immediate_temporal_successor_of(current):
                strictly_contiguous = False
            if ((not allow_orphans or
                (allow_orphans and not orphan_components)) and
                (not same_parent or not strictly_contiguous)):
                return False
            previous = current
        return True

    def map(self, expression=None):
        r'''Maps `expression` to selection.

        ..  container:: example expression

            Selects tuplets:

            >>> expression = abjad.select()
            >>> expression = expression.by_class(abjad.Tuplet)

            >>> staff = abjad.Staff(r"""
            ...     \times 2/3 { r8 d' e' } f' r
            ...     r f' \times 2/3 { e' d' r8 }
            ...     """)
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \times 2/3 {
                        \once \override Dots.color = #red
                        \once \override Rest.color = #red
                        r8
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        d'8
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        e'8
                    }
                    f'8
                    r8
                    r8
                    f'8
                    \times 2/3 {
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        e'8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        d'8
                        \once \override Dots.color = #blue
                        \once \override Rest.color = #blue
                        r8
                    }
                }

            >>> expression.print(result)
            Tuplet(Multiplier(2, 3), "r8 d'8 e'8")
            Tuplet(Multiplier(2, 3), "e'8 d'8 r8")

        ..  container:: example expression

            Selects each tuplet:

            >>> expression = abjad.select()
            >>> expression = expression.by_class(abjad.Tuplet)
            >>> expression = expression.map(abjad.select())

            >>> staff = abjad.Staff(r"""
            ...     \times 2/3 { r8 d' e' } f' r
            ...     r f' \times 2/3 { e' d' r8 }
            ...     """)
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \times 2/3 {
                        \once \override Dots.color = #red
                        \once \override Rest.color = #red
                        r8
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        d'8
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        e'8
                    }
                    f'8
                    r8
                    r8
                    f'8
                    \times 2/3 {
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        e'8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        d'8
                        \once \override Dots.color = #blue
                        \once \override Rest.color = #blue
                        r8
                    }
                }

            >>> expression.print(result)
            Selection([Tuplet(Multiplier(2, 3), "r8 d'8 e'8")])
            Selection([Tuplet(Multiplier(2, 3), "e'8 d'8 r8")])

        ..  container:: example

            Selects leaves in each component:

            >>> staff = abjad.Staff(r"""
            ...     \times 2/3 { r8 d' e' } f' r
            ...     r f' \times 2/3 { e' d' r8 }
            ...     """)
            >>> result = staff[:].map(abjad.select().by_leaf())
            >>> for item in result:
            ...     item
            ...
            Selection([Rest('r8'), Note("d'8"), Note("e'8")])
            Selection([Note("f'8")])
            Selection([Rest('r8')])
            Selection([Rest('r8')])
            Selection([Note("f'8")])
            Selection([Note("e'8"), Note("d'8"), Rest('r8')])

            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \times 2/3 {
                        \once \override Dots.color = #red
                        \once \override Rest.color = #red
                        r8
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        d'8
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        e'8
                    }
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    f'8
                    \once \override Dots.color = #red
                    \once \override Rest.color = #red
                    r8
                    \once \override Dots.color = #blue
                    \once \override Rest.color = #blue
                    r8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    f'8
                    \times 2/3 {
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        e'8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        d'8
                        \once \override Dots.color = #blue
                        \once \override Rest.color = #blue
                        r8
                    }
                }

        ..  container:: example expression

            Selects first note in each run:

            >>> expression = abjad.select()
            >>> expression = expression.by_leaf()
            >>> expression = expression.by_run(abjad.Note)
            >>> expression = expression.map(abjad.select()[0])

            >>> string = r"c'4 \times 2/3 { d'8 r8 e'8 } r16 f'16 g'8 a'4"
            >>> staff = abjad.Staff(string)
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'4
                    \times 2/3 {
                        d'8
                        r8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        e'8
                    }
                    r16
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    f'16
                    g'8
                    a'4
                }

            >>> expression.print(result)
            Note("c'4")
            Note("e'8")
            Note("f'16")

        Returns list.
        '''
        if self._expression:
            return self._update_expression(
                inspect.currentframe(),
                evaluation_template='map',
                map_operand=expression,
                )
        if expression is not None:
            return type(self)([expression(_) for _ in self])
        else:
            return type(self)(self)

    def partition_by_counts(
        self,
        counts,
        cyclic=False,
        fuse_overhang=False,
        nonempty=False,
        overhang=False,
        ):
        r'''Partitions selection by `counts`.

        ..  container:: example expression

            Partitions once by counts without overhang:

            >>> expression = abjad.select()
            >>> expression = expression.by_leaf()
            >>> expression = expression.partition_by_counts(
            ...     [3],
            ...     cyclic=False,
            ...     overhang=False,
            ...     )


            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'8
                    \once \override Dots.color = #red
                    \once \override Rest.color = #red
                    r8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    d'8
                    e'8
                    r8
                    f'8
                    g'8
                    a'8
                }

            >>> expression.print(result)
            Selection([Note("c'8"), Rest('r8'), Note("d'8")])

        ..  container:: example expression

            Partitions cyclically by counts without overhang:

            >>> expression = abjad.select()
            >>> expression = expression.by_leaf()
            >>> expression = expression.partition_by_counts(
            ...     [3],
            ...     cyclic=True,
            ...     overhang=False,
            ...     )

            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'8
                    \once \override Dots.color = #red
                    \once \override Rest.color = #red
                    r8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    d'8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    e'8
                    \once \override Dots.color = #blue
                    \once \override Rest.color = #blue
                    r8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    f'8
                    g'8
                    a'8
                }

            >>> expression.print(result)
            Selection([Note("c'8"), Rest('r8'), Note("d'8")])
            Selection([Note("e'8"), Rest('r8'), Note("f'8")])

        ..  container:: example expression

            Partitions cyclically by counts with overhang:

            >>> expression = abjad.select()
            >>> expression = expression.by_leaf()
            >>> expression = expression.partition_by_counts(
            ...     [3],
            ...     cyclic=True,
            ...     overhang=True,
            ...     )

            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'8
                    \once \override Dots.color = #red
                    \once \override Rest.color = #red
                    r8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    d'8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    e'8
                    \once \override Dots.color = #blue
                    \once \override Rest.color = #blue
                    r8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    f'8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    g'8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    a'8
                }

            >>> expression.print(result)
            Selection([Note("c'8"), Rest('r8'), Note("d'8")])
            Selection([Note("e'8"), Rest('r8'), Note("f'8")])
            Selection([Note("g'8"), Note("a'8")])

        ..  container:: example expression

            Partitions cyclically by counts with fused overhang:

            >>> expression = abjad.select()
            >>> expression = expression.by_leaf()
            >>> expression = expression.partition_by_counts(
            ...     [3],
            ...     cyclic=True,
            ...     fuse_overhang=True,
            ...     overhang=True,
            ...     )

            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'8
                    \once \override Dots.color = #red
                    \once \override Rest.color = #red
                    r8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    d'8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    e'8
                    \once \override Dots.color = #blue
                    \once \override Rest.color = #blue
                    r8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    f'8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    g'8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    a'8
                }

            >>> expression.print(result)
            Selection([Note("c'8"), Rest('r8'), Note("d'8")])
            Selection([Note("e'8"), Rest('r8'), Note("f'8"), Note("g'8"), Note("a'8")])

        ..  container:: example expression

            Partitions cyclically by counts with overhang:

            >>> expression = abjad.select()
            >>> expression = expression.by_leaf()
            >>> expression = expression.partition_by_counts(
            ...     [1, 2, 3],
            ...     cyclic=True,
            ...     overhang=True,
            ...     )

            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8 b'8 r8 c''8")
            >>> result = expression(staff)
            >>> expression.color(result, ['red', 'blue', 'cyan'])
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'8
                    \once \override Dots.color = #blue
                    \once \override Rest.color = #blue
                    r8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    d'8
                    \once \override Accidental.color = #cyan
                    \once \override Beam.color = #cyan
                    \once \override Dots.color = #cyan
                    \once \override NoteHead.color = #cyan
                    \once \override Stem.color = #cyan
                    e'8
                    \once \override Dots.color = #cyan
                    \once \override Rest.color = #cyan
                    r8
                    \once \override Accidental.color = #cyan
                    \once \override Beam.color = #cyan
                    \once \override Dots.color = #cyan
                    \once \override NoteHead.color = #cyan
                    \once \override Stem.color = #cyan
                    f'8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    g'8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    a'8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    b'8
                    \once \override Dots.color = #cyan
                    \once \override Rest.color = #cyan
                    r8
                    \once \override Accidental.color = #cyan
                    \once \override Beam.color = #cyan
                    \once \override Dots.color = #cyan
                    \once \override NoteHead.color = #cyan
                    \once \override Stem.color = #cyan
                    c''8
                }

            >>> expression.print(result)
            Selection([Note("c'8")])
            Selection([Rest('r8'), Note("d'8")])
            Selection([Note("e'8"), Rest('r8'), Note("f'8")])
            Selection([Note("g'8")])
            Selection([Note("a'8"), Note("b'8")])
            Selection([Rest('r8'), Note("c''8")])

        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        result = []
        groups = abjad.sequence(self).partition_by_counts(
            [abs(_) for _ in counts],
            cyclic=cyclic,
            overhang=overhang,
            )
        groups = list(groups)
        if overhang and fuse_overhang and 1 < len(groups):
            last_count = counts[(len(groups) - 1) % len(counts)]
            if len(groups[-1]) != last_count:
                last_group = groups.pop()
                groups[-1] += last_group
        subresult = []
        if cyclic:
            counts = abjad.CyclicTuple(counts)
        for i, group in enumerate(groups):
            try:
                count = counts[i]
            except:
                raise Exception(counts, i)
            if count < 0:
                continue
            items = type(self)(group)
            subresult.append(items)
        if nonempty and not subresult:
            group = type(self)(groups[0])
            subresult.append(group)
        result.extend(subresult)
        return result

    def partition_by_durations(
        self,
        durations,
        cyclic=False,
        fill=None,
        in_seconds=False,
        overhang=False,
        ):
        r'''Partitions selection by `durations`.

        ..  container:: example

            Cyclically partitions exactly 3/8 (of a whole note) with overhang
            returned at end:

            >>> staff = abjad.Staff(
            ...     "abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
            ...     "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |"
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    {
                        \time 2/8
                        c'8
                        d'8
                    }
                    {
                        e'8
                        f'8
                    }
                    {
                        g'8
                        a'8
                    }
                    {
                        b'8
                        c''8
                    }
                }

            >>> leaves = abjad.select(staff).by_leaf()
            >>> selections = leaves.partition_by_durations(
            ...     [abjad.Duration(3, 8)],
            ...     cyclic=True,
            ...     fill=abjad.Exact,
            ...     in_seconds=False,
            ...     overhang=True,
            ...     )
            >>> for selection in selections:
            ...     selection
            ...
            Selection([Note("c'8"), Note("d'8"), Note("e'8")])
            Selection([Note("f'8"), Note("g'8"), Note("a'8")])
            Selection([Note("b'8"), Note("c''8")])

        ..  container:: example

            Partitions exactly 3/8 (of a whole note) one time only:

            >>> staff = abjad.Staff(
            ...     "abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
            ...     "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |"
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    {
                        \time 2/8
                        c'8
                        d'8
                    }
                    {
                        e'8
                        f'8
                    }
                    {
                        g'8
                        a'8
                    }
                    {
                        b'8
                        c''8
                    }
                }

            >>> leaves = abjad.select(staff).by_leaf()
            >>> selections = leaves.partition_by_durations(
            ...     [abjad.Duration(3, 8)],
            ...     cyclic=False,
            ...     fill=abjad.Exact,
            ...     in_seconds=False,
            ...     overhang=False,
            ...     )
            >>> for selection in selections:
            ...     selection
            ...
            Selection([Note("c'8"), Note("d'8"), Note("e'8")])

        ..  container:: example

            Cyclically partitions 3/16 and 1/16 (of a whole note) with part
            durations allowed to be just more than 3/16 and 1/16 (of a whole
            note) and with overhang returned at end:

            >>> staff = abjad.Staff(
            ...     "abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
            ...     "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |"
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    {
                        \time 2/8
                        c'8
                        d'8
                    }
                    {
                        e'8
                        f'8
                    }
                    {
                        g'8
                        a'8
                    }
                    {
                        b'8
                        c''8
                    }
                }

            >>> leaves = abjad.select(staff).by_leaf()
            >>> selections = leaves.partition_by_durations(
            ...     [abjad.Duration(3, 16), abjad.Duration(1, 16)],
            ...     cyclic=True,
            ...     fill=abjad.More,
            ...     in_seconds=False,
            ...     overhang=True,
            ...     )
            >>> for selection in selections:
            ...     selection
            ...
            Selection([Note("c'8"), Note("d'8")])
            Selection([Note("e'8")])
            Selection([Note("f'8"), Note("g'8")])
            Selection([Note("a'8")])
            Selection([Note("b'8"), Note("c''8")])

        ..  container:: example

            Cyclically partitions 3/16 (of a whole note) with part durations
            allowed to be just less than 3/16 (of a whole note):

            >>> staff = abjad.Staff(
            ...     "abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
            ...     "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |"
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    {
                        \time 2/8
                        c'8
                        d'8
                    }
                    {
                        e'8
                        f'8
                    }
                    {
                        g'8
                        a'8
                    }
                    {
                        b'8
                        c''8
                    }
                }

            >>> leaves = abjad.select(staff).by_leaf()
            >>> selections = leaves.partition_by_durations(
            ...     [abjad.Duration(3, 16)],
            ...     cyclic=True,
            ...     fill=abjad.Less,
            ...     in_seconds=False,
            ...     overhang=False,
            ...     )
            >>> for selection in selections:
            ...     selection
            ...
            Selection([Note("c'8")])
            Selection([Note("d'8")])
            Selection([Note("e'8")])
            Selection([Note("f'8")])
            Selection([Note("g'8")])
            Selection([Note("a'8")])
            Selection([Note("b'8")])

        ..  container:: example

            Partitions 3/16 (of a whole note) just once with part duration
            allowed to be just less than 3/16 (of a whole note):

            >>> staff = abjad.Staff(
            ...     "abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
            ...     "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |"
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    {
                        \time 2/8
                        c'8
                        d'8
                    }
                    {
                        e'8
                        f'8
                    }
                    {
                        g'8
                        a'8
                    }
                    {
                        b'8
                        c''8
                    }
                }

            >>> leaves = abjad.select(staff).by_leaf()
            >>> selections = leaves.partition_by_durations(
            ...     [abjad.Duration(3, 16)],
            ...     cyclic=False,
            ...     fill=abjad.Less,
            ...     in_seconds=False,
            ...     overhang=False,
            ...     )
            >>> for selection in selections:
            ...     selection
            ...
            Selection([Note("c'8")])

        Examples in seconds appear below.

        ..  container:: example

            Cyclically partitions exactly 1.5 seconds at a time:

            >>> staff = abjad.Staff(
            ...     "abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
            ...     "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |"
            ...     )
            >>> mark = abjad.MetronomeMark((1, 4), 60)
            >>> leaf = abjad.inspect(staff).get_leaf(0)
            >>> abjad.attach(mark, leaf, scope=abjad.Staff)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    {
                        \time 2/8
                        \tempo 4=60
                        c'8
                        d'8
                    }
                    {
                        e'8
                        f'8
                    }
                    {
                        g'8
                        a'8
                    }
                    {
                        b'8
                        c''8
                    }
                }

            >>> leaves = abjad.select(staff).by_leaf()
            >>> selections = leaves.partition_by_durations(
            ...     [1.5],
            ...     cyclic=True,
            ...     fill=abjad.Exact,
            ...     in_seconds=True,
            ...     overhang=False,
            ...     )
            >>> for selection in selections:
            ...     selection
            ...
            Selection([Note("c'8"), Note("d'8"), Note("e'8")])
            Selection([Note("f'8"), Note("g'8"), Note("a'8")])

        ..  container:: example

            Cyclically partitions exactly 1.5 seconds at a time with overhang
            returned at end:

            >>> staff = abjad.Staff(
            ...     "abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
            ...     "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |"
            ...     )
            >>> mark = abjad.MetronomeMark((1, 4), 60)
            >>> leaf = abjad.inspect(staff).get_leaf(0)
            >>> abjad.attach(mark, leaf, scope=abjad.Staff)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    {
                        \time 2/8
                        \tempo 4=60
                        c'8
                        d'8
                    }
                    {
                        e'8
                        f'8
                    }
                    {
                        g'8
                        a'8
                    }
                    {
                        b'8
                        c''8
                    }
                }

            >>> leaves = abjad.select(staff).by_leaf()
            >>> selections = leaves.partition_by_durations(
            ...     [1.5],
            ...     cyclic=True,
            ...     fill=abjad.Exact,
            ...     in_seconds=True,
            ...     overhang=True,
            ...     )
            >>> for selection in selections:
            ...     selection
            ...
            Selection([Note("c'8"), Note("d'8"), Note("e'8")])
            Selection([Note("f'8"), Note("g'8"), Note("a'8")])
            Selection([Note("b'8"), Note("c''8")])

        ..  container:: example

            Partitions exactly 1.5 seconds one time only:

            >>> staff = abjad.Staff(
            ...     "abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
            ...     "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |"
            ...     )
            >>> mark = abjad.MetronomeMark((1, 4), 60)
            >>> leaf = abjad.inspect(staff).get_leaf(0)
            >>> abjad.attach(mark, leaf, scope=abjad.Staff)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    {
                        \time 2/8
                        \tempo 4=60
                        c'8
                        d'8
                    }
                    {
                        e'8
                        f'8
                    }
                    {
                        g'8
                        a'8
                    }
                    {
                        b'8
                        c''8
                    }
                }

            >>> leaves = abjad.select(staff).by_leaf()
            >>> selections = leaves.partition_by_durations(
            ...     [1.5],
            ...     cyclic=False,
            ...     fill=abjad.Exact,
            ...     in_seconds=True,
            ...     overhang=False,
            ...     )
            >>> for selection in selections:
            ...     selection
            ...
            Selection([Note("c'8"), Note("d'8"), Note("e'8")])

        ..  container:: example

            Cyclically partitions 0.75 seconds with part durations allowed to
            be just less than 0.75 seconds:

            >>> staff = abjad.Staff(
            ...     "abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
            ...     "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |"
            ...     )
            >>> mark = abjad.MetronomeMark((1, 4), 60)
            >>> leaf = abjad.inspect(staff).get_leaf(0)
            >>> abjad.attach(mark, leaf, scope=abjad.Staff)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    {
                        \time 2/8
                        \tempo 4=60
                        c'8
                        d'8
                    }
                    {
                        e'8
                        f'8
                    }
                    {
                        g'8
                        a'8
                    }
                    {
                        b'8
                        c''8
                    }
                }

            >>> leaves = abjad.select(staff).by_leaf()
            >>> selections = leaves.partition_by_durations(
            ...     [0.75],
            ...     cyclic=True,
            ...     fill=abjad.Less,
            ...     in_seconds=True,
            ...     overhang=False,
            ...     )
            >>> for selection in selections:
            ...     selection
            ...
            Selection([Note("c'8")])
            Selection([Note("d'8")])
            Selection([Note("e'8")])
            Selection([Note("f'8")])
            Selection([Note("g'8")])
            Selection([Note("a'8")])
            Selection([Note("b'8")])

        ..  container:: example

            Partitions 0.75 seconds just once with part duration allowed to be
            just less than 0.75 seconds:

            >>> staff = abjad.Staff(
            ...     "abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |"
            ...     "| 2/8 g'8 a'8 || 2/8 b'8 c''8 |"
            ...     )
            >>> mark = abjad.MetronomeMark((1, 4), 60)
            >>> leaf = abjad.inspect(staff).get_leaf(0)
            >>> abjad.attach(mark, leaf, scope=abjad.Staff)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    {
                        \time 2/8
                        \tempo 4=60
                        c'8
                        d'8
                    }
                    {
                        e'8
                        f'8
                    }
                    {
                        g'8
                        a'8
                    }
                    {
                        b'8
                        c''8
                    }
                }

            >>> leaves = abjad.select(staff).by_leaf()
            >>> selections = leaves.partition_by_durations(
            ...     [0.75],
            ...     cyclic=False,
            ...     fill=abjad.Less,
            ...     in_seconds=True,
            ...     overhang=False,
            ...     )
            >>> for selection in selections:
            ...     selection
            ...
            Selection([Note("c'8")])

        Interprets `fill` as `Exact` when `fill` is none.

        Parts must equal `durations` exactly when `fill` is `Exact`.

        Parts must be less than or equal to `durations` when `fill` is `Less`.

        Parts must be greater or equal to `durations` when `fill` is `More`.

        Reads `durations` cyclically when `cyclic` is true.

        Reads component durations in seconds when `in_seconds` is true.

        Returns remaining components at end in final part when `overhang`
        is true.

        Returns list of selections.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        fill = fill or abjad.Exact
        durations = [abjad.Duration(_) for _ in durations]
        if cyclic:
            durations = abjad.CyclicTuple(durations)
        result = []
        part = []
        current_duration_index = 0
        target_duration = durations[current_duration_index]
        cumulative_duration = abjad.Duration(0)
        components_copy = list(self)
        while True:
            try:
                component = components_copy.pop(0)
            except IndexError:
                break
            component_duration = component._get_duration()
            if in_seconds:
                component_duration = component._get_duration(in_seconds=True)
            candidate_duration = cumulative_duration + component_duration
            if candidate_duration < target_duration:
                part.append(component)
                cumulative_duration = candidate_duration
            elif candidate_duration == target_duration:
                part.append(component)
                result.append(part)
                part = []
                cumulative_duration = abjad.Duration(0)
                current_duration_index += 1
                try:
                    target_duration = durations[current_duration_index]
                except IndexError:
                    break
            elif target_duration < candidate_duration:
                if fill == abjad.Exact:
                    message = 'must partition exactly.'
                    raise Exception(message)
                elif fill == abjad.Less:
                    result.append(part)
                    part = [component]
                    if in_seconds:
                        cumulative_duration = sum([
                            _._get_duration(in_seconds=True)
                            for _ in part
                            ])
                    else:
                        cumulative_duration = sum([
                            _._get_duration() for _ in part
                            ])
                    current_duration_index += 1
                    try:
                        target_duration = durations[current_duration_index]
                    except IndexError:
                        break
                    if target_duration < cumulative_duration:
                        message = 'target duration {}'
                        message += ' is less than cumulative duration {}.'
                        message = message.format(
                            target_duration,
                            cumulative_duration,
                            )
                        raise Exception(message)
                elif fill == abjad.More:
                    part.append(component)
                    result.append(part)
                    part = []
                    cumulative_duration = abjad.Duration(0)
                    current_duration_index += 1
                    try:
                        target_duration = durations[current_duration_index]
                    except IndexError:
                        break
        if len(part):
            if overhang:
                result.append(part)
        if len(components_copy):
            if overhang:
                result.append(components_copy)
        result = [type(self)(_) for _ in result]
        return type(self)(result)

    def partition_by_ratio(self, ratio):
        r'''Partitions by ratio.

        ..  container:: example expression

            Partitions leaves by ratio of 1:1:

            >>> expression = abjad.select()
            >>> expression = expression.by_leaf()
            >>> expression = expression.partition_by_ratio((1, 1))

            >>> staff = abjad.Staff(r"c'8 d' r \times 2/3 { e' r f' } g' a' r")
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    d'8
                    \once \override Dots.color = #red
                    \once \override Rest.color = #red
                    r8
                    \times 2/3 {
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        e'8
                        \once \override Dots.color = #red
                        \once \override Rest.color = #red
                        r8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        f'8
                    }
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    g'8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    a'8
                    \once \override Dots.color = #blue
                    \once \override Rest.color = #blue
                    r8
                }

            >>> expression.print(result)
            Selection([Note("c'8"), Note("d'8"), Rest('r8'), Note("e'8"), Rest('r8')])
            Selection([Note("f'8"), Note("g'8"), Note("a'8"), Rest('r8')])

        ..  container:: example expression

            Partitions leaves by ratio of 1:1:1:

            >>> expression = abjad.select()
            >>> expression = expression.by_leaf()
            >>> expression = expression.partition_by_ratio((1, 1, 1))

            >>> staff = abjad.Staff(r"c'8 d' r \times 2/3 { e' r f' } g' a' r")
            >>> result = expression(staff)
            >>> expression.color(result, ['red', 'blue', 'cyan'])
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    d'8
                    \once \override Dots.color = #red
                    \once \override Rest.color = #red
                    r8
                    \times 2/3 {
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        e'8
                        \once \override Dots.color = #blue
                        \once \override Rest.color = #blue
                        r8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        f'8
                    }
                    \once \override Accidental.color = #cyan
                    \once \override Beam.color = #cyan
                    \once \override Dots.color = #cyan
                    \once \override NoteHead.color = #cyan
                    \once \override Stem.color = #cyan
                    g'8
                    \once \override Accidental.color = #cyan
                    \once \override Beam.color = #cyan
                    \once \override Dots.color = #cyan
                    \once \override NoteHead.color = #cyan
                    \once \override Stem.color = #cyan
                    a'8
                    \once \override Dots.color = #cyan
                    \once \override Rest.color = #cyan
                    r8
                }

            >>> expression.print(result)
            Selection([Note("c'8"), Note("d'8"), Rest('r8')])
            Selection([Note("e'8"), Rest('r8'), Note("f'8")])
            Selection([Note("g'8"), Note("a'8"), Rest('r8')])

        Returns new expression.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        ratio = ratio or abjad.Ratio((1,))
        counts = abjad.mathtools.partition_integer_by_ratio(
            len(self),
            ratio,
            )
        parts = abjad.sequence(self).partition_by_counts(counts=counts)
        selections = [type(self)(_) for _ in parts]
        return selections

    def top(self):
        r'''Selects top components.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        result = []
        for component in abjad.iterate(self).by_class(abjad.Component):
            parentage = abjad.inspect(component).get_parentage()
            for component_ in parentage:
                if isinstance(component_, abjad.Context):
                    break
                parent = abjad.inspect(component_).get_parentage().parent
                if isinstance(parent, abjad.Context) or parent is None:
                    if component_ not in result:
                        result.append(component_)
                    break
        return type(self)(result)

    def with_next_leaf(self):
        r'''Selects with next leaf.

        ..  container:: example expression

            Selects note runs (with next leaf):

            >>> expression = abjad.select()
            >>> expression = expression.by_leaf()
            >>> expression = expression.by_run(abjad.Note)
            >>> expression = expression.map(abjad.select().with_next_leaf())

            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'8
                    \once \override Dots.color = #red
                    \once \override Rest.color = #red
                    r8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    d'8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    e'8
                    \once \override Dots.color = #blue
                    \once \override Rest.color = #blue
                    r8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    f'8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    g'8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    a'8
                }

            >>> expression.print(result)
            Selection([Note("c'8"), Rest('r8')])
            Selection([Note("d'8"), Note("e'8"), Rest('r8')])
            Selection([Note("f'8"), Note("g'8"), Note("a'8")])

        ..  container:: example expression

            Selects pitched tails (with next leaf):

            >>> expression = abjad.select()
            >>> expression = expression.by_logical_tie(pitched=True)
            >>> get = abjad.select()[-1].select().with_next_leaf()
            >>> expression = expression.map(get)

            >>> staff = abjad.Staff(r"c'8 r d' ~ d' e' ~ e' r8 f'8")
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'8
                    \once \override Dots.color = #red
                    \once \override Rest.color = #red
                    r8
                    d'8 ~
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    d'8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    e'8 ~
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    e'8
                    \once \override Dots.color = #red
                    \once \override Rest.color = #red
                    r8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    f'8
                }

            >>> expression.print(result)
            Selection([Note("c'8"), Rest('r8')])
            Selection([Note("d'8"), Note("e'8")])
            Selection([Note("e'8"), Rest('r8')])
            Selection([Note("f'8")])

        ..  container:: example expression

            Selects pitched logical ties (with next leaf). This is the correct
            selection for single-pitch sustain pedal application:

            >>> expression = abjad.select()
            >>> expression = expression.by_logical_tie(pitched=True)
            >>> expression = expression.map(abjad.select().with_next_leaf())

            >>> staff = abjad.Staff(r"c'8 r d' ~ d' e' ~ e' r8 f'8")
            >>> result = expression(staff)
            >>> for selection in result:
            ...     abjad.attach(abjad.PianoPedalSpanner(), selection)
            ...

            >>> expression.color(result)
            >>> manager = abjad.override(staff).sustain_pedal_line_spanner
            >>> manager.staff_padding = 6
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    \override SustainPedalLineSpanner.staff-padding = #6
                    autoBeaming = ##f
                } {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    \set Staff.pedalSustainStyle = #'mixed
                    c'8 \sustainOn
                    \once \override Dots.color = #red
                    \once \override Rest.color = #red
                    r8 \sustainOff
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    \set Staff.pedalSustainStyle = #'mixed
                    d'8 ~ \sustainOn
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    d'8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    \set Staff.pedalSustainStyle = #'mixed
                    e'8 ~ \sustainOff \sustainOn
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    e'8
                    \once \override Dots.color = #red
                    \once \override Rest.color = #red
                    r8 \sustainOff
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    \set Staff.pedalSustainStyle = #'mixed
                    f'8 \sustainOn \sustainOff
                }

            >>> expression.print(result)
            Selection([Note("c'8"), Rest('r8')])
            Selection([Note("d'8"), Note("d'8"), Note("e'8")])
            Selection([Note("e'8"), Note("e'8"), Rest('r8')])
            Selection([Note("f'8")])

        Returns new expression.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        leaves = list(self.by_leaf())
        next_leaf = leaves[-1]._get_leaf(1)
        if next_leaf is not None:
            leaves.append(next_leaf)
        return type(self)(leaves)

    def with_previous_leaf(self):
        r'''Selects with previous leaf.

        ..  container:: example expression

            Selects note runs (with previous leaf):

            >>> expression = abjad.select()
            >>> expression = expression.by_leaf()
            >>> expression = expression.by_run(abjad.Note)
            >>> get = abjad.select().with_previous_leaf()
            >>> expression = expression.map(get)

            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'8
                    \once \override Dots.color = #blue
                    \once \override Rest.color = #blue
                    r8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    d'8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    e'8
                    \once \override Dots.color = #red
                    \once \override Rest.color = #red
                    r8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    f'8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    g'8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    a'8
                }

            >>> expression.print(result)
            Selection([Note("c'8")])
            Selection([Rest('r8'), Note("d'8"), Note("e'8")])
            Selection([Rest('r8'), Note("f'8"), Note("g'8"), Note("a'8")])

        ..  container:: example expression

            Selects pitched heads (with previous leaf):

            >>> expression = abjad.select()
            >>> expression = expression.by_logical_tie(pitched=True)
            >>> get = abjad.select()[0].select().with_previous_leaf()
            >>> expression = expression.map(get)

            >>> staff = abjad.Staff(r"c'8 r d' ~ d' e' ~ e' r8 f'8")
            >>> result = expression(staff)
            >>> expression.color(result)
            >>> abjad.setting(staff).auto_beaming = False
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'8
                    \once \override Dots.color = #blue
                    \once \override Rest.color = #blue
                    r8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    d'8 ~
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    d'8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    e'8 ~
                    e'8
                    \once \override Dots.color = #blue
                    \once \override Rest.color = #blue
                    r8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    f'8
                }

            >>> expression.print(result)
            Selection([Note("c'8")])
            Selection([Rest('r8'), Note("d'8")])
            Selection([Note("d'8"), Note("e'8")])
            Selection([Rest('r8'), Note("f'8")])

        Returns new expression.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        leaves = list(self.by_leaf())
        previous_leaf = leaves[0]._get_leaf(-1)
        if previous_leaf is not None:
            leaves.insert(0, previous_leaf)
        return type(self)(leaves)


collections.Sequence.register(Selection)


r"""
    @staticmethod
    def run_selectors(argument, selectors):

        Returns a dictionary of selector/selection pairs.
        '''
        import abjad
        prototype = (abjad.Component, abjad.Selection)
        if not isinstance(argument, prototype):
            argument = abjad.select(argument)
        argument = (argument,)
        assert all(isinstance(_, prototype) for _ in argument), repr(argument)
        maximum_length = 0
        for selector in selectors:
            if selector.callbacks:
                maximum_length = max(maximum_length, len(selector.callbacks))
        #print('MAX LENGTH', maximum_length)
        selectors = list(selectors)
        results_by_prefix = {(): argument}
        results_by_selector = collections.OrderedDict()
        for index in range(1, maximum_length + 2):
            #print('INDEX', index)
            #print('PRUNING')
            for selector in selectors[:]:
                callbacks = selector.callbacks or ()
                callback_length = index - 1
                if len(callbacks) == callback_length:
                    prefix = callbacks[:callback_length]
                    results_by_selector[selector] = results_by_prefix[prefix]
                    selectors.remove(selector)
                    #print('\tREMOVED:', selector)
                    #print('\tREMAINING:', len(selectors))
            if not selectors:
                #print('BREAKING')
                break
            #print('ADDING')
            for selector in selectors:
                callbacks = selector.callbacks or ()
                this_prefix = callbacks[:index]
                if this_prefix in results_by_prefix:
                    #print('\tSKIPPING', repr(selector))
                    continue
                #print('\tADDING', repr(selector))
                previous_prefix = callbacks[:index - 1]
                previous_expr = results_by_prefix[previous_prefix]
                callback = this_prefix[-1]
                argument = callback(previous_expr)
                results_by_prefix[this_prefix] = argument
        return results_by_selector
"""
