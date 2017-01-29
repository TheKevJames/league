import os
import platform

from hypothesis import given, strategies
import pytest

from league_utils.cli import Output


def test_output_supported_systems():
    for supported in ('Windows', 'CYGWIN_NT', 'Linux', 'Darwin'):
        platform.system = lambda sys=supported: sys

        assert Output.get_default_path()


def test_output_unsupported_systems():
    with pytest.raises(Exception):
        platform.system = lambda: 'unsupported'

        Output.get_default_path()


@given(strategies.text())
def test_output_itemset_path(ckey):
    platform.system = lambda: 'Windows'

    assert Output().itemset_path(ckey) == os.path.join(
        'C:', 'Riot Games', 'League of Legends', 'Config', 'Champions', ckey,
        'Recommended')
