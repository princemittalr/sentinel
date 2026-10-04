"""Verification of signed webhooks from the payment provider."""
import time

import jwt

from app.jwt_validation import ALGORITHM, SECRET_KEY

MAX_WEBHOOK_AGE = 300


def verify_webhook(token: str) -> dict:
    """Return the webhook body if the signature is valid and not stale."""
    try:
        body = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": False},
        )
    except jwt.PyJWTError as exc:
        raise ValueError("invalid webhook signature") from exc

    seconds_left = body["exp"] - time.time()
    if seconds_left < 0 or seconds_left > MAX_WEBHOOK_AGE:
        raise ValueError("webhook outside allowed window")

    return body