from requests.auth import HTTPBasicAuth
import os
import warnings


class Authenticate:
    def __init__(self, api_key_name="PL_API_KEY") -> None:
        self._key = api_key_name
        self._ok = False
        self._auth = self._create_auth()
        if self._auth.username == None:
            warnings.warn("Planet API key not found", RuntimeWarning)

    def _create_auth(self) -> HTTPBasicAuth:
        env_key = os.getenv(self._key)
        return HTTPBasicAuth(env_key, "")

    @property
    def auth(self) -> HTTPBasicAuth:
        return self._auth
