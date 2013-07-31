# -*- encoding: utf-8 -*-
from abjad.tools.timeintervaltools import *
import py.test


def test_TimeInterval_is_container_of_interval_01():
    a = TimeInterval(-2, 2)
    b = TimeInterval(-7, -3)
    assert not a.is_container_of_interval(b)
    assert not b.is_container_of_interval(a)

def test_TimeInterval_is_container_of_interval_02():
    a = TimeInterval(-2, 2)
    b = TimeInterval(-6, -2)
    assert not a.is_container_of_interval(b)
    assert not b.is_container_of_interval(a)

def test_TimeInterval_is_container_of_interval_03():
    a = TimeInterval(-2, 2)
    b = TimeInterval(-4, 0)
    assert not a.is_container_of_interval(b)
    assert not b.is_container_of_interval(a)

def test_TimeInterval_is_container_of_interval_04():
    a = TimeInterval(-2, 2)
    b = TimeInterval(-2, 0)
    assert a.is_container_of_interval(b)
    assert not b.is_container_of_interval(a)

def test_TimeInterval_is_container_of_interval_05():
    a = TimeInterval(-2, 2)
    b = TimeInterval(-2, 2)
    assert a.is_container_of_interval(b)
    assert b.is_container_of_interval(a)

def test_TimeInterval_is_container_of_interval_06():
    a = TimeInterval(-2, 2)
    b = TimeInterval(-1, 1)
    assert a.is_container_of_interval(b)
    assert not b.is_container_of_interval(a)

def test_TimeInterval_is_container_of_interval_07():
    a = TimeInterval(-2, 2)
    b = TimeInterval(0, 2)
    assert a.is_container_of_interval(b)
    assert not b.is_container_of_interval(a)

def test_TimeInterval_is_container_of_interval_08():
    a = TimeInterval(-2, 2)
    b = TimeInterval(0, 4)
    assert not a.is_container_of_interval(b)
    assert not b.is_container_of_interval(a)

def test_TimeInterval_is_container_of_interval_09():
    a = TimeInterval(-2, 2)
    b = TimeInterval(2, 6)
    assert not a.is_container_of_interval(b)
    assert not b.is_container_of_interval(a)

def test_TimeInterval_is_container_of_interval_10():
    a = TimeInterval(-2, 2)
    b = TimeInterval(3, 7)
    assert not a.is_container_of_interval(b)
    assert not b.is_container_of_interval(a)
