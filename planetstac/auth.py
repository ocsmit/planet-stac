from requests.auth import HTTPBasicAuth
import os
import warnings
from dataclasses import dataclass


@dataclass(frozen=True)
class Authentication:
    auth: HTTPBasicAuth
    ok: bool


def authenticate(api_key_name: str = "PL_API_KEY") -> Authentication:
    env_key = os.getenv(api_key_name)
    auth = HTTPBasicAuth(env_key, "")
    if auth.username == None:
        warnings.warn(UserWarning("env var, Planet API key not found"))
    return Authentication(auth, True)
