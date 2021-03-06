from .Spanner import Spanner


class TextSpanner(Spanner):
    r'''Text spanner.

    ..  container:: example

        Text spanner with no grob overrides:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> text_spanner = abjad.TextSpanner()
        >>> abjad.attach(text_spanner, staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                c'4 \startTextSpan
                d'4
                e'4
                f'4 \stopTextSpan
            }

        This is (notationally unlikely) default behavior.

    ..  container:: example

        Text spanner with grob override for left text:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> text_spanner = abjad.TextSpanner()
        >>> markup = abjad.Markup('foo').italic().bold()
        >>> abjad.override(text_spanner).text_spanner.bound_details__left__text = markup
        >>> abjad.override(text_spanner).text_spanner.bound_details__left__stencil_align_dir_y = 0
        >>> abjad.attach(text_spanner, staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \override TextSpanner.bound-details.left.stencil-align-dir-y = #0
                \override TextSpanner.bound-details.left.text = \markup {
                    \bold
                        \italic
                            foo
                    }
                c'4 \startTextSpan
                d'4
                e'4
                \revert TextSpanner.bound-details
                f'4 \stopTextSpan
            }

    ..  container:: example

        Text spanner interacting with piecewise markup. At beginning of
        spanner:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> spanner = abjad.TextSpanner()
        >>> abjad.attach(spanner, staff[:])
        >>> spanner.attach(abjad.Markup('pont.'), staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                c'4 ^ \markup { pont. }
                d'4
                e'4
                f'4
            }

        Text spanner is suppresssed and only the markup appears.

    ..  container:: example

        Text spanner interacting with piecewise markup. At end of spanner:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> spanner = abjad.TextSpanner()
        >>> abjad.attach(spanner, staff[:])
        >>> spanner.attach(abjad.Markup('tasto'), staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                c'4
                d'4
                e'4
                f'4 ^ \markup { tasto }
            }

        Text spanner is suppresssed and only the markup appears.

    ..  container:: example

        Text spanner interacting with piecewise markup. At beginning and
        end of spanner:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> spanner = abjad.TextSpanner()
        >>> abjad.attach(spanner, staff[:])
        >>> spanner.attach(abjad.Markup('pont.'), staff[0])
        >>> spanner.attach(abjad.Markup('tasto'), staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                c'4 ^ \markup { pont. }
                d'4
                e'4
                f'4 ^ \markup { tasto }
            }

        Text spanner is suppresssed and only the markup appear.

    ..  container:: example

        Text spanner interacting with piecewise indicators:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> spanner = abjad.TextSpanner()
        >>> abjad.attach(spanner, staff[:])
        >>> spanner.attach(abjad.Markup('one'), staff[0])
        >>> spanner.attach(abjad.LineSegment(), staff[0])
        >>> spanner.attach(abjad.Markup('two'), staff[1])
        >>> spanner.attach(abjad.ArrowLineSegment(), staff[1])
        >>> spanner.attach(abjad.Markup('three'), staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \once \override TextSpanner.bound-details.left.text = \markup { one }
                c'4 \startTextSpan
                \once \override TextSpanner.arrow-width = 0.25
                \once \override TextSpanner.bound-details.left-broken.text = ##f
                \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                \once \override TextSpanner.bound-details.left.text = \markup {
                    \concat
                        {
                            two
                            \hspace
                                #0.25
                        }
                    }
                \once \override TextSpanner.bound-details.right-broken.padding = 0
                \once \override TextSpanner.bound-details.right.arrow = ##t
                \once \override TextSpanner.bound-details.right.padding = 1.5
                \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                \once \override TextSpanner.dash-fraction = 1
                d'4 \stopTextSpan \startTextSpan
                e'4
                f'4 \stopTextSpan ^ \markup { three }
            }

    ..  container:: example

        Text spanner interacting with piecewise and nonpiecewise indicators:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> spanner = abjad.TextSpanner()
        >>> abjad.attach(spanner, staff[:])
        >>> spanner.attach(abjad.Markup('ord.'), staff[0])
        >>> spanner.attach(abjad.ArrowLineSegment(), staff[0])
        >>> spanner.attach(abjad.Markup('pont.'), staff[-1])
        >>> abjad.attach(abjad.Markup('leggieriss.'), staff[0])

        >>> abjad.override(staff).text_spanner.staff_padding = 2.5
        >>> abjad.override(staff).text_script.staff_padding = 2
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff \with {
                    \override TextScript.staff-padding = #2
                    \override TextSpanner.staff-padding = #2.5
            } {
                \once \override TextSpanner.arrow-width = 0.25
                \once \override TextSpanner.bound-details.left-broken.text = ##f
                \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                \once \override TextSpanner.bound-details.left.text = \markup {
                    \concat
                        {
                            ord.
                            \hspace
                                #0.25
                        }
                    }
                \once \override TextSpanner.bound-details.right-broken.padding = 0
                \once \override TextSpanner.bound-details.right.arrow = ##t
                \once \override TextSpanner.bound-details.right.padding = 1.5
                \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                \once \override TextSpanner.dash-fraction = 1
                c'4 \startTextSpan - \markup { leggieriss. }
                d'4
                e'4
                f'4 \stopTextSpan ^ \markup { pont. }
            }

    ..  container:: example

        Raises exception on fewer than two leaves:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> spanner = abjad.TextSpanner()
        >>> abjad.attach(spanner, staff[:1])
        Traceback (most recent call last):
            ...
        Exception: TextSpanner() attachment test fails for Selection([Note("c'4")]).

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_skip_attachment_test_all',
        )

    ### INITIALIZER ###

    def __init__(self, overrides=None):
        Spanner.__init__(self, overrides=overrides)
        self._skip_attachment_test_all = False

    ### PRIVATE METHODS ###

    def _attachment_test_all(self, argument):
        if self._skip_attachment_test_all:
            return True
        return self._at_least_two_leaves(argument)

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = self._get_basic_lilypond_format_bundle(component)
        current_indicators = self._get_piecewise(component)
        current_markups = current_indicators[0]
        current_markup = bool(current_markups)
        current_line_segment = current_indicators[1]
        start_spanner = self._spanner_starts_on_leaf(component)
        stop_spanner = self._spanner_stops_on_leaf(component)
        if start_spanner:
            string = r'\startTextSpan'
            bundle.right.spanner_starts.append(string)
        if stop_spanner:
            string = r'\stopTextSpan'
            bundle.right.spanner_stops.append(string)
        if current_markups is not None:
            # assign markup to spanner left text
            if start_spanner:
                markup = current_markups[0]
                if current_line_segment:
                    if current_line_segment.left_hspace is not None:
                        hspace = current_line_segment.left_hspace
                        hspace = abjad.Markup.hspace(hspace)
                        markup = abjad.Markup.concat([markup, hspace])
                override_ = abjad.LilyPondGrobOverride(
                    grob_name='TextSpanner',
                    once=True,
                    property_path=(
                        'bound-details',
                        'left',
                        'text',
                        ),
                    value=markup,
                    )
                override_string = override_.override_string
                bundle.grob_overrides.append(override_string)
            # format markup normally
            else:
                current_markup = current_markups[0]
                markup = abjad.new(current_markup, direction=abjad.Up)
                string = format(markup, 'lilypond')
                bundle.right.markup.append(string)
        if current_line_segment is not None:
            overrides = current_line_segment._get_lilypond_grob_overrides()
            for override_ in overrides:
                override_string = override_.override_string
                bundle.grob_overrides.append(override_string)
        return bundle

    def _get_piecewise(self, leaf):
        import abjad
        markups = abjad.inspect(leaf).get_piecewise(
            abjad.Markup,
            None,
            )
        if markups is not None:
            markups = [markups]
        line_segment = abjad.inspect(leaf).get_piecewise(
            abjad.LineSegment,
            None,
            )
        return markups, line_segment

    def _get_previous_piecewise(self, component):
        import abjad
        if not isinstance(component, abjad.Leaf):
            return None, None
        leaves = self.leaves
        index = leaves.index(component)
        for index in reversed(range(index)):
            previous_leaf = leaves[index]
            indicators = self._get_piecewise(previous_leaf)
            if any(_ is not None for _ in indicators):
                return indicators
        return None, None

    def _leaf_has_current_event(self, leaf):
        indicators = self._get_piecewise(leaf)
        markup = bool(indicators[0])
        line_segment = bool(indicators[1])
        return markup or line_segment

    def _leaf_has_markup(self, leaf):
        indicators = self._get_piecewise(leaf)
        markup = bool(indicators[0])
        return markup

    def _spanner_has_smart_events(self):
        for leaf in self.leaves:
            if self._leaf_has_current_event(leaf):
                return True
        return False

    def _spanner_is_open_immediately_before_leaf(self, leaf):
        import abjad
        if not isinstance(leaf, abjad.Leaf):
            return False
        leaves = list(self.leaves)
        index = leaves.index(leaf)
        for index in reversed(range(index)):
            previous_leaf = leaves[index]
            if self._spanner_starts_on_leaf(previous_leaf):
                return True
            if self._leaf_has_markup(previous_leaf):
                return False
        return False

    def _spanner_starts_on_leaf(self, leaf):
        indicators = self._get_piecewise(leaf)
        line_segment = indicators[1]
        has_smart_events = self._spanner_has_smart_events()
        if not has_smart_events and self._is_my_first_leaf(leaf):
            return True
        if line_segment:
            return True
        return False

    def _spanner_stops_on_leaf(self, leaf):
        spanner_is_open = self._spanner_is_open_immediately_before_leaf(leaf)
        if spanner_is_open and self._leaf_has_current_event(leaf):
            return True
        if spanner_is_open and self._is_my_last_leaf(leaf):
            return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def overrides(self):
        r'''Gets text spanner overrides.

        ..  container:: example

            Overlapping spanner regression test. Red spanner reverts color
            before default spanner begins:

            >>> staff = abjad.Staff("c'4 d' e' f' c' d' e' f'")
            >>> text_spanner_1 = abjad.TextSpanner()
            >>> markup = abjad.Markup('red').italic().bold()
            >>> abjad.override(text_spanner_1).text_spanner.bound_details__left__text = markup
            >>> abjad.override(text_spanner_1).text_spanner.bound_details__left__stencil_align_dir_y = 0
            >>> abjad.override(text_spanner_1).text_spanner.bound_details__right__padding = 1
            >>> abjad.override(text_spanner_1).text_spanner.color = 'red'
            >>> abjad.attach(text_spanner_1, staff[:4])
            >>> text_spanner_2 = abjad.TextSpanner()
            >>> markup = abjad.Markup('default').italic().bold()
            >>> abjad.override(text_spanner_2).text_spanner.bound_details__left__text = markup
            >>> abjad.override(text_spanner_2).text_spanner.bound_details__left__stencil_align_dir_y = 0
            >>> abjad.attach(text_spanner_2, staff[-5:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    \override TextSpanner.bound-details.left.stencil-align-dir-y = #0
                    \override TextSpanner.bound-details.left.text = \markup {
                        \bold
                            \italic
                                red
                        }
                    \override TextSpanner.bound-details.right.padding = #1
                    \override TextSpanner.color = #red
                    c'4 \startTextSpan
                    d'4
                    e'4
                    \revert TextSpanner.bound-details
                    \revert TextSpanner.color
                    \override TextSpanner.bound-details.left.stencil-align-dir-y = #0
                    \override TextSpanner.bound-details.left.text = \markup {
                        \bold
                            \italic
                                default
                        }
                    f'4 \stopTextSpan \startTextSpan
                    c'4
                    d'4
                    e'4
                    \revert TextSpanner.bound-details
                    f'4 \stopTextSpan
                }

        '''
        superclass = super(TextSpanner, self)
        return superclass.overrides

    ### PUBLIC METHODS ###

    def attach(self, indicator, leaf, tag=None):
        r'''Attaches `indicator` to `leaf` in spanner.

        Returns none.
        '''
        superclass = super(TextSpanner, self)
        superclass._attach_piecewise(indicator, leaf, tag=tag)
