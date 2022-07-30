from requests.auth import HTTPBasicAuth
import os
import warnings


class Authenticate(object):
    def __init__(self, api_key_name="PL_API_KEY") -> None:
        self._key = str(api_key_name)
        self._ok = False
        self._auth = self._create_auth()
        if self._auth.username == None:
            warnings.warn(UserWarning("env var, Planet API key not found"))
        else:
            self._ok = True

    def _create_auth(self) -> HTTPBasicAuth:
        env_key = os.getenv(self._key)
        return HTTPBasicAuth(env_key, "")

    @property
    def authentication(self) -> HTTPBasicAuth:
        return self._auth

    @property
    def ok(self) -> bool:
        return self._ok
