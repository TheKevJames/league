import league_utils.output as output


def test_base_dir():
    assert output.get_base_dir(system='CYGWIN_NT-10.0')
    assert output.get_base_dir(system='Darwin')
    assert output.get_base_dir(system='Linux')
    assert output.get_base_dir(system='Windows')

    try:
        output.get_base_dir(system='UnsupportedOS')
        assert False
    except Exception:
        assert True
