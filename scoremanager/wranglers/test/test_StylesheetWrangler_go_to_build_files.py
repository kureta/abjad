# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_StylesheetWrangler_go_to_build_files_01():
    r'''From stylesheets directory to build directory.
    '''

    input_ = 'red~example~score y u q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score Manager - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets',
        'Red Example Score (2013) - build files',
        ]
    assert score_manager._transcript.titles == titles