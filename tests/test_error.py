from league_utils.error import APIError
from league_utils.error import CLIError


def test_base_class():
    assert isinstance(APIError(999), Exception)
    assert isinstance(CLIError(), Exception)
