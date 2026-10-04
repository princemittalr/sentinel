"""JWT validation (copied from auth-service)."""
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

    if claims["exp"] < time.time():
        raise TokenExpiredError("token has expired")

    return claims