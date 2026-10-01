#!/usr/bin/env python3
"""One-command verification entry point for the public publication snapshot.

This program verifies snapshot integrity plus finite certificates and
computational claims. It does not formally verify the analytic proofs.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent

SUITES = [
    ("Theorem A finite construction checks", ROOT / "checkers" / "reachability_rounding.py"),
    ("Theorem B finite certificate", ROOT / "checkers" / "four_edge_minimality.py"),
    ("Theorem C exact primal/dual certificate", ROOT / "checkers" / "integrality_gap.py"),
    ("Theorem D stopping-tree certificate", ROOT / "checkers" / "stopping_tree.py"),
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def verify_lock() -> None:
    lock_path = ROOT / "PUBLICATION_LOCK.json"
    data = json.loads(lock_path.read_text(encoding="utf-8"))
    for item in data["artifacts"]:
        path = ROOT / item["destination"]
        if not path.is_file():
            raise RuntimeError(f"missing exported artifact: {item['destination']}")
        actual = sha256_file(path)
        if actual != item["sha256"]:
            raise RuntimeError(
                f"artifact hash mismatch: {item['destination']}\n"
                f" expected {item['sha256']}\n"
                f" actual   {actual}"
            )


def run_suite(label: str, path: Path) -> None:
    proc = subprocess.run(
        [sys.executable, "-O", str(path)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if proc.returncode != 0:
        print(f"[FAIL] {label}")
        print(proc.stdout)
        raise SystemExit(proc.returncode or 1)
    print(f"[PASS] {label}")


def main() -> int:
    try:
        verify_lock()
    except Exception as exc:
        print("[FAIL] snapshot integrity")
        print(exc)
        return 1

    print("[PASS] snapshot integrity")
    for label, path in SUITES:
        run_suite(label, path)

    print("All finite certificates and computational claims passed.")
    print("Analytic proofs are contained in paper/proofs/ and are not formally verified here.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
