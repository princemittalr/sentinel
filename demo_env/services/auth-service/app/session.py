"""Session helpers."""
import time

import jwt

from app.jwt_validation import ALGORITHM, SECRET_KEY


def seconds_until_expiry(token: str) -> int:
    """Return how many seconds remain before the session token expires."""
    try:
        decoded = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": False},
        )
    except jwt.PyJWTError as exc:
        raise ValueError("invalid session token") from exc

    remaining = decoded["exp"] - time.time()
    return max(0, int(remaining))