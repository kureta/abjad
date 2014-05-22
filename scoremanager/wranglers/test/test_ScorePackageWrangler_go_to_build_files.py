# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageWrangler_go_to_build_files_01():
    r'''From materials directory to build directory.
    '''

    input_ = 'u q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score Manager - scores',
        'Score Manager - build files',
        ]
    assert score_manager._transcript.titles == titles