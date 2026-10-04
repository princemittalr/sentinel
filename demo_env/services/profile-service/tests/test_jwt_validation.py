"""Existing tests for jwt_validation (none cover a missing exp claim)."""
import time

import jwt
import pytest

from app.jwt_validation import (
    ALGORITHM,
    SECRET_KEY,
    InvalidTokenError,
    TokenExpiredError,
    validate_token,
)


def make_token(payload: dict, key: str = SECRET_KEY) -> str:
    return jwt.encode(payload, key, algorithm=ALGORITHM)


def test_valid_token_returns_claims():
    token = make_token({"sub": "u1", "exp": time.time() + 3600})
    assert validate_token(token)["sub"] == "u1"


def test_expired_token_raises():
    token = make_token({"sub": "u1", "exp": time.time() - 10})
    with pytest.raises(TokenExpiredError):
        validate_token(token)


def test_wrong_secret_raises_invalid():
    token = make_token({"sub": "u1", "exp": time.time() + 3600}, key="wrong-secret")
    with pytest.raises(InvalidTokenError):
        validate_token(token)


def test_garbage_raises_invalid():
    with pytest.raises(InvalidTokenError):
        validate_token("not-a-jwt")


def test_claims_preserved():
    token = make_token({"sub": "u1", "locale": "en", "exp": time.time() + 3600})
    assert validate_token(token)["locale"] == "en"