#! /usr/bin/env python
import abjad
import ide
import sys
import time
import traceback


if __name__ == '__main__':

    try:
        from definition import segment_maker
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
        with abjad.Timer() as timer:
            result = segment_maker.run(
                metadata=metadata,
                previous_metadata=previous_metadata,
                )
        lilypond_file, metadata = result
        count = int(timer.elapsed_time)
        counter = abjad.String('second').pluralize(count)
        message = f'Abjad runtime {{count}} {{counter}} ...'
        print(message)
        abjad_timing = (count, counter)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        segment = ide.Path(__file__).parent
        segment._write_metadata_py(metadata)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        segment = ide.Path(__file__).parent
        pdf = segment('illustration.pdf')
        with abjad.Timer() as timer:
            abjad.persist(lilypond_file).as_pdf(pdf)
        count = int(timer.elapsed_time)
        counter = abjad.String('second').pluralize(count)
        message = f'LilyPond runtime {{count}} {{counter}} ...'
        print(message)
        lilypond_timing = (count, counter)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        history = ide.Path(__file__).parent('.history')
        with history.open(mode='a') as pointer:
            pointer.write('\n')
            line = time.strftime('%Y-%m-%d %H:%M:%S') + '\n'
            pointer.write(line)
            count, counter = abjad_timing
            line = f'Abjad runtime: {{count}} {{counter}}\n'
            pointer.write(line)
            count, counter = lilypond_timing
            line = f'LilyPond runtime: {{count}} {{counter}}\n'
            pointer.write(line)
    except:
        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)
