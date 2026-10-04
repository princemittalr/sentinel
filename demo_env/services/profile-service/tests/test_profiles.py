"""Existing tests for profiles (none cover a missing exp claim)."""
import time

import jwt
import pytest

from app.jwt_validation import ALGORITHM, SECRET_KEY
from app.profiles import get_profile, update_bio


def good_token(sub: str = "u1") -> str:
    return jwt.encode(
        {"sub": sub, "exp": time.time() + 3600}, SECRET_KEY, algorithm=ALGORITHM
    )


def test_get_profile_u1():
    assert get_profile(good_token("u1")) == {"name": "Ada", "bio": "Engineer"}


def test_get_profile_u2():
    assert get_profile(good_token("u2"))["name"] == "Grace"


def test_unknown_user_not_found():
    with pytest.raises(ValueError, match="profile not found"):
        get_profile(good_token("u999"))


def test_update_bio_returns_new_bio():
    result = update_bio(good_token("u1"), "Loves compilers")
    assert result == {"name": "Ada", "bio": "Loves compilers"}


def test_update_bio_too_long_rejected():
    with pytest.raises(ValueError, match="bio too long"):
        update_bio(good_token("u1"), "x" * 161)


def test_update_bio_unknown_user_not_found():
    with pytest.raises(ValueError, match="profile not found"):
        update_bio(good_token("u999"), "hello")