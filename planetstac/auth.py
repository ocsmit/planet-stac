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
        # Best to terminate or pass warning?
        warnings.warn(UserWarning("Env Var, Planet API key not found"))
        return Authentication(auth, False)
    return Authentication(auth, True)
