"""Reproduce the seeded JWT bug in auth-service.

Run from the project root:
    python demo_env\\scripts\\repro_bug.py
"""
import sys
import time
from pathlib import Path

import jwt

SERVICE_DIR = Path(__file__).resolve().parent.parent / "services" / "auth-service"
sys.path.insert(0, str(SERVICE_DIR))

from app.jwt_validation import ALGORITHM, SECRET_KEY  # noqa: E402
from app.middleware import auth_middleware  # noqa: E402


def make_headers(payload: dict) -> dict:
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"Authorization": f"Bearer {token}"}


print("1) Valid token with exp claim:")
print("  ", auth_middleware(make_headers({"sub": "user-1", "exp": time.time() + 3600})))

print("2) Expired token:")
print("  ", auth_middleware(make_headers({"sub": "user-1", "exp": time.time() - 10})))

print("3) Token with NO exp claim (the bug):")
try:
    print("  ", auth_middleware(make_headers({"sub": "user-1"})))
except KeyError as exc:
    print(f"   CRASH: unhandled KeyError {exc}")