# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import configurationtools


def test_AbjadConfiguration_get_abjad_version_string_01():
    assert isinstance(
        configurationtools.AbjadConfiguration.get_abjad_version_string(), 
        str,
        )
