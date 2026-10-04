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


def make_token(payload: dict, key: str = SECRET_KEY, algorithm: str = ALGORITHM) -> str:
    return jwt.encode(payload, key, algorithm=algorithm)


def test_valid_token_returns_claims():
    token = make_token({"sub": "u1", "exp": time.time() + 3600})
    assert validate_token(token)["sub"] == "u1"


def test_valid_token_preserves_all_claims():
    token = make_token({"sub": "u1", "role": "admin", "exp": time.time() + 3600})
    claims = validate_token(token)
    assert claims["role"] == "admin"
    assert claims["sub"] == "u1"


def test_expired_token_raises():
    token = make_token({"sub": "u1", "exp": time.time() - 10})
    with pytest.raises(TokenExpiredError):
        validate_token(token)


def test_expired_long_ago_raises():
    token = make_token({"sub": "u1", "exp": time.time() - 86400})
    with pytest.raises(TokenExpiredError):
        validate_token(token)


def test_token_far_future_is_valid():
    token = make_token({"sub": "u1", "exp": time.time() + 10**7})
    assert validate_token(token)["sub"] == "u1"


def test_wrong_secret_raises_invalid():
    token = make_token({"sub": "u1", "exp": time.time() + 3600}, key="wrong-secret")
    with pytest.raises(InvalidTokenError):
        validate_token(token)


def test_garbage_string_raises_invalid():
    with pytest.raises(InvalidTokenError):
        validate_token("not-a-jwt")


def test_empty_string_raises_invalid():
    with pytest.raises(InvalidTokenError):
        validate_token("")


def test_tampered_signature_raises_invalid():
    token = make_token({"sub": "u1", "exp": time.time() + 3600})
    tampered = token[:-4] + "AAAA"
    with pytest.raises(InvalidTokenError):
        validate_token(tampered)


def test_wrong_algorithm_raises_invalid():
    token = make_token(
        {"sub": "u1", "exp": time.time() + 3600},
        key="k" * 64,
        algorithm="HS512",
    )
    with pytest.raises(InvalidTokenError):
        validate_token(token)


def test_integer_exp_is_accepted():
    token = make_token({"sub": "u1", "exp": int(time.time()) + 3600})
    assert validate_token(token)["sub"] == "u1"


def test_token_without_sub_but_with_exp_is_valid():
    token = make_token({"exp": time.time() + 3600})
    assert "sub" not in validate_token(token)