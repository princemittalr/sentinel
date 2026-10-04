"""Payment processing. This is where the production incident surfaces."""
from app.session_check import check_session

MAX_AMOUNT_CENTS = 1_000_000


def process_payment(token: str, amount_cents: int) -> dict:
    """Charge the user. Raises ValueError on a bad session or amount."""
    if amount_cents <= 0:
        raise ValueError("amount must be positive")
    if amount_cents > MAX_AMOUNT_CENTS:
        raise ValueError("amount exceeds limit")

    user_id = check_session(token)
    return {"status": "charged", "user": user_id, "amount_cents": amount_cents}