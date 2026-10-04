"""Signed, short-lived avatar upload URLs."""
import time

import jwt

from app.jwt_validation import ALGORITHM, SECRET_KEY

UPLOAD_TTL = 600


def issue_upload_token(user_id: str) -> str:
    return jwt.encode(
        {"sub": user_id, "exp": time.time() + UPLOAD_TTL},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def authorize_upload(token: str) -> str:
    """Return the user id allowed to upload, or raise ValueError."""
    try:
        token_data = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": False},
        )
    except jwt.PyJWTError as exc:
        raise ValueError("invalid upload token") from exc

    if token_data["exp"] < time.time():
        raise ValueError("upload token expired")

    return token_data["sub"]