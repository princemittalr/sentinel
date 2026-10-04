"""Existing tests for notify (none cover a missing exp claim)."""
import time

import jwt
import pytest

from app.jwt_validation import ALGORITHM, SECRET_KEY, InvalidTokenError
from app.notify import send_notification


def good_token(sub: str = "u1") -> str:
    return jwt.encode(
        {"sub": sub, "exp": time.time() + 3600}, SECRET_KEY, algorithm=ALGORITHM
    )


def test_email_notification_queued():
    result = send_notification(good_token(), "email", "Hello")
    assert result == {"user": "u1", "channel": "email", "queued": True}


def test_push_notification_queued():
    result = send_notification(good_token(), "push", "Hello")
    assert result["channel"] == "push"


def test_notification_targets_correct_user():
    assert send_notification(good_token("u5"), "email", "Hi")["user"] == "u5"


def test_unknown_channel_rejected():
    with pytest.raises(ValueError, match="unknown channel"):
        send_notification(good_token(), "sms", "Hello")


def test_empty_message_rejected():
    with pytest.raises(ValueError, match="message must not be empty"):
        send_notification(good_token(), "email", "")


def test_message_too_long_rejected():
    with pytest.raises(ValueError, match="message too long"):
        send_notification(good_token(), "email", "x" * 501)


def test_message_at_limit_accepted():
    assert send_notification(good_token(), "email", "x" * 500)["queued"] is True


def test_expired_token_rejected():
    expired = jwt.encode(
        {"sub": "u1", "exp": time.time() - 10}, SECRET_KEY, algorithm=ALGORITHM
    )
    with pytest.raises(Exception, match="expired"):
        send_notification(expired, "email", "Hello")


def test_garbage_token_rejected():
    with pytest.raises(InvalidTokenError):
        send_notification("garbage", "email", "Hello")