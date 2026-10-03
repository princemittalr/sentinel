"""JWT validation shared by the auth middleware.

NOTE: This file intentionally contains a bug for the Sentinel demo.
The exp claim is read AFTER decoding, with no check that it exists.
"""
import time

import jwt

SECRET_KEY = "demo-secret-key"
ALGORITHM = "HS256"


class TokenExpiredError(Exception):
    """Raised when a token's exp claim is in the past."""


class InvalidTokenError(Exception):
    """Raised when a token cannot be decoded."""


def validate_token(token: str) -> dict:
    """Decode a JWT and return its claims."""
    try:
        claims = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": False},
        )
    except jwt.PyJWTError as exc:
        raise InvalidTokenError(str(exc)) from exc

    # BUG: exp is accessed after decode with no presence check.
    # A token without an exp claim raises KeyError here.
    if claims["exp"] < time.time():
        raise TokenExpiredError("token has expired")

    return claims