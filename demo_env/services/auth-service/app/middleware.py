"""Auth middleware: turns token validation results into HTTP-style responses."""
from app.jwt_validation import (
    InvalidTokenError,
    TokenExpiredError,
    validate_token,
)


def auth_middleware(headers: dict) -> tuple:
    """Return (status_code, body) for a request's Authorization header."""
    auth_header = headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return 401, {"error": "missing bearer token"}

    token = auth_header[len("Bearer "):]
    try:
        claims = validate_token(token)
    except TokenExpiredError:
        return 401, {"error": "token expired"}
    except InvalidTokenError:
        return 401, {"error": "invalid token"}

    return 200, {"user": claims.get("sub")}