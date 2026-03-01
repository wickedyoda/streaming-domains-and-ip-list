#!/usr/bin/env python3
"""Validate domain/IP/ASN list files in this repository."""

from __future__ import annotations

import ipaddress
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

FILE_RULES: dict[str, str] = {
    "bypass_sites.txt": "mixed",
    "bamboo_printer/bamboo_domains.txt": "mixed",
    "social_media/social_media.txt": "mixed",
    "streaming_services/streaming_domains_whitelist.txt": "mixed",
    "porn/known_porn_domains_v2.txt": "mixed",
    "netflix/router-list.txt": "mixed",
    "netflix/domains.md": "mixed",
    "netflix/ipv4-address.md": "ipv4",
    "netflix/ipv6-address.md": "ipv6",
    "netflix/ans.md": "asn",
}

DOMAIN_LABEL_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")
ASN_RE = re.compile(r"^AS\d+$")


def strip_inline_comment(value: str) -> str:
    # Keep the left side when inline comments are formatted like: "entry  # note"
    return re.split(r"\s+#", value, maxsplit=1)[0].strip()


def parse_cidr(value: str) -> ipaddress._BaseNetwork | None:
    if "/" not in value:
        return None
    try:
        return ipaddress.ip_network(value, strict=False)
    except ValueError:
        return None


def is_domain(value: str) -> bool:
    candidate = value
    if candidate.startswith("*."):
        candidate = candidate[2:]
    if candidate != candidate.lower():
        return False
    if len(candidate) > 253:
        return False
    if "." not in candidate or candidate.startswith(".") or candidate.endswith("."):
        return False
    parts = candidate.split(".")
    return all(DOMAIN_LABEL_RE.match(part) for part in parts)


def validate_token(mode: str, token: str) -> bool:
    if mode == "asn":
        return bool(ASN_RE.match(token.upper()))

    network = parse_cidr(token)
    if mode == "ipv4":
        return network is not None and network.version == 4
    if mode == "ipv6":
        return network is not None and network.version == 6
    if mode == "mixed":
        return is_domain(token) or network is not None
    raise ValueError(f"Unknown mode: {mode}")


def normalized_token(mode: str, token: str) -> str:
    if mode == "asn":
        return token.upper()
    return token.lower()


def validate_file(path: Path, mode: str) -> list[str]:
    errors: list[str] = []
    seen: dict[str, int] = {}

    if not path.exists():
        return [f"{path}: file not found"]

    with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        for lineno, raw in enumerate(handle, start=1):
            if "\r" in raw:
                errors.append(f"{path}:{lineno}: CRLF/CR line ending is not allowed")

            line = raw.rstrip("\n")
            if line != line.rstrip(" \t"):
                errors.append(f"{path}:{lineno}: trailing whitespace is not allowed")

            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            token = strip_inline_comment(stripped)
            if not token:
                continue

            if not validate_token(mode, token):
                errors.append(f"{path}:{lineno}: invalid entry for {mode}: {token}")
                continue

            key = normalized_token(mode, token)
            if key in seen:
                errors.append(
                    f"{path}:{lineno}: duplicate entry (first at line {seen[key]}): {token}"
                )
            else:
                seen[key] = lineno

    return errors


def main() -> int:
    all_errors: list[str] = []

    for relative_path, mode in FILE_RULES.items():
        path = REPO_ROOT / relative_path
        all_errors.extend(validate_file(path, mode))

    if all_errors:
        print("Validation failed:\n")
        for error in all_errors:
            print(f"- {error}")
        return 1

    print(f"Validation passed for {len(FILE_RULES)} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
