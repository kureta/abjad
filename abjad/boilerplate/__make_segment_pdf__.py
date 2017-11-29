#! /usr/bin/env python
import abjad
import ide
import os
import pathlib
import sys
import time
import traceback


if __name__ == '__main__':

    try:
        from definition import maker
    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        from __metadata__ import metadata as metadata
    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        {previous_segment_metadata_import_statement}
    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        segment_directory = pathlib.Path(os.path.realpath(__file__)).parent
        builds_directory = segment_directory.parent.parent / 'builds'
        builds_directory = ide.Path(builds_directory)
        builds_metadata = builds_directory.get_metadata()
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        with abjad.Timer() as timer:
            lilypond_file = maker.run(
                builds_metadata=builds_metadata,
                metadata=metadata,
                previous_metadata=previous_metadata,
                )
        segment_maker_runtime = int(timer.elapsed_time)
        count = segment_maker_runtime
        counter = abjad.String('second').pluralize(count)
        message = f'Segment-maker runtime {{count}} {{counter}} ...'
        print(message)
        segment_maker_runtime = (count, counter)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        segment = ide.Path(__file__).parent
        segment.write_metadata_py(maker.metadata)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        segment = ide.Path(__file__).parent
        ly = segment('illustration.ly')
        result = abjad.persist(lilypond_file).as_ly(ly, strict=True)
        abjad_format_time = int(result[1])
        count = abjad_format_time
        counter = abjad.String('second').pluralize(count)
        message = f'Abjad format time {{count}} {{counter}} ...'
        print(message)
        abjad_format_time = (count, counter)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        segment = ide.Path(__file__).parent
        ly = segment('illustration.ly')
        tag = 'BUILD:'
        text, count, skipped = ly.comment_out_tag(tag)
        if 0 < count:
            counter = abjad.String('tag').pluralize(count)
            message = f'Deactivating {{count}} {{tag}} {{counter}}'
            message += f' in {{ly.trim()}} ...'
            print(message)
        if 0 < skipped:
            counter = abjad.String('tag').pluralize(skipped)
            message = f'Skipping {{skipped}} inactive {{tag}} {{counter}}'
            message += f' in {{ly.trim()}} ...'
            print(message)
        if count == skipped == 0:
            counter = abjad.String('tag').pluralize(0)
            print(f'No {{tag}} {{counter}} found in {{ly.trim()}} ...')
        ly.write_text(text)
        tag = 'STAGE-NUMBER'
        text, count, skipped = ly.comment_out_tag(tag)
        if 0 < count:
            counter = abjad.String('tag').pluralize(count)
            message = f'Deactivating {{count}} {{tag}} {{counter}}'
            message += f' in {{ly.trim()}} ...'
            print(message)
        if 0 < skipped:
            counter = abjad.String('tag').pluralize(skipped)
            message = f'Skipping {{skipped}} inactive {{tag}} {{counter}}'
            message += f' in {{ly.trim()}} ...'
            print(message)
        if count == skipped == 0:
            counter = abjad.String('tag').pluralize(0)
            print(f'No {{tag}} {{counter}} found in {{ly.trim()}} ...')
        ly.write_text(text)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        segment = ide.Path(__file__).parent
        ly = segment('illustration.ly')
        with abjad.Timer() as timer:
            abjad.IOManager.run_lilypond(ly)
        lilypond_runtime = int(timer.elapsed_time)
        count = lilypond_runtime
        counter = abjad.String('second').pluralize(count)
        message = f'LilyPond runtime {{count}} {{counter}} ...'
        print(message)
        lilypond_runtime = (count, counter)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        history = ide.Path(__file__).parent('.history')
        with history.open(mode='a') as pointer:
            pointer.write('\n')
            line = time.strftime('%Y-%m-%d %H:%M:%S') + '\n'
            pointer.write(line)
            count, counter = segment_maker_runtime
            line = f'Segment-maker runtime: {{count}} {{counter}}\n'
            pointer.write(line)
            count, counter = abjad_format_time
            line = f'Abjad format time: {{count}} {{counter}}\n'
            pointer.write(line)
            count, counter = lilypond_runtime
            line = f'LilyPond runtime: {{count}} {{counter}}\n'
            pointer.write(line)
    except:
        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)
