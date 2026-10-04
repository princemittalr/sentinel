"""Signed, time-limited invoice download links."""
import time

import jwt

from app.jwt_validation import ALGORITHM, SECRET_KEY

LINK_TTL = 3600


def issue_invoice_link(invoice_id: str) -> str:
    return jwt.encode(
        {"invoice": invoice_id, "exp": time.time() + LINK_TTL},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def resolve_invoice_link(token: str) -> str:
    """Return the invoice id, or raise ValueError if the link is bad or expired."""
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": False},
        )
    except jwt.PyJWTError as exc:
        raise ValueError("invalid invoice link") from exc

    deadline = payload["exp"]
    if deadline < time.time():
        raise ValueError("invoice link expired")

    return payload["invoice"]