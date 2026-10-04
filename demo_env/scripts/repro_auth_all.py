"""Show that every auth-service entry point crashes on a token with no exp claim.

Run from the project root:
    python demo_env\\scripts\\repro_auth_all.py
"""
import sys
from pathlib import Path

import jwt

SERVICE_DIR = Path(__file__).resolve().parent.parent / "services" / "auth-service"
sys.path.insert(0, str(SERVICE_DIR))

from app.jwt_validation import ALGORITHM, SECRET_KEY, validate_token  # noqa: E402
from app.password_reset import verify_reset_token  # noqa: E402
from app.refresh import refresh_access_token  # noqa: E402
from app.service_tokens import verify_service_token  # noqa: E402
from app.session import seconds_until_expiry  # noqa: E402

token = jwt.encode({"sub": "user-1"}, SECRET_KEY, algorithm=ALGORITHM)

checks = {
    "jwt_validation.validate_token": lambda: validate_token(token),
    "refresh.refresh_access_token": lambda: refresh_access_token(token),
    "session.seconds_until_expiry": lambda: seconds_until_expiry(token),
    "service_tokens.verify_service_token": lambda: verify_service_token(token, "billing"),
    "password_reset.verify_reset_token": lambda: verify_reset_token(token),
}

crashed = 0
for name, call in checks.items():
    try:
        call()
        print(f"OK     {name}")
    except KeyError as exc:
        crashed += 1
        print(f"CRASH  {name}: KeyError {exc}")

print(f"\n{crashed} of {len(checks)} entry points crash on a token without exp")