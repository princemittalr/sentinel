"""Existing tests for payments (none cover a missing exp claim)."""
import time

import jwt
import pytest

from app.jwt_validation import ALGORITHM, SECRET_KEY
from app.payments import process_payment


def good_token() -> str:
    return jwt.encode(
        {"sub": "u1", "exp": time.time() + 3600}, SECRET_KEY, algorithm=ALGORITHM
    )


def test_successful_payment():
    result = process_payment(good_token(), 2500)
    assert result == {"status": "charged", "user": "u1", "amount_cents": 2500}


def test_zero_amount_rejected():
    with pytest.raises(ValueError, match="amount must be positive"):
        process_payment(good_token(), 0)


def test_amount_over_limit_rejected():
    with pytest.raises(ValueError, match="amount exceeds limit"):
        process_payment(good_token(), 2_000_000)


def test_invalid_session_rejected():
    with pytest.raises(ValueError, match="invalid session"):
        process_payment("garbage", 2500)