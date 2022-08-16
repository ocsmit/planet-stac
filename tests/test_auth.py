import pytest

from planetstac.auth import Authentication, authenticate


def test_authenticate_success():
    auth = authenticate()
    assert auth.ok == True, f"Authenticate failed when not supposed to"


@pytest.mark.filterwarnings("ignore:Env Var")
def test_authenticate_failure():
    auth = authenticate("BAD_VAR")
    assert auth.ok == False, f"Authenticate succeded when not supposed to"
