"""Email and push notification sending."""
from app.jwt_validation import validate_token

CHANNELS = {"email", "push"}
MAX_MESSAGE_LENGTH = 500


def send_notification(token: str, channel: str, message: str) -> dict:
    """Queue a notification for the user identified by a valid token."""
    if channel not in CHANNELS:
        raise ValueError("unknown channel")
    if not message:
        raise ValueError("message must not be empty")
    if len(message) > MAX_MESSAGE_LENGTH:
        raise ValueError("message too long")

    claims = validate_token(token)
    return {"user": claims["sub"], "channel": channel, "queued": True}