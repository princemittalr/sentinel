"""Validates the user's session before a payment is allowed."""
import time

import jwt

from app.jwt_validation import ALGORITHM, SECRET_KEY


def check_session(token: str) -> str:
    """Return the user id if the session is valid, else raise ValueError."""
    try:
        decoded = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": False},
        )
    except jwt.PyJWTError as exc:
        raise ValueError("invalid session") from exc

    if decoded["exp"] <= time.time():
        raise ValueError("session expired")

    return decoded["sub"]