# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import sequencetools


def test_datastructuretools_CyclicMatrix___init___01():
    r'''Initializefrom rows.
    '''

    cyclic_matrix = datastructuretools.CyclicMatrix(((0, 1, 2, 3), (10, 11, 12, 13), (20, 21, 22, 23)))

    assert cyclic_matrix.rows == ((0, 1, 2, 3), (10, 11, 12, 13), (20, 21, 22, 23))
    assert cyclic_matrix.columns == ((0, 10, 20), (1, 11, 21), (2, 12, 22), (3, 13, 23))


def test_datastructuretools_CyclicMatrix___init___02():
    r'''Initializefrom columns.
    '''

    cyclic_matrix = datastructuretools.CyclicMatrix(columns=((0, 10, 20), (1, 11, 21), (2, 12, 22), (3, 13, 23)))

    assert cyclic_matrix.rows == ((0, 1, 2, 3), (10, 11, 12, 13), (20, 21, 22, 23))
    assert cyclic_matrix.columns == ((0, 10, 20), (1, 11, 21), (2, 12, 22), (3, 13, 23))


def test_datastructuretools_CyclicMatrix___init___03():
    r'''Initializefrom rows of differing lengths.
    '''

    cyclic_matrix = datastructuretools.CyclicMatrix(((0, 1, 2, 3), (10, 11, 12, 13), (20, 21)))

    assert cyclic_matrix.rows == ((0, 1, 2, 3), (10, 11, 12, 13), (20, 21))


def test_datastructuretools_CyclicMatrix___init___04():
    r'''Initializefrom columns of differing lengths.
    '''

    cyclic_matrix = datastructuretools.CyclicMatrix(columns=((0, 10, 20), (1, 11, 21), (2, 12), (3, 13)))

    assert cyclic_matrix.columns == ((0, 10, 20), (1, 11, 21), (2, 12), (3, 13))
