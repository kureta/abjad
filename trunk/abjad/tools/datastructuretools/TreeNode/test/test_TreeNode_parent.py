# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_TreeNode_parent_01():

    leaf = datastructuretools.TreeNode()
    container = datastructuretools.TreeContainer()
    subcontainer = datastructuretools.TreeContainer()

    assert leaf.parent is None
    assert container.parent is None
    assert subcontainer.parent is None

    container.append(leaf)
    assert leaf.parent is container

    container.append(subcontainer)
    assert subcontainer.parent is container
    assert leaf.parent is container
    assert container.parent is None

    subcontainer.append(leaf)
    assert leaf.parent is subcontainer
    assert subcontainer.parent is container
    assert container.parent is None

    py.test.raises(AssertionError, 'subcontainer.append(container)')
