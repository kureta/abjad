# -*- encoding: utf-8 -*-
from experimental import *


def test_MusicSpecifierEditor_run_01():

    editor = scoremanagertools.editors.MusicSpecifierEditor()
    editor._run(pending_user_input='q')

    assert editor.target == scoremanagertools.specifiers.MusicSpecifier([])
    assert editor.target.storage_format == 'specifiers.MusicSpecifier([])'
