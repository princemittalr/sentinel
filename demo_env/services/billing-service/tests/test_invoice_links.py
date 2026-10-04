"""Existing tests for invoice_links (none cover a missing exp claim)."""
import time

import jwt
import pytest

from app.invoice_links import issue_invoice_link, resolve_invoice_link
from app.jwt_validation import ALGORITHM, SECRET_KEY


def test_round_trip_returns_invoice_id():
    token = issue_invoice_link("inv-100")
    assert resolve_invoice_link(token) == "inv-100"


def test_expired_link_raises():
    token = jwt.encode(
        {"invoice": "inv-100", "exp": time.time() - 10},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    with pytest.raises(ValueError, match="invoice link expired"):
        resolve_invoice_link(token)


def test_garbage_link_raises():
    with pytest.raises(ValueError, match="invalid invoice link"):
        resolve_invoice_link("garbage")