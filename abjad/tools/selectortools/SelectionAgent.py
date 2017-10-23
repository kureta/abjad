import collections
import inspect
import itertools
from abjad.tools import abctools


class SelectionAgent(abctools.AbjadObject):
    r'''Selection agent.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Selectors'

    __slots__ = (
        '_callbacks',
        '_client',
        '_expression',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        client=None,
        callbacks=None,
        ):
        assert not isinstance(client, str), repr(client)
        if callbacks is not None:
            callbacks = tuple(callbacks)
        self._callbacks = callbacks
        self._client = client
        self._expression = None

    ### SPECIAL METHODS ###

    def __call__(self, music=None):
        r'''Calls selector on `music`.

        Returns selection.
        '''
        import abjad
        prototype = (abjad.Component, abjad.Selection, list)
        if not isinstance(music, prototype):
            raise Exception(music)
            music = abjad.select(music)
        for callback in self.callbacks or ():
            music = callback(music)
        return music

    def __getitem__(self, argument):
        r'''Gets item or slice identified by `argument`.

        Returns another selector.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.client.__getitem__(argument)

    ### PRIVATE METHODS ###

    def _append_callback(self, callback):
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

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

    ### PUBLIC PROPERTIES ###

    @property
    def callbacks(self):
        r'''Gets callbacks.

        Returns tuple.
        '''
        return self._callbacks

    @property
    def client(self):
        r'''Gets client.

        Returns client.
        '''
        return self._client

    ### PUBLIC METHODS ###

    def by_class(self, prototype=None):
        r'''Selects by class.

        Returns new expression.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return abjad.Selection._by_class(self.client, prototype=prototype)

    def by_contiguity(self):
        r'''Selects by contiguity.

        Returns new expression.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        selections, selection = [], []
        selection.extend(self.client[:1])
        for item in self.client[1:]:
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
                selections.append(abjad.Selection._manifest(selection))
                selection = [item]
        if selection:
            selections.append(abjad.Selection._manifest(selection))
        return selections

    def by_duration(self, inequality=None, duration=None, preprolated=None):
        r'''Selects by duration.

        Returns new expression.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
#        duration_expr = None
#        prototype = (abjad.Duration, abjad.DurationInequality)
#        if isinstance(inequality, prototype):
#            duration_expr = inequality
#        elif isinstance(inequality, str) and duration is not None:
#            duration_expr = abjad.DurationInequality(
#                duration=duration,
#                operator_string=inequality,
#                )
#        elif inequality is None and duration is not None:
#            duration_expr = abjad.DurationInequality(
#                duration=duration,
#                operator_string='==',
#                )
#        if not isinstance(duration_expr, prototype):
#            raise ValueError(inequality, duration)
#        callback = abjad.ByDurationCallback(
#            duration=duration_expr,
#            preprolated=preprolated,
#            )
#        selector = self._append_callback(callback)
#        return selector
        raise Exception('implement duration filter')

    def by_leaf(
        self,
        prototype=None,
        head=None,
        pitched=None,
        tail=None,
        trim=None,
        ):
        r'''Selects by leaf.

        Returns new expression.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        if pitched:
            prototype = (abjad.Chord, abjad.Note)
        elif prototype is None:
            prototype = abjad.Leaf
        return abjad.Selection._by_class(
            self.client,
            prototype=prototype,
            head=head,
            tail=tail,
            trim=trim,
            )

    def by_length(self, inequality=None, length=None):
        r'''Selects by length.

        Returns new expression.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        length_expr = None
        if isinstance(inequality, (int, float, abjad.LengthInequality)):
            length_expr = inequality
        elif isinstance(inequality, str) and length is not None:
            length_expr = abjad.LengthInequality(
                length=int(length),
                operator_string=inequality,
                )
        elif inequality is None and length is not None:
            length_expr = abjad.LengthInequality(
                length=int(length),
                operator_string='==',
                )
        if not isinstance(length_expr, (int, float, abjad.LengthInequality)):
            raise ValueError(inequality, length)
        raise Exception('implement length filter')

    def by_logical_measure(self):
        r'''Selects by logical measure.

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
        argument = self.client
        first_component = _get_first_component(argument)
        first_component._update_logical_measure_numbers()
        pairs = itertools.groupby(argument, _get_logical_measure_number)
        for value, group in pairs:
            selection = abjad.Selection._manifest(group)
            selections.append(selection)
        return abjad.Selection._manifest(selections)

    def by_logical_tie(
        self,
        nontrivial=False,
        pitched=False,
        with_grace_notes=True,
        ):
        r'''Selects by logical tie.

        Returns new expression.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        generator = abjad.iterate(self.client).by_logical_tie(
            pitched=pitched,
            nontrivial=nontrivial,
            with_grace_notes=with_grace_notes,
            )
        return abjad.Selection._manifest(generator)

#    def by_pattern(self, pattern=None):
#        r'''Selects by `pattern`.
#
#        Returns new expression.
#        '''
#        import abjad
#        callback = abjad.ByPatternCallback(pattern=pattern)
#        selector = self._append_callback(callback)
#        return selector

