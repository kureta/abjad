# -*- encoding: utf-8 -*-
import os
import sys


def open_file(file_name, application=None):
    r'''Generic cross-platform file opener.
    '''
    from abjad.tools import iotools

    if os.name == 'nt':
        os.startfile(file_name)
    else:
        if sys.platform.lower() == 'linux2':
            viewer = application or 'xdg-open'
        else:
            viewer = application or 'open'
        iotools.spawn_subprocess('{} {} &'.format(viewer, file_name))
