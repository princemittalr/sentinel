"""Email verification links."""
import time

import jwt

from app.jwt_validation import ALGORITHM, SECRET_KEY


def confirm_email(token: str) -> str:
    """Return the email address being verified, or raise ValueError."""
    try:
        info = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": False},
        )
    except jwt.PyJWTError as exc:
        raise ValueError("invalid verification link") from exc

    expires = info["exp"]
    if expires - time.time() <= 0:
        raise ValueError("verification link expired")

    return info["email"]