#    def by_pitch(self, pitches=None):
#        r'''Selects by pitch.
#
#        Returns new expression.
#        '''
#        import abjad
#        callback = abjad.ByPitchCallback(pitches=pitches)
#        selector = self._append_callback(callback)
#        return selector

    def by_run(self, prototype=None):
        r'''Selects by run.

        Returns new expression.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        generator = abjad.iterate(self.client).by_run(prototype=prototype)
        return abjad.Selection._manifest(generator)

    def color(self, result, colors=None):
        r'''Colors `result`.

        Returns none.
        '''
        import abjad
        abjad.label(result).color_selections(self._expression, colors=colors)

#    def group_by_pitch(self, allow_discontiguity=False):
#        r'''Groups by pitch.
#
#        Returns new expression.
#        '''
#        import abjad
#        callback = abjad.GroupByPitchCallback(
#            allow_discontiguity=allow_discontiguity,
#            )
#        selector = self._append_callback(callback)
#        return selector

    def map(self, operand=None):
        r'''Maps `operand` to selection.

        Returns list.
        '''
        import abjad
        if self._expression:
            return self._update_expression(
                inspect.currentframe(),
                evaluation_template='map',
                map_operand=operand,
                )
        raise Exception('evaluation handled in abjad.Expression (not here).')
        if operand is not None:
            return [operand(_) for _ in self]
        else:
            return [_ for _ in self]

    def partition_by_counts(
        self,
        counts,
        cyclic=False,
        fuse_overhang=False,
        nonempty=False,
        overhang=False,
        ):
        r'''Partitions by counts.

        Returns new expression.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        result = []
        argument = self.client
        groups = abjad.Sequence(argument).partition_by_counts(
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
        for i, group in enumerate(groups):
            try:
                count = counts[i]
            except:
                raise Exception(counts, i)
            if count < 0:
                continue
            items = abjad.Selection._manifest(group)
            subresult.append(items)
        if nonempty and not subresult:
            group = abjad.Selection._manifest(groups[0])
            subresult.append(group)
        result.extend(subresult)
        return result

#    def partition_by_ratio(self, ratio):
#        r'''Partitions by ratio.
#
#        Returns new expression.
#        '''
#        import abjad
#        callback = abjad.PartitionByRatioCallback(ratio)
#        selector = self._append_callback(callback)
#        return selector

#    def top(self):
#        r'''Selects top components.
#        '''
#        import abjad
#        if self._expression:
#            return self._update_expression(inspect.currentframe())
#        result = []
#        for component in abjad.iterate(self.client).by_class(abjad.Component):
#            parentage = abjad.inspect(component).get_parentage()
#            for component_ in parentage:
#                if isinstance(component_, abjad.Context):
#                    break
#                parent = abjad.inspect(component_).get_parentage().parent
#                if isinstance(parent, abjad.Context) or parent is None:
#                    if component_ not in result:
#                        result.append(component_)
#                    break
#        return abjad.Selection._manifest(result)

