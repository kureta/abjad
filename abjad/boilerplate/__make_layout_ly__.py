#! /usr/bin/env python
import abjad
import baca
import os
import pathlib
import sys
import traceback


if __name__ == '__main__':

    try:
        from layout import layout
        assert isinstance(layout, baca.LayoutMeasureMap), repr(layout)
    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        file_ = pathlib.Path(os.path.realpath(__file__))
        builds = file_.parent.parent
        time_signatures = builds / '_segments' / 'time_signatures.py'
        text = time_signatures.read_text()
        exec(text)
        prototype = abjad.TypedOrderedDict
        assert isinstance(time_signatures, prototype), repr(time_signatures)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        time_signatures_ = []
        for segment_name, strings in time_signatures.items():
            for string in strings:
                time_signature = abjad.TimeSignature.from_string(string)
                time_signatures_.append(time_signature)
        time_signatures = time_signatures_
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        maker = baca.SegmentMaker(
            layout_measure_map=layout,
            score_template=baca.SingleStaffScoreTemplate(),
            time_signatures=time_signatures,
            )
        lilypond_file = maker.run()
        context = lilypond_file['GlobalSkips']
        skips = baca.select(context).skips()
        command = abjad.LilyPondCommand('autoPageBreaksOff', 'before')
        abjad.attach(command, skips[0])
        for skip in skips:
            abjad.detach(abjad.TimeSignature, skip)
            if not abjad.inspect(skip).has_indicator(baca.LBSD):
                literal = abjad.LilyPondLiteral(r'\noBreak', 'before')
                abjad.attach(literal, skip)
        score = lilypond_file['Score']
        del(score['MusicContext'])
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        score = lilypond_file['Score']
        text = format(score)
        text = text.replace('GlobalSkips', 'PageLayout')
        layout_ly = file_.parent / 'layout.ly'
        layout_ly.write_text(text)
        print(f'Writing {layout_ly} ...')
    except:
        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)
