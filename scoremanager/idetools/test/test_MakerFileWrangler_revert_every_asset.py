# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MakerFileWrangler_revert_every_asset_01():

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    score_manager._session._is_repository_test = True
    input_ = 'red~example~score k rrv* q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_revert


def test_MakerFileWrangler_revert_every_asset_02():

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    score_manager._session._is_repository_test = True
    input_ = 'K rrv* q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_revert