#    def with_next_leaf(self):
#        r'''Selects with next leaf.
#
#        ..  container:: example
#
#            Selects note runs (with next leaf):
#
#            ::
#
#                >>> selector = abjad.select()
#                >>> selector = selector.by_leaf()
#                >>> selector = selector.by_run(abjad.Note)
#                >>> selector = selector.map(abjad.select().with_next_leaf())
#
#            ::
#
#                >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
#                >>> result = selector(staff)
#                >>> selector.color(result)
#                >>> abjad.setting(staff).auto_beaming = False
#                >>> show(staff) # doctest: +SKIP
#
#            ..  docs::
#
#                >>> f(staff)
#                \new Staff \with {
#                    autoBeaming = ##f
#                } {
#                    \once \override Accidental.color = #red
#                    \once \override Beam.color = #red
#                    \once \override Dots.color = #red
#                    \once \override NoteHead.color = #red
#                    \once \override Stem.color = #red
#                    c'8
#                    \once \override Dots.color = #red
#                    \once \override Rest.color = #red
#                    r8
#                    \once \override Accidental.color = #blue
#                    \once \override Beam.color = #blue
#                    \once \override Dots.color = #blue
#                    \once \override NoteHead.color = #blue
#                    \once \override Stem.color = #blue
#                    d'8
#                    \once \override Accidental.color = #blue
#                    \once \override Beam.color = #blue
#                    \once \override Dots.color = #blue
#                    \once \override NoteHead.color = #blue
#                    \once \override Stem.color = #blue
#                    e'8
#                    \once \override Dots.color = #blue
#                    \once \override Rest.color = #blue
#                    r8
#                    \once \override Accidental.color = #red
#                    \once \override Beam.color = #red
#                    \once \override Dots.color = #red
#                    \once \override NoteHead.color = #red
#                    \once \override Stem.color = #red
#                    f'8
#                    \once \override Accidental.color = #red
#                    \once \override Beam.color = #red
#                    \once \override Dots.color = #red
#                    \once \override NoteHead.color = #red
#                    \once \override Stem.color = #red
#                    g'8
#                    \once \override Accidental.color = #red
#                    \once \override Beam.color = #red
#                    \once \override Dots.color = #red
#                    \once \override NoteHead.color = #red
#                    \once \override Stem.color = #red
#                    a'8
#                }
#
#            ::
#
#                >>> selector.print(selector, result)
#                Selection([Note("c'8"), Rest('r8')])
#                Selection([Note("d'8"), Note("e'8"), Rest('r8')])
#                Selection([Note("f'8"), Note("g'8"), Note("a'8")])
#
#        ..  container:: example
#
#            Selects pitched tails (with next leaf):
#
#            ::
#
#                >>> selector = abjad.select()
#                >>> selector = selector.by_logical_tie(pitched=True)
#                >>> get = abjad.select()[-1].with_next_leaf()
#                >>> selector = selector.map(get)
#
#            ::
#
#                >>> staff = abjad.Staff(r"c'8 r d' ~ d' e' ~ e' r8 f'8")
#                >>> result = selector(staff)
#                >>> selector.color(result)
#                >>> abjad.setting(staff).auto_beaming = False
#                >>> show(staff) # doctest: +SKIP
#
#            ..  docs::
#
#                >>> f(staff)
#                \new Staff \with {
#                    autoBeaming = ##f
#                } {
#                    \once \override Accidental.color = #red
#                    \once \override Beam.color = #red
#                    \once \override Dots.color = #red
#                    \once \override NoteHead.color = #red
#                    \once \override Stem.color = #red
#                    c'8
#                    \once \override Dots.color = #red
#                    \once \override Rest.color = #red
#                    r8
#                    d'8 ~
#                    \once \override Accidental.color = #blue
#                    \once \override Beam.color = #blue
#                    \once \override Dots.color = #blue
#                    \once \override NoteHead.color = #blue
#                    \once \override Stem.color = #blue
#                    d'8
#                    \once \override Accidental.color = #blue
#                    \once \override Beam.color = #blue
#                    \once \override Dots.color = #blue
#                    \once \override NoteHead.color = #blue
#                    \once \override Stem.color = #blue
#                    e'8 ~
#                    \once \override Accidental.color = #red
#                    \once \override Beam.color = #red
#                    \once \override Dots.color = #red
#                    \once \override NoteHead.color = #red
#                    \once \override Stem.color = #red
#                    e'8
#                    \once \override Dots.color = #red
#                    \once \override Rest.color = #red
#                    r8
#                    \once \override Accidental.color = #blue
#                    \once \override Beam.color = #blue
#                    \once \override Dots.color = #blue
#                    \once \override NoteHead.color = #blue
#                    \once \override Stem.color = #blue
#                    f'8
#                }
#
#            ::
#
#                >>> selector.print(selector, result)
#                Selection([Note("c'8"), Rest('r8')])
#                Selection([Note("d'8"), Note("e'8")])
#                Selection([Note("e'8"), Rest('r8')])
#                Selection([Note("f'8")])
#
#        ..  container:: example
#
#            Selects pitched logical ties (with next leaf). This is the correct
#            selection for single-pitch sustain pedal application:
#
#            ::
#
#                >>> selector = abjad.select()
#                >>> selector = selector.by_logical_tie(pitched=True)
#                >>> selector = selector.map(abjad.select().with_next_leaf())
#
#            ::
#
#                >>> staff = abjad.Staff(r"c'8 r d' ~ d' e' ~ e' r8 f'8")
#                >>> result = selector(staff)
#                >>> for selection in result:
#                ...     abjad.attach(abjad.PianoPedalSpanner(), selection)
#                ...
#
#            ::
#
#                >>> selector.color(result)
#                >>> manager = abjad.override(staff).sustain_pedal_line_spanner
#                >>> manager.staff_padding = 6
#                >>> abjad.setting(staff).auto_beaming = False
#                >>> show(staff) # doctest: +SKIP
#
#            ..  docs::
#
#                >>> f(staff)
#                \new Staff \with {
#                    \override SustainPedalLineSpanner.staff-padding = #6
#                    autoBeaming = ##f
#                } {
#                    \once \override Accidental.color = #red
#                    \once \override Beam.color = #red
#                    \once \override Dots.color = #red
#                    \once \override NoteHead.color = #red
#                    \once \override Stem.color = #red
#                    \set Staff.pedalSustainStyle = #'mixed
#                    c'8 \sustainOn
#                    \once \override Dots.color = #red
#                    \once \override Rest.color = #red
#                    r8 \sustainOff
#                    \once \override Accidental.color = #blue
#                    \once \override Beam.color = #blue
#                    \once \override Dots.color = #blue
#                    \once \override NoteHead.color = #blue
#                    \once \override Stem.color = #blue
#                    \set Staff.pedalSustainStyle = #'mixed
#                    d'8 ~ \sustainOn
#                    \once \override Accidental.color = #blue
#                    \once \override Beam.color = #blue
#                    \once \override Dots.color = #blue
#                    \once \override NoteHead.color = #blue
#                    \once \override Stem.color = #blue
#                    d'8
#                    \once \override Accidental.color = #red
#                    \once \override Beam.color = #red
#                    \once \override Dots.color = #red
#                    \once \override NoteHead.color = #red
#                    \once \override Stem.color = #red
#                    \set Staff.pedalSustainStyle = #'mixed
#                    e'8 ~ \sustainOff \sustainOn
#                    \once \override Accidental.color = #red
#                    \once \override Beam.color = #red
#                    \once \override Dots.color = #red
#                    \once \override NoteHead.color = #red
#                    \once \override Stem.color = #red
#                    e'8
#                    \once \override Dots.color = #red
#                    \once \override Rest.color = #red
#                    r8 \sustainOff
#                    \once \override Accidental.color = #blue
#                    \once \override Beam.color = #blue
#                    \once \override Dots.color = #blue
#                    \once \override NoteHead.color = #blue
#                    \once \override Stem.color = #blue
#                    \set Staff.pedalSustainStyle = #'mixed
#                    f'8 \sustainOn \sustainOff
#                }
#
#            ::
#
#                >>> selector.print(selector, result)
#                Selection([Note("c'8"), Rest('r8')])
#                Selection([Note("d'8"), Note("d'8"), Note("e'8")])
#                Selection([Note("e'8"), Note("e'8"), Rest('r8')])
#                Selection([Note("f'8")])
#
#        Returns new expression.
#        '''
#        import abjad
#        callback = abjad.WithLeafCallback(with_next_leaf=True)
#        selector = self._append_callback(callback)
#        return selector

