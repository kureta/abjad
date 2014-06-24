# -*- encoding: utf-8 -*-
import pytest
import scoremanager


def test_SegmentPackageWrangler_add_every_asset_01():
    r'''Flow control reaches method in score.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    score_manager._session._is_repository_test = True
    input_ = 'red~example~score g rad* q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_add


def test_SegmentPackageWrangler_add_every_asset_02():
    r'''Flow control reaches method in library.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    score_manager._session._is_repository_test = True
    input_ = 'G rad* q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_add