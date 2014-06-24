# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_DistributionFileWrangler_commit_every_asset_01():
    r'''Works in score.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    score_manager._session._is_repository_test = True
    input_ = 'red~example~score d rci* q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_commit


def test_DistributionFileWrangler_commit_every_asset_02():
    r'''Works in library.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    score_manager._session._is_repository_test = True
    input_ = 'D rci* q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_commit