#    def with_previous_leaf(self):
#        r'''Selects with previous leaf.
#
#        ..  container:: example
#
#            Selects note runs (with previous leaf):
#
#            ::
#
#                >>> selector = abjad.select()
#                >>> selector = selector.by_leaf()
#                >>> selector = selector.by_run(abjad.Note)
#                >>> get = abjad.select().with_previous_leaf()
#                >>> selector = selector.map(get)
#
#            ::
#
#                >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
#                >>> result = selector(staff)
#                >>> selector.color(result)
#                >>> abjad.setting(staff).auto_beaming = False
#                >>> show(staff) # doctest: +SKIP
#
#            ..  docs::
#
#                >>> f(staff)
#                \new Staff \with {
#                    autoBeaming = ##f
#                } {
#                    \once \override Accidental.color = #red
#                    \once \override Beam.color = #red
#                    \once \override Dots.color = #red
#                    \once \override NoteHead.color = #red
#                    \once \override Stem.color = #red
#                    c'8
#                    \once \override Dots.color = #blue
#                    \once \override Rest.color = #blue
#                    r8
#                    \once \override Accidental.color = #blue
#                    \once \override Beam.color = #blue
#                    \once \override Dots.color = #blue
#                    \once \override NoteHead.color = #blue
#                    \once \override Stem.color = #blue
#                    d'8
#                    \once \override Accidental.color = #blue
#                    \once \override Beam.color = #blue
#                    \once \override Dots.color = #blue
#                    \once \override NoteHead.color = #blue
#                    \once \override Stem.color = #blue
#                    e'8
#                    \once \override Dots.color = #red
#                    \once \override Rest.color = #red
#                    r8
#                    \once \override Accidental.color = #red
#                    \once \override Beam.color = #red
#                    \once \override Dots.color = #red
#                    \once \override NoteHead.color = #red
#                    \once \override Stem.color = #red
#                    f'8
#                    \once \override Accidental.color = #red
#                    \once \override Beam.color = #red
#                    \once \override Dots.color = #red
#                    \once \override NoteHead.color = #red
#                    \once \override Stem.color = #red
#                    g'8
#                    \once \override Accidental.color = #red
#                    \once \override Beam.color = #red
#                    \once \override Dots.color = #red
#                    \once \override NoteHead.color = #red
#                    \once \override Stem.color = #red
#                    a'8
#                }
#
#            ::
#
#                >>> selector.print(selector, result)
#                Selection([Note("c'8")])
#                Selection([Rest('r8'), Note("d'8"), Note("e'8")])
#                Selection([Rest('r8'), Note("f'8"), Note("g'8"), Note("a'8")])
#
#        ..  container:: example
#
#            Selects pitched heads (with previous leaf):
#
#            ::
#
#                >>> selector = abjad.select()
#                >>> selector = selector.by_logical_tie(pitched=True)
#                >>> get = abjad.select()[0].with_previous_leaf()
#                >>> selector = selector.map(get)
#
#            ::
#
#                >>> staff = abjad.Staff(r"c'8 r d' ~ d' e' ~ e' r8 f'8")
#                >>> result = selector(staff)
#                >>> selector.color(result)
#                >>> abjad.setting(staff).auto_beaming = False
#                >>> show(staff) # doctest: +SKIP
#
#            ..  docs::
#
#                >>> f(staff)
#                \new Staff \with {
#                    autoBeaming = ##f
#                } {
#                    \once \override Accidental.color = #red
#                    \once \override Beam.color = #red
#                    \once \override Dots.color = #red
#                    \once \override NoteHead.color = #red
#                    \once \override Stem.color = #red
#                    c'8
#                    \once \override Dots.color = #blue
#                    \once \override Rest.color = #blue
#                    r8
#                    \once \override Accidental.color = #blue
#                    \once \override Beam.color = #blue
#                    \once \override Dots.color = #blue
#                    \once \override NoteHead.color = #blue
#                    \once \override Stem.color = #blue
#                    d'8 ~
#                    \once \override Accidental.color = #red
#                    \once \override Beam.color = #red
#                    \once \override Dots.color = #red
#                    \once \override NoteHead.color = #red
#                    \once \override Stem.color = #red
#                    d'8
#                    \once \override Accidental.color = #red
#                    \once \override Beam.color = #red
#                    \once \override Dots.color = #red
#                    \once \override NoteHead.color = #red
#                    \once \override Stem.color = #red
#                    e'8 ~
#                    e'8
#                    \once \override Dots.color = #blue
#                    \once \override Rest.color = #blue
#                    r8
#                    \once \override Accidental.color = #blue
#                    \once \override Beam.color = #blue
#                    \once \override Dots.color = #blue
#                    \once \override NoteHead.color = #blue
#                    \once \override Stem.color = #blue
#                    f'8
#                }
#
#            ::
#
#                >>> selector.print(selector, result)
#                Selection([Note("c'8")])
#                Selection([Rest('r8'), Note("d'8")])
#                Selection([Note("d'8"), Note("e'8")])
#                Selection([Rest('r8'), Note("f'8")])
#
#        Returns new expression.
#        '''
#        import abjad
#        callback = abjad.WithLeafCallback(with_previous_leaf=True)
#        selector = self._append_callback(callback)
#        return selector

