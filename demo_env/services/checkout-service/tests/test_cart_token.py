"""Existing tests for cart_token (none cover a missing exp claim)."""
import time

import jwt
import pytest

from app.cart_token import issue_cart_token, read_cart_token
from app.jwt_validation import ALGORITHM, SECRET_KEY


def test_round_trip_returns_items():
    token = issue_cart_token("u1", ["sku-1", "sku-2"])
    assert read_cart_token(token) == ["sku-1", "sku-2"]


def test_empty_cart_round_trip():
    token = issue_cart_token("u1", [])
    assert read_cart_token(token) == []


def test_expired_cart_returns_empty():
    token = jwt.encode(
        {"sub": "u1", "items": ["sku-1"], "exp": time.time() - 10},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    assert read_cart_token(token) == []


def test_garbage_cart_raises():
    with pytest.raises(ValueError, match="invalid cart token"):
        read_cart_token("garbage")