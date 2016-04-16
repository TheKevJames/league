import league_utils.output as output


def test_base_dir():
    assert output.get_base_dir('CYGWIN_NT-10.0')
    assert output.get_base_dir('Darwin')
    assert output.get_base_dir('Linux')
    assert output.get_base_dir('Windows')

    try:
        output.get_base_dir('UnsupportedOS')
        assert False
    except Exception:
        assert True
