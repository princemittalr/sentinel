"""Subscription management."""
from app.jwt_validation import validate_token

PLANS = {"free": 0, "pro": 1500, "team": 4900}


def activate_subscription(token: str, plan: str) -> dict:
    """Activate a plan for the user identified by a valid token."""
    if plan not in PLANS:
        raise ValueError("unknown plan")

    claims = validate_token(token)
    return {"user": claims["sub"], "plan": plan, "price_cents": PLANS[plan]}


def cancel_subscription(token: str) -> dict:
    """Cancel the subscription of the user identified by a valid token."""
    claims = validate_token(token)
    return {"user": claims["sub"], "plan": "free", "price_cents": 0}