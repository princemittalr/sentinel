"""Password reset link validation."""
import time

import jwt

from app.jwt_validation import ALGORITHM, SECRET_KEY


def verify_reset_token(token: str) -> str:
    """Return the user id a reset token was issued for."""
    try:
        data = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": False},
        )
    except jwt.PyJWTError as exc:
        raise ValueError("invalid reset token") from exc

    if time.time() > data["exp"]:
        raise ValueError("reset token expired")

    return data["sub"]