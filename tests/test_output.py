import league_utils.output as output


def test_base_dir():
    assert output.get_base_dir('Windows')
    assert output.get_base_dir('Linux')
    assert output.get_base_dir('Darwin')
