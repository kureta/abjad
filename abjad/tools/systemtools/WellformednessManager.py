from abjad.tools.abctools import AbjadObject


class WellformednessManager(AbjadObject):
    r'''Wellformedness manager.

    ..  container:: example

        ::

            >>> abjad.WellformednessManager()
            WellformednessManager()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Managers'

    __slots__ = (
        '_allow_percussion_clef',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, allow_percussion_clef=None):
        self._allow_percussion_clef = allow_percussion_clef

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls all wellformedness checks on `argument`.

        Returns triples.
        '''
        if argument is None:
            return
        check_names = [_ for _ in dir(self) if _.startswith('check_')]
        triples = []
        for current_check_name in sorted(check_names):
            current_check = getattr(self, current_check_name)
            current_violators, current_total = current_check(argument=argument)
            triple = (current_violators, current_total, current_check_name)
            triples.append(triple)
        return triples

    ### PRIVATE METHODS ###

    def _check_overlapping_spanners(self, argument=None, prototype=None):
        import abjad
        violators, spanners = [], set()
        for leaf in abjad.iterate(argument).by_leaf():
            spanners_ = list(abjad.inspect(leaf).get_spanners(prototype))
            spanners.update(spanners_)
            if 1 < len(spanners_):
                if len(spanners_) == 2:
                    common_leaves = set(spanners_[0].components)
                    common_leaves &= set(spanners_[1].components)
                    if len(common_leaves) == 1:
                        leaf = list(common_leaves)[0]
                        if ((spanners_[0]._is_my_first_leaf(leaf) and
                            spanners_[1]._is_my_last_leaf(leaf)) or
                            (spanners_[1]._is_my_first_leaf(leaf) and
                            spanners_[0]._is_my_last_leaf(leaf))):
                            break
                for spanner_ in spanners_:
                    if spanner_ not in violators:
                        violators.append(spanner_)
        return violators, len(spanners)

    ### PUBLIC PROPERTIES ###

    @property
    def allow_percussion_clef(self):
        r'''Is true when manager allows percussion clef. Otherwise false.

        Returns true, false or none.
        '''
        return self._allow_percussion_clef

    ### PUBLIC METHODS ###

    def check_beamed_quarter_notes(self, argument=None):
        r'''Checks to make sure there are no beamed quarter notes.

        Returns list of beamed quarter notes and count of all quarter notes in
        `argument`.
        '''
        import abjad
        violators, total = [], 0
        smart_beams = (
            abjad.DuratedComplexBeam,
            abjad.MultipartBeam,
            )
        for leaf in abjad.iterate(argument).by_leaf():
            if leaf.written_duration < abjad.Duration(1, 4):
                continue
            total += 1
            beams = abjad.inspect(leaf).get_spanners(abjad.Beam)
            for beam in beams:
                if isinstance(beam, smart_beams):
                    continue
                violators.append(leaf)
        return violators, total

    def check_discontiguous_spanners(self, argument=None):
        r'''Checks for discontiguous spanners.

        There are now two different types of spanner. Most spanners demand that
        spanner components be logical-voice-contiguous. But a few special
        spanners (like MetronomeMark) do not make such a demand. The check here
        consults the experimental `_contiguity_constraint`.

        Returns list of discontiguous spanners and nonnegative integer count of
        all spanners in `argument`.
        '''
        import abjad
        violators = []
        descendants = abjad.inspect(argument).get_descendants()
        spanners = descendants._get_spanners()
        for spanner in spanners:
            if spanner._contiguity_constraint == 'logical voice':
                if not abjad.Selection._all_in_same_logical_voice(
                    spanner[:],
                    contiguous=True,
                    ):
                    violators.append(spanner)
        return violators, len(spanners)

    def check_duplicate_ids(self, argument=None):
        r'''Checks to make sure there are no components with duplicated IDs.

        Returns violators and total.
        '''
        import abjad
        violators = []
        components = abjad.iterate(argument).by_class()
        total_ids = [id(_) for _ in components]
        unique_ids = abjad.Sequence(total_ids).remove_repeats()
        if len(unique_ids) < len(total_ids):
            for current_id in unique_ids:
                if 1 < total_ids.count(current_id):
                    violators.extend([_ for _ in components
                        if id(_) == current_id])
        return violators, len(total_ids)

    def check_empty_containers(self, argument=None):
        r'''Checks to make sure there are no empty containers in score.

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'4 d' e' f'")
                >>> staff.append(abjad.Container())

            ::

                >>> f(staff)
                \new Staff {
                    c'4
                    d'4
                    e'4
                    f'4
                    {
                    }
                }

            ::

                >>> manager = abjad.WellformednessManager()
                >>> result = manager.check_empty_containers(staff)
                >>> violators, total = result

            ::

                >>> '{} total containers'.format(total)
                '2 total containers'

            ::

                >>> '{} empty container'.format(len(violators))
                '1 empty container'

        Returns list of empty containers and count of all containers in
        `argument`.
        '''
        import abjad
        violators, containers = [], set()
        for container in abjad.iterate(argument).by_class(abjad.Container):
            containers.add(container)
            if len(container) == 0:
                violators.append(container)
        return violators, len(containers)

    def check_intermarked_hairpins(self, argument=None):
        r'''Checks to make sure there are no hairpins with intervening dynamic
        marks.

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'4 d' e' f'")
                >>> abjad.attach(abjad.Hairpin('<'), staff[:])
                >>> abjad.attach(abjad.Dynamic('f'), staff[2])

            ::

                >>> f(staff)
                \new Staff {
                    c'4 \<
                    d'4
                    e'4 \f
                    f'4 \!
                }

            ::

                >>> manager = abjad.WellformednessManager()
                >>> result = manager.check_intermarked_hairpins(staff)
                >>> violators, total = result

            ::

                >>> '{} total hairpin'.format(total)
                '1 total hairpin'

            ::

                >>> '{} intermarked hairpin'.format(len(violators))
                '1 intermarked hairpin'

        Returns violators and total.
        '''
        import abjad
        violators, hairpins = [], set()
        descendants = abjad.inspect(argument).get_descendants()
        hairpins = descendants._get_spanners(abjad.Hairpin)
        for hairpin in hairpins:
            if 2 < len(hairpin.components):
                for leaf in hairpin.components[1:-1]:
                    if abjad.inspect(leaf).get_indicators(abjad.Dynamic):
                        violators.append(hairpin)
                        break
        return violators, len(hairpins)

    def check_misdurated_measures(self, argument=None):
        r'''Checks to make sure there are no misdurated measures in score.

        Returns violators and total.
        '''
        import abjad
        violators = []
        total, bad = 0, 0
        for measure in abjad.iterate(argument).by_class(abjad.Measure):
            time_signature = measure.time_signature
            if time_signature is not None:
                if measure._get_preprolated_duration() != \
                    time_signature.duration:
                    violators.append(measure)
                    bad += 1
            total += 1
        return violators, total

    def check_misfilled_measures(self, argument=None):
        r'''Checks that time signature duration equals measure contents
        duration for every measure.

        Returns violators and total.
        '''
        import abjad
        violators = []
        total, bad = 0, 0
        for measure in abjad.iterate(argument).by_class(abjad.Measure):
            if measure.is_misfilled:
                violators.append(measure)
                bad += 1
            total += 1
        return violators, total

    def check_mismatched_enchained_hairpins(self, argument=None):
        r'''Checks mismatched enchained hairpins.

        ..  container:: example

            Checks mismatched enchained hairpins:

            ::

                >>> staff = abjad.Staff("c'4 d' e' f'")
                >>> abjad.attach(abjad.Hairpin('p < f'), staff[:2])
                >>> abjad.attach(abjad.Hairpin('p > pp'), staff[1:])

            ::

                >>> agent = abjad.inspect(staff)
                >>> print(agent.tabulate_well_formedness_violations())
                0 /	4 beamed quarter notes
                0 /	2 discontiguous spanners
                0 /	5 duplicate ids
                0 /     1 empty containers
                0 /	2 intermarked hairpins
                0 /	0 misdurated measures
                0 /	0 misfilled measures
                2 /	2 mismatched enchained hairpins
                0 /	0 mispitched ties
                0 /	4 misrepresented flags
                0 /	5 missing parents
                0 /	0 nested measures
                0 /     4 notes on wrong clef
                0 /     4 out of range notes
                0 /	0 overlapping beams
                0 /	0 overlapping glissandi
                0 /	2 overlapping hairpins
                0 /	0 overlapping octavation spanners
                0 /	0 overlapping ties
                0 /     0 overlapping trill spanners 
                0 /	2 short hairpins
                0 /	0 tied rests

        Enchained hairpins are fine so long as hairpin ends match.

        Returns violators and total.
        '''
        import abjad
        violators = []
        all_hairpins = set()
        for leaf in abjad.iterate(argument).by_leaf():
            hairpins = abjad.inspect(leaf).get_spanners(abjad.Hairpin)
            hairpins = list(hairpins)
            all_hairpins.update(hairpins)
            if len(hairpins) <= 1:
                continue
            if 2 < len(hairpins):
                raise Exception('too many hairpins')
            assert len(hairpins) == 2
            hairpins_are_enchained = False
            if (hairpins[0]._is_my_last_leaf(leaf) and
                hairpins[-1]._is_my_first_leaf(leaf)):
                hairpins_are_enchained = True
            if (hairpins[-1]._is_my_last_leaf(leaf) and
                hairpins[0]._is_my_first_leaf(leaf)):
                hairpins_are_enchained = True
            if not hairpins_are_enchained:
                continue
            if hairpins[0]._is_my_first_leaf(leaf):
                first_hairpin = hairpins[-1]
                second_hairpin = hairpins[0]
            else:
                first_hairpin = hairpins[0]
                second_hairpin = hairpins[-1]
            if first_hairpin.stop_dynamic == second_hairpin.start_dynamic:
                continue
            else:
                violators.append(first_hairpin)
                violators.append(second_hairpin)
        total = len(all_hairpins)
        return violators, total

    def check_mispitched_ties(self, argument=None):
        r'''Checks for mispitched notes.

        ..  container:: example

            Checks for mispitched ties attached to notes:

            ::

                >>> staff = abjad.Staff("c'4 ~ c'")
                >>> staff[1].written_pitch = abjad.NamedPitch("d'")

            ::

                >>> agent = abjad.inspect(staff)
                >>> print(agent.tabulate_well_formedness_violations())
                0 /	2 beamed quarter notes
                0 /	1 discontiguous spanners
                0 /	3 duplicate ids
                0 /     1 empty containers
                0 /	0 intermarked hairpins
                0 /	0 misdurated measures
                0 /	0 misfilled measures
                0 /	0 mismatched enchained hairpins
                1 /	1 mispitched ties
                0 /	2 misrepresented flags
                0 /	3 missing parents
                0 /	0 nested measures
                0 /     2 notes on wrong clef
                0 /     2 out of range notes
                0 /	0 overlapping beams
                0 /	0 overlapping glissandi
                0 /	0 overlapping hairpins
                0 /	0 overlapping octavation spanners
                0 /	1 overlapping ties
                0 /     0 overlapping trill spanners
                0 /	0 short hairpins
                0 /	0 tied rests

        ..  container:: example

            Checks for mispitched ties attached to chords:

            ::

                >>> staff = abjad.Staff("<c' d' bf'>4 ~ <c' d' bf'>")
                >>> staff[1].written_pitches = [6, 9, 10]

            ::

                >>> agent = abjad.inspect(staff)
                >>> print(agent.tabulate_well_formedness_violations())
                0 /	2 beamed quarter notes
                0 /	1 discontiguous spanners
                0 /	3 duplicate ids
                0 /     1 empty containers
                0 /	0 intermarked hairpins
                0 /	0 misdurated measures
                0 /	0 misfilled measures
                0 /	0 mismatched enchained hairpins
                1 /	1 mispitched ties
                0 /	2 misrepresented flags
                0 /	3 missing parents
                0 /	0 nested measures
                0 /     2 notes on wrong clef
                0 /     2 out of range notes
                0 /	0 overlapping beams
                0 /	0 overlapping glissandi
                0 /	0 overlapping hairpins
                0 /	0 overlapping octavation spanners
                0 /	1 overlapping ties
                0 /     0 overlapping trill spanners
                0 /	0 short hairpins
                0 /	0 tied rests

        Does not check tied rests, chords or skips.

        Returns violator ties together with total number of ties.
        '''
        import abjad
        violators = set()
        all_spanners = set()
        for leaf in abjad.iterate(argument).by_leaf(pitched=True):
            spanners = abjad.inspect(leaf).get_spanners(abjad.Tie)
            if not spanners:
                continue
            all_spanners.update(spanners)
            spanner = spanners.pop()
            written_pitches = []
            for leaf in spanner:
                if isinstance(leaf, abjad.Note):
                    written_pitches.append(leaf.written_pitch)
                elif isinstance(leaf, abjad.Chord):
                    written_pitches.append(leaf.written_pitches)
                else:
                    raise TypeError(leaf)
            if not abjad.mathtools.all_are_equal(written_pitches):
                violators.add(spanner)
        violators = list(violators)
        total = len(all_spanners)
        return violators, total

    def check_misrepresented_flags(self, argument=None):
        r'''Checks to make sure there are no misrepresented flags in score.

        Returns violators and total.
        '''
        import abjad
        violators = []
        total = 0
        for leaf in abjad.iterate(argument).by_leaf():
            total += 1
            flags = leaf.written_duration.flag_count
            left = getattr(abjad.setting(leaf), 'stem_left_beam_count', None)
            right = getattr(abjad.setting(leaf), 'stem_right_beam_count', None)
            if left is not None:
                if (flags < left or
                    (left < flags and right not in (flags, None))):
                    if leaf not in violators:
                        violators.append(leaf)
            if right is not None:
                if (flags < right or
                    (right < flags and left not in (flags, None))):
                    if leaf not in violators:
                        violators.append(leaf)
        return violators, total

    def check_missing_parents(self, argument=None):
        r'''Checks to make sure there are no components in score with missing
        parent.

        Returns violators and total.
        '''
        import abjad
        violators = []
        total = 0
        components = abjad.iterate(argument).by_class()
        for i, component in enumerate(components):
            if 0 < i:
                if component._parent is None:
                    violators.append(component)
        total = i + 1
        return violators, total

    def check_nested_measures(self, argument=None):
        r'''Checks to make sure there are no nested measures in score.

        Returns violators and total.
        '''
        import abjad
        violators = []
        total = 0
        for measure in abjad.iterate(argument).by_class(abjad.Measure):
            parentage = abjad.inspect(measure).get_parentage(include_self=False)
            if parentage.get_first(abjad.Measure):
                violators.append(measure)
            total += 1
        return violators, total

    def check_notes_on_wrong_clef(self, argument=None):
        r'''Checks notes and chords on wrong clef.

        ..  container:: example

            ::

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> clef = abjad.Clef('alto')
                >>> abjad.attach(clef, staff[0])
                >>> violin = abjad.instrumenttools.Violin()
                >>> abjad.attach(violin, staff[0])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \set Staff.instrumentName = \markup { Violin }
                    \set Staff.shortInstrumentName = \markup { Vn. }
                    \clef "alto"
                    c'8
                    d'8
                    e'8
                    f'8
                }

            ::

                >>> agent = abjad.inspect(staff)
                >>> print(agent.tabulate_well_formedness_violations())
                0 /	0 beamed quarter notes
                0 /	0 discontiguous spanners
                0 /	5 duplicate ids
                0 /	1 empty containers
                0 /	0 intermarked hairpins
                0 /	0 misdurated measures
                0 /	0 misfilled measures
                0 /	0 mismatched enchained hairpins
                0 /	0 mispitched ties
                0 /	4 misrepresented flags
                0 /	5 missing parents
                0 /	0 nested measures
                4 /	4 notes on wrong clef
                0 /	4 out of range notes
                0 /	0 overlapping beams
                0 /	0 overlapping glissandi
                0 /	0 overlapping hairpins
                0 /	0 overlapping octavation spanners
                0 /	0 overlapping ties
                0 /     0 overlapping trill spanners
                0 /	0 short hairpins
                0 /	0 tied rests

        ..  container:: example

            Allows percussion clef:

            ::

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> clef = abjad.Clef('percussion')
                >>> abjad.attach(clef, staff[0])
                >>> violin = abjad.instrumenttools.Violin()
                >>> abjad.attach(violin, staff[0])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \set Staff.instrumentName = \markup { Violin }
                    \set Staff.shortInstrumentName = \markup { Vn. }
                    \clef "percussion"
                    c'8
                    d'8
                    e'8
                    f'8
                }

            ::

                >>> agent = abjad.inspect(staff)
                >>> print(agent.tabulate_well_formedness_violations(
                ...     allow_percussion_clef=True,
                ...     ))
                0 /	0 beamed quarter notes
                0 /	0 discontiguous spanners
                0 /	5 duplicate ids
                0 /	1 empty containers
                0 /	0 intermarked hairpins
                0 /	0 misdurated measures
                0 /	0 misfilled measures
                0 /	0 mismatched enchained hairpins
                0 /	0 mispitched ties
                0 /	4 misrepresented flags
                0 /	5 missing parents
                0 /	0 nested measures
                0 /	4 notes on wrong clef
                0 /	4 out of range notes
                0 /	0 overlapping beams
                0 /	0 overlapping glissandi
                0 /	0 overlapping hairpins
                0 /	0 overlapping octavation spanners
                0 /	0 overlapping ties
                0 /     0 overlapping trill spanners
                0 /	0 short hairpins
                0 /	0 tied rests

        ..  container:: example

            Forbids percussion clef:

            ::

                >>> agent = abjad.inspect(staff)
                >>> print(agent.tabulate_well_formedness_violations(
                ...     allow_percussion_clef=False,
                ...     ))
                0 /	0 beamed quarter notes
                0 /	0 discontiguous spanners
                0 /	5 duplicate ids
                0 /	1 empty containers
                0 /	0 intermarked hairpins
                0 /	0 misdurated measures
                0 /	0 misfilled measures
                0 /	0 mismatched enchained hairpins
                0 /	0 mispitched ties
                0 /	4 misrepresented flags
                0 /	5 missing parents
                0 /	0 nested measures
                4 /	4 notes on wrong clef
                0 /	4 out of range notes
                0 /	0 overlapping beams
                0 /	0 overlapping glissandi
                0 /	0 overlapping hairpins
                0 /	0 overlapping octavation spanners
                0 /	0 overlapping ties
                0 /     0 overlapping trill spanners
                0 /	0 short hairpins
                0 /	0 tied rests

        Returns true or false.
        '''
        import abjad
        violators = []
        total = 0
        for leaf in abjad.iterate(argument).by_leaf():
            total += 1
            instrument = abjad.inspect(leaf).get_effective(abjad.Instrument)
            if instrument is None:
                continue
            clef = abjad.inspect(leaf).get_effective(abjad.Clef)
            if clef is None:
                continue
            allowable_clefs = [
                abjad.Clef(_) for _ in instrument.allowable_clefs
                ]
            if self.allow_percussion_clef:
                allowable_clefs.append(abjad.Clef('percussion'))
            if clef not in allowable_clefs:
                violators.append(leaf)
        return violators, total

    def check_out_of_range_notes(self, argument=None):
        r'''Checks to make sure notes and chords are within traditional
        instrument ranges.

        ..  container:: example

            Out of range:

            ::

                >>> staff = abjad.Staff("c'8 r8 <d fs>8 r8")
                >>> violin = abjad.instrumenttools.Violin()
                >>> abjad.attach(violin, staff[0])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \set Staff.instrumentName = \markup { Violin }
                    \set Staff.shortInstrumentName = \markup { Vn. }
                    c'8
                    r8
                    <d fs>8
                    r8
                }

            ::

                >>> agent = abjad.inspect(staff)
                >>> print(agent.tabulate_well_formedness_violations())
                0 /	0 beamed quarter notes
                0 /	0 discontiguous spanners
                0 /	5 duplicate ids
                0 /	1 empty containers
                0 /	0 intermarked hairpins
                0 /	0 misdurated measures
                0 /	0 misfilled measures
                0 /	0 mismatched enchained hairpins
                0 /	0 mispitched ties
                0 /	4 misrepresented flags
                0 /	5 missing parents
                0 /	0 nested measures
                0 /	4 notes on wrong clef
                1 /	2 out of range notes
                0 /	0 overlapping beams
                0 /	0 overlapping glissandi
                0 /	0 overlapping hairpins
                0 /	0 overlapping octavation spanners
                0 /	0 overlapping ties
                0 /     0 overlapping trill spanners
                0 /	0 short hairpins
                0 /	2 tied rests

        Returns true or false.
        '''
        import abjad
        violators = []
        all_pitched_leaves = []
        for leaf in abjad.iterate(argument).by_leaf(pitched=True):
            all_pitched_leaves.append(leaf)
            instrument = abjad.inspect(leaf).get_effective(abjad.Instrument)
            if instrument is None:
                continue
            if leaf not in instrument.pitch_range:
                violators.append(leaf)
        total = len(all_pitched_leaves)
        return violators, total

    def check_overlapping_beams(self, argument=None):
        r'''Checks to make sure there are no overlapping beams in score.

        ..  container:: example

            Overlapping beams are well-formed:

            ::

                >>> staff = abjad.Staff("c'8 d' e' f'")
                >>> abjad.attach(abjad.Beam(), staff[:3])
                >>> abjad.attach(abjad.Beam(), staff[2:])

            ::

                >>> f(staff)
                \new Staff {
                    c'8 [
                    d'8
                    e'8 ] [
                    f'8 ]
                }

            ::

                >>> manager = abjad.WellformednessManager()
                >>> violators, total = manager.check_overlapping_beams(staff)
                >>> '{} overlapping beams'.format(total)
                '2 overlapping beams'

            (Enchained beams are not well-formed either.)

        Returns list of overlapping beams and nonnegative integer count of
        total beams in score.
        '''
        import abjad
        violators = []
        all_beams = set()
        for leaf in abjad.iterate(argument).by_leaf():
            beams = abjad.inspect(leaf).get_spanners(abjad.Beam)
            all_beams.update(beams)
            if 1 < len(beams):
                for beam in beams:
                    if beam not in violators:
                        violators.append(beam)
        total = len(all_beams)
        return violators, total

    def check_overlapping_glissandi(self, argument=None):
        r'''Checks to make sure there are no overlapping glissandi in score.

        Returns violators and total.
        '''
        import abjad
        violators = []
        all_spanners = set()
        for leaf in abjad.iterate(argument).by_leaf():
            glissandi = abjad.inspect(leaf).get_spanners(abjad.Glissando)
            glissandi = list(glissandi)
            all_spanners.update(glissandi)
            if 1 < len(glissandi):
                if len(glissandi) == 2:
                    common_leaves = set(glissandi[0]._get_leaves())
                    common_leaves &= set(glissandi[1]._get_leaves())
                    if len(common_leaves) == 1:
                        leaf = list(common_leaves)[0]
                        if ((glissandi[0]._is_my_first_leaf(leaf) and
                            glissandi[1]._is_my_last_leaf(leaf)) or
                            (glissandi[1]._is_my_first_leaf(leaf) and
                            glissandi[0]._is_my_last_leaf(leaf))):
                            break
                for glissando in glissandi:
                    if glissando not in violators:
                        violators.append(glissando)
        total = len(all_spanners)
        return violators, total

    def check_overlapping_hairpins(self, argument=None):
        r'''Checks to make sure there are no overlapping hairpins in score.

        ..  container:: example

            Checks overlapping hairpins:

            ::

                >>> staff = abjad.Staff("c'4 d' e' f'")
                >>> abjad.attach(abjad.Hairpin('<'), staff[:])
                >>> abjad.attach(abjad.Hairpin('>'), staff[:])

            ::

                >>> agent = abjad.inspect(staff)
                >>> print(agent.tabulate_well_formedness_violations())
                0 /	4 beamed quarter notes
                0 /	2 discontiguous spanners
                0 /	5 duplicate ids
                0 /     1 empty containers
                0 /	2 intermarked hairpins
                0 /	0 misdurated measures
                0 /	0 misfilled measures
                0 /	2 mismatched enchained hairpins
                0 /	0 mispitched ties
                0 /	4 misrepresented flags
                0 /	5 missing parents
                0 /	0 nested measures
                0 /	4 notes on wrong clef
                0 /	4 out of range notes
                0 /	0 overlapping beams
                0 /	0 overlapping glissandi
                2 /	2 overlapping hairpins
                0 /	0 overlapping octavation spanners
                0 /	0 overlapping ties
                0 /     0 overlapping trill spanners
                0 /	2 short hairpins
                0 /	0 tied rests

        Enchained hairpins are fine so long as hairpin ends match.

        Returns violators and total.
        '''
        import abjad
        return self._check_overlapping_spanners(
            argument=argument,
            prototype=abjad.Hairpin,
            )

    def check_overlapping_octavation_spanners(self, argument=None):
        r'''Checks to make sure there are no overlapping octavation spanners in
        score.

        Returns violators and total.
        '''
        import abjad
        violators = []
        all_spanners = set()
        prototype = abjad.OctavationSpanner
        for leaf in abjad.iterate(argument).by_leaf():
            spanners = abjad.inspect(leaf).get_spanners(prototype)
            all_spanners.update(spanners)
            if 1 < len(spanners):
                for spanner in spanners:
                    if spanner not in violators:
                        violators.append(spanner)
        total = len(all_spanners)
        return violators, total

    def check_overlapping_ties(self, argument=None):
        r'''Checks to make sure there are no overlapping ties in score.

        ..  container:: example

            Checks overlapping ties:

            ::

                >>> staff = abjad.Staff("c'4 c' c' c''")
                >>> abjad.attach(abjad.Tie(), staff[:2])
                >>> tie = abjad.Tie()
                >>> tie._ignore_attachment_test = True
                >>> abjad.attach(tie, staff[1:3])

            ::

                >>> agent = abjad.inspect(staff)
                >>> print(agent.tabulate_well_formedness_violations())
                0 /	4 beamed quarter notes
                0 /	2 discontiguous spanners
                0 /	5 duplicate ids
                0 /     1 empty containers
                0 /	0 intermarked hairpins
                0 /	0 misdurated measures
                0 /	0 misfilled measures
                0 /	0 mismatched enchained hairpins
                0 /	2 mispitched ties
                0 /	4 misrepresented flags
                0 /	5 missing parents
                0 /	0 nested measures
                0 /	4 notes on wrong clef
                0 /	4 out of range notes
                0 /	0 overlapping beams
                0 /	0 overlapping glissandi
                0 /	0 overlapping hairpins
                0 /	0 overlapping octavation spanners
                2 /	2 overlapping ties
                0 /     0 overlapping trill spanners
                0 /	0 short hairpins
                0 /	0 tied rests

        Returns violators and count of total ties.
        '''
        import abjad
        total = set()
        violators = set()
        for leaf in abjad.iterate(argument).by_leaf():
            spanners = leaf._get_spanners(abjad.Tie)
            total.update(spanners)
            if 1 < len(spanners):
                violators.update(spanners)
        return violators, len(total)

    def check_overlapping_trill_spanners(self, argument=None):
        r'''Checks to make sure there are no overlapping trill spanners in
        score.

        ..  container:: example

            Enchained trill spanners are ok:

            ::

                >>> staff = abjad.Staff("c'4 d' e' f'")
                >>> abjad.attach(abjad.TrillSpanner(), staff[:3])
                >>> abjad.attach(abjad.TrillSpanner(), staff[2:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    c'4 \startTrillSpan
                    d'4
                    e'4 \stopTrillSpan \startTrillSpan
                    f'4 \stopTrillSpan
                }

            ::

                >>> abjad.inspect(staff).is_well_formed()
                True

        ..  container:: example

            Overlapping trill spanners are not well-formed:

            ::

                >>> staff = abjad.Staff("c'4 d' e' f'")
                >>> abjad.attach(abjad.TrillSpanner(), staff[:])
                >>> abjad.attach(abjad.TrillSpanner(), staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    c'4 \startTrillSpan \startTrillSpan
                    d'4
                    e'4
                    f'4 \stopTrillSpan \stopTrillSpan
                }

            ::

                >>> agent = abjad.inspect(staff)
                >>> print(agent.tabulate_well_formedness_violations())
                0 /	4 beamed quarter notes
                0 /	2 discontiguous spanners
                0 /	5 duplicate ids
                0 /	1 empty containers
                0 /	0 intermarked hairpins
                0 /	0 misdurated measures
                0 /	0 misfilled measures
                0 /	0 mismatched enchained hairpins
                0 /	0 mispitched ties
                0 /	4 misrepresented flags
                0 /	5 missing parents
                0 /	0 nested measures
                0 /	4 notes on wrong clef
                0 /	4 out of range notes
                0 /	0 overlapping beams
                0 /	0 overlapping glissandi
                0 /	0 overlapping hairpins
                0 /	0 overlapping octavation spanners
                0 /	0 overlapping ties
                2 /	2 overlapping trill spanners
                0 /	0 short hairpins
                0 /	0 tied rests

        Enchained hairpins are fine so long as hairpin ends match.

        Returns violators and total.
        '''
        import abjad
        return self._check_overlapping_spanners(
            argument=argument,
            prototype=abjad.TrillSpanner,
            )

    def check_short_hairpins(self, argument=None):
        r'''Checks to make sure that hairpins span at least two leaves.

        Returns violators and total.
        '''
        import abjad
        violators = []
        total = 0
        hairpins = argument._get_descendants()._get_spanners(abjad.Hairpin)
        for hairpin in hairpins:
            if len(hairpin._get_leaves()) <= 1:
                violators.append(hairpin)
            total += 1
        return violators, total

    def check_tied_rests(self, argument=None):
        r'''Checks to make sure there are no tied rests.

        Returns violators and total.
        '''
        import abjad
        violators = []
        total = 0
        for rest in abjad.iterate(argument).by_leaf(abjad.Rest):
            if abjad.inspect(rest).has_spanner(abjad.Tie):
                violators.append(rest)
            total += 1
        return violators, total
