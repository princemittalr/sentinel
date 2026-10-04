"""Show that every billing-service pattern file crashes on a token with no exp claim.

Run from the project root:
    python demo_env\\scripts\\repro_billing.py
"""
import sys
from pathlib import Path

import jwt

SERVICE_DIR = Path(__file__).resolve().parent.parent / "services" / "billing-service"
sys.path.insert(0, str(SERVICE_DIR))

from app.invoice_links import resolve_invoice_link  # noqa: E402
from app.jwt_validation import ALGORITHM, SECRET_KEY, validate_token  # noqa: E402
from app.plan_changes import authorize_plan_change  # noqa: E402

token = jwt.encode({"sub": "user-1"}, SECRET_KEY, algorithm=ALGORITHM)

checks = {
    "jwt_validation.validate_token": lambda: validate_token(token),
    "invoice_links.resolve_invoice_link": lambda: resolve_invoice_link(token),
    "plan_changes.authorize_plan_change": lambda: authorize_plan_change(token),
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