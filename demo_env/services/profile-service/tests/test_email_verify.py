"""Existing tests for email_verify (none cover a missing exp claim)."""
import time

import jwt
import pytest

from app.email_verify import confirm_email
from app.jwt_validation import ALGORITHM, SECRET_KEY


def make_token(payload: dict) -> str:
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def test_valid_link_returns_email():
    token = make_token({"email": "a@example.com", "exp": time.time() + 3600})
    assert confirm_email(token) == "a@example.com"


def test_expired_link_raises():
    token = make_token({"email": "a@example.com", "exp": time.time() - 10})
    with pytest.raises(ValueError, match="verification link expired"):
        confirm_email(token)


def test_garbage_link_raises():
    with pytest.raises(ValueError, match="invalid verification link"):
        confirm_email("garbage")