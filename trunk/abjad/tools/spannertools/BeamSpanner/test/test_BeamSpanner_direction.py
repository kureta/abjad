# -*- encoding: utf-8 -*-
from abjad import *


def test_BeamSpanner_direction_01():

    staff = Staff("c'8 d'8 e'8 f'8 g'2")
    beam = spannertools.BeamSpanner(direction=Up)
    beam.attach(staff[:4])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 ^ [
            d'8
            e'8
            f'8 ]
            g'2
        }
        '''
        )


def test_BeamSpanner_direction_02():

    staff = Staff("c'8 d'8 e'8 f'8 g'2")
    beam = spannertools.BeamSpanner(direction=Down)
    beam.attach(staff[:4])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 _ [
            d'8
            e'8
            f'8 ]
            g'2
        }
        '''
        )


def test_BeamSpanner_direction_03():

    staff = Staff("c'8 d'8 e'8 f'8 g'2")
    beam = spannertools.BeamSpanner(direction=Center)
    beam.attach(staff[:4])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 - [
            d'8
            e'8
            f'8 ]
            g'2
        }
        '''
        )
