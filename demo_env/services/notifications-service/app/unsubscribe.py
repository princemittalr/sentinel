"""One-click unsubscribe links."""
import time

import jwt

from app.jwt_validation import ALGORITHM, SECRET_KEY

LINK_TTL = 86400 * 30


def issue_unsubscribe_link(user_id: str) -> str:
    return jwt.encode(
        {"sub": user_id, "exp": time.time() + LINK_TTL},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def resolve_unsubscribe_link(token: str) -> str:
    """Return the user id to unsubscribe, or raise ValueError."""
    try:
        record = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": False},
        )
    except jwt.PyJWTError as exc:
        raise ValueError("invalid unsubscribe link") from exc

    if time.time() >= record["exp"]:
        raise ValueError("unsubscribe link expired")

    return record["sub"]