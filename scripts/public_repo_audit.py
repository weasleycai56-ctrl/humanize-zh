#!/usr/bin/env python3
"""Check this repository for common accidental-publication risks."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SKIP_DIRS = {".git", ".venv", "__pycache__", "dist", "build"}
SKIP_FILES = {"public_repo_audit.py"}
TEXT_LIMIT = 2_000_000
BINARY_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".gz", ".mp4", ".mov"}
CHECKS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "token-like assignment": re.compile(
        r"(?i)(?:api[_-]?key|secret|access[_-]?token|password)\s*[:=]\s*['\"][A-Za-z0-9_./+\-=]{16,}['\"]"
    ),
    "personal macOS path": re.compile(r"/Users/[A-Za-z0-9._-]+/"),
    "email address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
}


def files_under(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in SKIP_FILES:
            continue
        yield path


def audit(root: Path) -> list[str]:
    findings: list[str] = []
    for path in files_under(root):
        rel = path.relative_to(root)
        size = path.stat().st_size
        if size > TEXT_LIMIT:
            findings.append(f"large file ({size} bytes): {rel}")
            continue
        if path.suffix.lower() in BINARY_SUFFIXES:
            findings.append(f"binary/media file needs license review: {rel}")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(f"unreadable binary file needs review: {rel}")
            continue
        for label, pattern in CHECKS.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                findings.append(f"{label}: {rel}:{line}")
    required = ["LICENSE", "SECURITY.md", "CODE_OF_CONDUCT.md", "CONTRIBUTING.md"]
    for name in required:
        if not (root / name).is_file():
            findings.append(f"missing governance file: {name}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    findings = audit(args.root.resolve())
    print("Public repository audit")
    print(f"Root: {args.root.resolve()}")
    if findings:
        for finding in findings:
            print(f"[REVIEW] {finding}")
        print(f"Result: {len(findings)} item(s) need review")
        return 1
    print("[PASS] No configured secret, privacy, large-file, or binary-media findings")
    print("[PASS] Required governance files are present")
    print("Result: suitable for maintainer review before publication")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
