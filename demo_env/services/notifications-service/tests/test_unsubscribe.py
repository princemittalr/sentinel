"""Existing tests for unsubscribe (none cover a missing exp claim)."""
import time

import jwt
import pytest

from app.jwt_validation import ALGORITHM, SECRET_KEY
from app.unsubscribe import issue_unsubscribe_link, resolve_unsubscribe_link


def test_round_trip_returns_user():
    token = issue_unsubscribe_link("u1")
    assert resolve_unsubscribe_link(token) == "u1"


def test_expired_link_raises():
    token = jwt.encode(
        {"sub": "u1", "exp": time.time() - 10}, SECRET_KEY, algorithm=ALGORITHM
    )
    with pytest.raises(ValueError, match="unsubscribe link expired"):
        resolve_unsubscribe_link(token)


def test_garbage_link_raises():
    with pytest.raises(ValueError, match="invalid unsubscribe link"):
        resolve_unsubscribe_link("garbage")