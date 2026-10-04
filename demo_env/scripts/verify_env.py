"""Verify the Sentinel demo environment is in its expected baseline state.

Run from the project root:
    python demo_env\\scripts\\verify_env.py

Exit code 0 means the baseline is intact. Exit code 1 means something drifted.
"""
import re
import subprocess
import sys
from pathlib import Path

SERVICES_DIR = Path(__file__).resolve().parent.parent / "services"

# service name -> (expected pattern files, expected tests)
EXPECTED = {
    "auth-service": (5, 20),
    "checkout-service": (4, 18),
    "billing-service": (3, 17),
    "profile-service": (3, 17),
    "notifications-service": (2, 17),
}

PATTERN = '["exp"]'


def count_pattern_files(service_dir: Path) -> int:
    """Count app/*.py files that read the exp claim by direct indexing."""
    return sum(
        1
        for path in (service_dir / "app").glob("*.py")
        if PATTERN in path.read_text(encoding="utf-8")
    )


def run_tests(service_dir: Path) -> int:
    """Run pytest inside the service folder and return the passed count (-1 on failure)."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"],
        cwd=service_dir,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return -1
    match = re.search(r"(\d+) passed", result.stdout)
    return int(match.group(1)) if match else -1


def lint_clean(service_dir: Path) -> bool:
    result = subprocess.run(
        [sys.executable, "-m", "ruff", "check", ".", "--no-cache"],
        cwd=service_dir,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def main() -> int:
    total_files = 0
    total_tests = 0
    problems = []

    print(f"{'service':<24}{'pattern files':<16}{'tests':<10}{'lint':<8}status")
    print("-" * 66)

    for name, (want_files, want_tests) in EXPECTED.items():
        service_dir = SERVICES_DIR / name
        files = count_pattern_files(service_dir)
        tests = run_tests(service_dir)
        lint = lint_clean(service_dir)

        total_files += files
        total_tests += max(tests, 0)

        ok = files == want_files and tests == want_tests and lint
        if not ok:
            problems.append(name)

        print(
            f"{name:<24}{files:<16}{tests if tests >= 0 else 'FAIL':<10}"
            f"{'clean' if lint else 'ERRORS':<8}{'ok' if ok else 'DRIFT'}"
        )

    print("-" * 66)
    print(f"{'TOTAL':<24}{total_files:<16}{total_tests:<10}")

    want_total_files = sum(f for f, _ in EXPECTED.values())
    want_total_tests = sum(t for _, t in EXPECTED.values())

    if problems or total_files != want_total_files or total_tests != want_total_tests:
        print(f"\nBASELINE BROKEN. Check: {', '.join(problems) or 'totals'}")
        return 1

    print(f"\nBASELINE INTACT: {total_files} pattern files, {total_tests} existing tests.")
    return 0


if __name__ == "__main__":
    sys.exit(main())