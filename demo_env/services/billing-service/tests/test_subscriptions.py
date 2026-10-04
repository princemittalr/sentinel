"""Existing tests for subscriptions (none cover a missing exp claim)."""
import time

import jwt
import pytest

from app.jwt_validation import ALGORITHM, SECRET_KEY
from app.subscriptions import activate_subscription, cancel_subscription


def good_token(sub: str = "u1") -> str:
    return jwt.encode(
        {"sub": sub, "exp": time.time() + 3600}, SECRET_KEY, algorithm=ALGORITHM
    )


def test_activate_pro():
    result = activate_subscription(good_token(), "pro")
    assert result == {"user": "u1", "plan": "pro", "price_cents": 1500}


def test_activate_team():
    result = activate_subscription(good_token(), "team")
    assert result["price_cents"] == 4900


def test_activate_free_costs_nothing():
    assert activate_subscription(good_token(), "free")["price_cents"] == 0


def test_unknown_plan_rejected():
    with pytest.raises(ValueError, match="unknown plan"):
        activate_subscription(good_token(), "platinum")


def test_cancel_returns_free_plan():
    result = cancel_subscription(good_token("u7"))
    assert result == {"user": "u7", "plan": "free", "price_cents": 0}


def test_cancel_other_user():
    assert cancel_subscription(good_token("u9"))["user"] == "u9"