#    def wrap(self):
#        r'''Wraps result in list.
#
#        ..  container:: example
#
#            Wraps tuplets:
#
#            ::
#
#                >>> selector = abjad.select()
#                >>> selector = selector.by_class(abjad.Tuplet)
#
#            ::
#
#                >>> staff = abjad.Staff(r"""
#                ...     \times 2/3 { r8 d' e' } f' r
#                ...     r f' \times 2/3 { e' d' r8 }
#                ...     """)
#                >>> result = selector(staff)
#                >>> selector.color(result)
#                >>> abjad.setting(staff).auto_beaming = False
#                >>> show(staff) # doctest: +SKIP
#
#            ..  docs::
#
#                >>> f(staff)
#                \new Staff \with {
#                    autoBeaming = ##f
#                } {
#                    \times 2/3 {
#                        \once \override Dots.color = #red
#                        \once \override Rest.color = #red
#                        r8
#                        \once \override Accidental.color = #red
#                        \once \override Beam.color = #red
#                        \once \override Dots.color = #red
#                        \once \override NoteHead.color = #red
#                        \once \override Stem.color = #red
#                        d'8
#                        \once \override Accidental.color = #red
#                        \once \override Beam.color = #red
#                        \once \override Dots.color = #red
#                        \once \override NoteHead.color = #red
#                        \once \override Stem.color = #red
#                        e'8
#                    }
#                    f'8
#                    r8
#                    r8
#                    f'8
#                    \times 2/3 {
#                        \once \override Accidental.color = #blue
#                        \once \override Beam.color = #blue
#                        \once \override Dots.color = #blue
#                        \once \override NoteHead.color = #blue
#                        \once \override Stem.color = #blue
#                        e'8
#                        \once \override Accidental.color = #blue
#                        \once \override Beam.color = #blue
#                        \once \override Dots.color = #blue
#                        \once \override NoteHead.color = #blue
#                        \once \override Stem.color = #blue
#                        d'8
#                        \once \override Dots.color = #blue
#                        \once \override Rest.color = #blue
#                        r8
#                    }
#                }
#
#            ::
#
#                >>> selector.print(selector, result)
#                Tuplet(Multiplier(2, 3), "r8 d'8 e'8")
#                Tuplet(Multiplier(2, 3), "e'8 d'8 r8")
#
#        ..  container:: example
#
#            Wraps each tuplet:
#
#            ::
#
#                >>> selector = abjad.select()
#                >>> selector = selector.by_class(abjad.Tuplet)
#                >>> selector = selector.map(abjad.select().wrap())
#
#            ::
#
#                >>> staff = abjad.Staff(r"""
#                ...     \times 2/3 { r8 d' e' } f' r
#                ...     r f' \times 2/3 { e' d' r8 }
#                ...     """)
#                >>> result = selector(staff)
#                >>> selector.color(result)
#                >>> abjad.setting(staff).auto_beaming = False
#                >>> show(staff) # doctest: +SKIP
#
#            ..  docs::
#
#                >>> f(staff)
#                \new Staff \with {
#                    autoBeaming = ##f
#                } {
#                    \times 2/3 {
#                        \once \override Dots.color = #red
#                        \once \override Rest.color = #red
#                        r8
#                        \once \override Accidental.color = #red
#                        \once \override Beam.color = #red
#                        \once \override Dots.color = #red
#                        \once \override NoteHead.color = #red
#                        \once \override Stem.color = #red
#                        d'8
#                        \once \override Accidental.color = #red
#                        \once \override Beam.color = #red
#                        \once \override Dots.color = #red
#                        \once \override NoteHead.color = #red
#                        \once \override Stem.color = #red
#                        e'8
#                    }
#                    f'8
#                    r8
#                    r8
#                    f'8
#                    \times 2/3 {
#                        \once \override Accidental.color = #blue
#                        \once \override Beam.color = #blue
#                        \once \override Dots.color = #blue
#                        \once \override NoteHead.color = #blue
#                        \once \override Stem.color = #blue
#                        e'8
#                        \once \override Accidental.color = #blue
#                        \once \override Beam.color = #blue
#                        \once \override Dots.color = #blue
#                        \once \override NoteHead.color = #blue
#                        \once \override Stem.color = #blue
#                        d'8
#                        \once \override Dots.color = #blue
#                        \once \override Rest.color = #blue
#                        r8
#                    }
#                }
#
#            ::
#
#                >>> selector.print(selector, result)
#                [Tuplet(Multiplier(2, 3), "r8 d'8 e'8")]
#                [Tuplet(Multiplier(2, 3), "e'8 d'8 r8")]
#
#        Returns new expression.
#        '''
#        import abjad
#        callback = abjad.WrapCallback()
#        selector = self._append_callback(callback)
#        return selector
