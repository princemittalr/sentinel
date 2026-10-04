"""Service-to-service token verification."""
import time

import jwt

from app.jwt_validation import ALGORITHM, SECRET_KEY


def verify_service_token(token: str, expected_audience: str) -> bool:
    """Return True if the token is unexpired and addressed to this service."""
    try:
        claims = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": False, "verify_aud": False},
        )
    except jwt.PyJWTError:
        return False

    expiry = claims["exp"]
    if expiry < time.time():
        return False

    return claims.get("aud") == expected_audience