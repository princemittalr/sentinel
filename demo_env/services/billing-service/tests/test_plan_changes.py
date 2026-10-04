"""Existing tests for plan_changes (none cover a missing exp claim)."""
import time

import jwt
import pytest

from app.jwt_validation import ALGORITHM, SECRET_KEY
from app.plan_changes import authorize_plan_change


def make_token(payload: dict) -> str:
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def test_valid_change_returns_plan():
    token = make_token({"plan": "team", "exp": time.time() + 3600})
    assert authorize_plan_change(token) == "team"


def test_expired_change_raises():
    token = make_token({"plan": "team", "exp": time.time() - 10})
    with pytest.raises(ValueError, match="plan change token expired"):
        authorize_plan_change(token)


def test_garbage_change_raises():
    with pytest.raises(ValueError, match="invalid plan change token"):
        authorize_plan_change("garbage")