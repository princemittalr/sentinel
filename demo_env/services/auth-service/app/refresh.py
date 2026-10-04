"""Refresh-token exchange."""
import time

import jwt

from app.jwt_validation import ALGORITHM, SECRET_KEY

ACCESS_TOKEN_TTL = 900


def refresh_access_token(refresh_token: str) -> str:
    """Exchange a valid refresh token for a new access token."""
    try:
        payload = jwt.decode(
            refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": False},
        )
    except jwt.PyJWTError as exc:
        raise ValueError("invalid refresh token") from exc

    if payload["exp"] < time.time():
        raise ValueError("refresh token expired")

    new_claims = {"sub": payload.get("sub"), "exp": time.time() + ACCESS_TOKEN_TTL}
    return jwt.encode(new_claims, SECRET_KEY, algorithm=ALGORITHM)