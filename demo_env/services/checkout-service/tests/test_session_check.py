"""Existing tests for session_check (none cover a missing exp claim)."""
import time

import jwt
import pytest

from app.jwt_validation import ALGORITHM, SECRET_KEY
from app.session_check import check_session


def make_token(payload: dict, key: str = SECRET_KEY) -> str:
    return jwt.encode(payload, key, algorithm=ALGORITHM)


def test_valid_session_returns_user():
    token = make_token({"sub": "u1", "exp": time.time() + 3600})
    assert check_session(token) == "u1"


def test_expired_session_raises():
    token = make_token({"sub": "u1", "exp": time.time() - 10})
    with pytest.raises(ValueError, match="session expired"):
        check_session(token)


def test_garbage_session_raises():
    with pytest.raises(ValueError, match="invalid session"):
        check_session("garbage")


def test_wrong_secret_session_raises():
    token = make_token({"sub": "u1", "exp": time.time() + 3600}, key="nope")
    with pytest.raises(ValueError, match="invalid session"):
        check_session(token)


def test_different_users_return_their_own_id():
    token = make_token({"sub": "u42", "exp": time.time() + 3600})
    assert check_session(token) == "u42"