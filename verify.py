#!/usr/bin/env python3
"""One-command verification entry point for the public publication snapshot.

This program verifies public snapshot integrity, publication-metadata
consistency, the privacy boundary, the frozen PDF when present, and finite
certificates/computational claims. It does not formally verify the analytic
proofs.
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

FORBIDDEN_PUBLIC_TEXT = (
    "taishiwoidake/" + "QTRAC",
    "canonical_" + "repository",
    "research_source_" + "commit",
    "QTRAC-" + "TAIL-",
    "papers/" + "tail/",
    "checkers/" + "tail/",
    "certificates/" + "tail/",
    "excluded_" + "from_v1",
    "Xime" + "ste",
    "Arithmetic " + "Power-Lift",
    "Closed " + "Control",
    "Chat" + "GPT",
    "AI-" + "generated",
    "chat " + "history",
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load_json(name: str) -> dict:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def verify_lock() -> tuple[dict, dict]:
    lock = load_json("PUBLICATION_LOCK.json")
    manifest_path = ROOT / "SOURCE_MANIFEST.json"
    if not manifest_path.is_file():
        raise RuntimeError("missing SOURCE_MANIFEST.json")

    actual_manifest = sha256_file(manifest_path)
    expected_manifest = lock.get("source_manifest_sha256")
    if actual_manifest != expected_manifest:
        raise RuntimeError(
            "source manifest hash mismatch\n"
            f" expected {expected_manifest}\n"
            f" actual   {actual_manifest}"
        )

    manifest = load_json("SOURCE_MANIFEST.json")
    locked = {
        (item["destination"], item["sha256"], item.get("role"))
        for item in lock["artifacts"]
    }
    manifested = {
        (item["path"], item["sha256"], item.get("role"))
        for item in manifest["artifacts"]
    }
    if locked != manifested:
        raise RuntimeError("SOURCE_MANIFEST.json and PUBLICATION_LOCK.json disagree")

    for item in lock["artifacts"]:
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
    return lock, manifest


def verify_metadata(lock: dict, manifest: dict) -> dict:
    release = load_json("RELEASE.json")
    fields = ("publication_id", "paper_version", "certificate_schema")
    for field in fields:
        values = (lock.get(field), manifest.get(field), release.get(field))
        if len(set(values)) != 1:
            raise RuntimeError(f"metadata disagreement for {field}: {values}")

    if manifest.get("title") != release.get("title"):
        raise RuntimeError("title disagreement between SOURCE_MANIFEST.json and RELEASE.json")

    manifest_pdf = manifest.get("technical_preprint", {})
    release_pdf = release.get("technical_preprint", {})
    for field in ("pdf_sha256", "pages", "reproducible_build"):
        if manifest_pdf.get(field) != release_pdf.get(field):
            raise RuntimeError(f"technical_preprint disagreement for {field}")

    return release


def verify_privacy_boundary() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for forbidden in FORBIDDEN_PUBLIC_TEXT:
            if forbidden in content:
                rel = path.relative_to(ROOT)
                raise RuntimeError(f"forbidden public text {forbidden!r} in {rel}")


def verify_pdf(release: dict) -> bool:
    pdf_path = ROOT / "paper" / "preprint_v1.pdf"
    if not pdf_path.is_file():
        return False
    expected = release["technical_preprint"]["pdf_sha256"]
    actual = sha256_file(pdf_path)
    if actual != expected:
        raise RuntimeError(
            "frozen PDF hash mismatch\n"
            f" expected {expected}\n"
            f" actual   {actual}"
        )
    return True


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
        lock, manifest = verify_lock()
        print("[PASS] snapshot integrity")

        release = verify_metadata(lock, manifest)
        print("[PASS] publication metadata consistency")

        verify_privacy_boundary()
        print("[PASS] privacy boundary")

        pdf_present = verify_pdf(release)
        if pdf_present:
            print("[PASS] frozen PDF hash")
        else:
            print("[INFO] frozen PDF not present in this source-only export")
    except Exception as exc:
        print("[FAIL] publication snapshot")
        print(exc)
        return 1

    for label, path in SUITES:
        run_suite(label, path)

    print("All finite certificates and computational claims passed.")
    print("Analytic proofs are contained in paper/proofs/ and are not formally verified here.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
