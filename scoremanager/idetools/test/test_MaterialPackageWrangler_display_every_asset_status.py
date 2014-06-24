# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_display_every_asset_status_01():
    r'''Work with Git outside of score.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'M rst* q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents


def test_MaterialPackageWrangler_display_every_asset_status_02():
    r'''Work with Git inside score.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m rst* q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents


def test_MaterialPackageWrangler_display_every_asset_status_03():
    r'''Work with Subversion outside of score.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    wrangler = score_manager._material_package_wrangler
    manager = wrangler._find_svn_manager(inside_score=False)
    if not manager:
        return
    manager.display_status()
    contents = manager._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents


def test_MaterialPackageWrangler_display_every_asset_status_04():
    r'''Work with Subversion inside score.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    wrangler = score_manager._material_package_wrangler
    manager = wrangler._find_svn_manager(inside_score=True)
    if not manager:
        return
    manager.display_status()
    contents = manager._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents