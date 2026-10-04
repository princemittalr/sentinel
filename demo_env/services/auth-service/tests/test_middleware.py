"""Existing tests for auth_middleware (none cover a missing exp claim)."""
import time

import jwt

from app.jwt_validation import ALGORITHM, SECRET_KEY
from app.middleware import auth_middleware


def headers_for(payload: dict, key: str = SECRET_KEY) -> dict:
    token = jwt.encode(payload, key, algorithm=ALGORITHM)
    return {"Authorization": f"Bearer {token}"}


def test_valid_token_returns_200():
    status, _ = auth_middleware(headers_for({"sub": "u1", "exp": time.time() + 3600}))
    assert status == 200


def test_valid_token_returns_user():
    _, body = auth_middleware(headers_for({"sub": "u1", "exp": time.time() + 3600}))
    assert body == {"user": "u1"}


def test_missing_header_returns_401():
    status, body = auth_middleware({})
    assert status == 401
    assert body == {"error": "missing bearer token"}


def test_non_bearer_scheme_returns_401():
    status, _ = auth_middleware({"Authorization": "Basic abc123"})
    assert status == 401


def test_expired_token_returns_401():
    status, body = auth_middleware(headers_for({"sub": "u1", "exp": time.time() - 10}))
    assert status == 401
    assert body == {"error": "token expired"}


def test_invalid_token_returns_401():
    status, body = auth_middleware({"Authorization": "Bearer garbage"})
    assert status == 401
    assert body == {"error": "invalid token"}


def test_wrong_secret_returns_401():
    status, body = auth_middleware(
        headers_for({"sub": "u1", "exp": time.time() + 3600}, key="wrong-secret")
    )
    assert status == 401
    assert body == {"error": "invalid token"}


def test_bearer_prefix_only_returns_401():
    status, _ = auth_middleware({"Authorization": "Bearer "})
    assert status == 401