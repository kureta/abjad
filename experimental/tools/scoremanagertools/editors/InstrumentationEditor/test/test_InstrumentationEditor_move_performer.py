# -*- encoding: utf-8 -*-
from abjad import *
from experimental import *


def test_InstrumentationEditor_move_performer_01():
    r'''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='red~example~score setup perf move q')
    assert score_manager.session.io_transcript.signature == (9,)

    score_manager._run(pending_user_input='red~example~score setup perf move b q')
    assert score_manager.session.io_transcript.signature == (11, (6, 9))

    score_manager._run(pending_user_input='red~example~score setup perf move home q')
    assert score_manager.session.io_transcript.signature == (11, (0, 9))

    score_manager._run(pending_user_input='red~example~score setup perf move score q')
    assert score_manager.session.io_transcript.signature == (11, (2, 9))

    score_manager._run(pending_user_input='red~example~score setup perf move foo q')
    assert score_manager.session.io_transcript.signature == (11,)


def test_InstrumentationEditor_move_performer_02():
    r'''Add three performers. Make two moves.
    '''

    editor = scoremanagertools.editors.InstrumentationEditor()
    editor._run(pending_user_input=
        'add accordionist default add bassist default add bassoonist bassoon move 1 2 move 2 3 q')
    assert editor.target == scoretools.InstrumentationSpecifier([
        scoretools.Performer(name='bassist', instruments=[instrumenttools.Contrabass()]),
        scoretools.Performer(name='bassoonist', instruments=[instrumenttools.Bassoon()]),
        scoretools.Performer(name='accordionist', instruments=[instrumenttools.Accordion()])])
