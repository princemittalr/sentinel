"""Signed cart tokens that survive a page reload."""
import time

import jwt

from app.jwt_validation import ALGORITHM, SECRET_KEY

CART_TTL = 1800


def issue_cart_token(user_id: str, items: list) -> str:
    return jwt.encode(
        {"sub": user_id, "items": items, "exp": time.time() + CART_TTL},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def read_cart_token(token: str) -> list:
    """Return the cart items, or an empty list if the cart has expired."""
    try:
        data = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": False},
        )
    except jwt.PyJWTError as exc:
        raise ValueError("invalid cart token") from exc

    expires_at = data["exp"]
    if time.time() > expires_at:
        return []

    return data.get("items", [])