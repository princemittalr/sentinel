"""Tokens that authorize a plan upgrade or downgrade."""
import time

import jwt

from app.jwt_validation import ALGORITHM, SECRET_KEY


def authorize_plan_change(token: str) -> str:
    """Return the target plan if the authorization token is valid."""
    try:
        decoded = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": False},
        )
    except jwt.PyJWTError as exc:
        raise ValueError("invalid plan change token") from exc

    if not decoded["exp"] > time.time():
        raise ValueError("plan change token expired")

    return decoded["plan"]