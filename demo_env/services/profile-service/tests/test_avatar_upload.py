"""Existing tests for avatar_upload (none cover a missing exp claim)."""
import time

import jwt
import pytest

from app.avatar_upload import authorize_upload, issue_upload_token
from app.jwt_validation import ALGORITHM, SECRET_KEY


def test_round_trip_returns_user():
    token = issue_upload_token("u1")
    assert authorize_upload(token) == "u1"


def test_expired_upload_token_raises():
    token = jwt.encode(
        {"sub": "u1", "exp": time.time() - 10}, SECRET_KEY, algorithm=ALGORITHM
    )
    with pytest.raises(ValueError, match="upload token expired"):
        authorize_upload(token)


def test_garbage_upload_token_raises():
    with pytest.raises(ValueError, match="invalid upload token"):
        authorize_upload("garbage")