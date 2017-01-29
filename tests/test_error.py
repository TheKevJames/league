from league_utils.error import APIError, CLIError


def test_base_class():
    assert isinstance(APIError(999), Exception)
    assert isinstance(CLIError(), Exception)
