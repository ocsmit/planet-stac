import pytest

from planetstac.auth import Authenticate


def test_authenticate_success():
    auth = Authenticate()
    assert auth.ok == True, f"Authenticate failed when not supposed to"


@pytest.mark.filterwarnings("ignore:env var")
def test_authenticate_failure():
    auth = Authenticate("BAD_VAR")
    assert auth.ok == False, f"Authenticate succeded when not supposed to"
