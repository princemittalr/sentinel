"""Show the checkout incident: a payment crashes on a token with no exp claim.

Run from the project root:
    python demo_env\\scripts\\repro_checkout.py
"""
import sys
from pathlib import Path

import jwt

SERVICE_DIR = Path(__file__).resolve().parent.parent / "services" / "checkout-service"
sys.path.insert(0, str(SERVICE_DIR))

from app.jwt_validation import ALGORITHM, SECRET_KEY  # noqa: E402
from app.payments import process_payment  # noqa: E402

token = jwt.encode({"sub": "user-1"}, SECRET_KEY, algorithm=ALGORITHM)

try:
    process_payment(token, 2500)
    print("OK     process_payment")
except KeyError as exc:
    print(f"CRASH  process_payment: KeyError {exc}")