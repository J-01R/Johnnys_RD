"""
Lab Artifact Scanner
====================

Author:
    Jonatan "Johnny" Rassekhnia (@J-01R)

Role:
    Cybersecurity & Information Security Researcher

Project:
    Defensive Keylogger Analysis Lab

Description:
    Provides a safe scanner for explicitly supplied, lab-owned artifacts.
    The scanner records basic file metadata and calculates SHA-256 hashes
    for forensic identification and reproducibility.

Security Scope:
    This module only examines files explicitly supplied to it by the user.
    It does not execute files, capture keyboard input, or inspect private
    application content.

Copyright:
    Copyright (c) 2026 Jonatan "Johnny" Rassekhnia
    All Rights Reserved.

License:
    This project is not released under an open-source license.
    See the repository LICENSE file for usage restrictions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    """Calculate the SHA-256 hash of a file.

    Args:
        path: Path to the file to hash.

    Returns:
        The hexadecimal SHA-256 digest of the file contents.

    Notes:
        The file is read in chunks to avoid loading the entire file
        into memory at once.
    """
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def scan(paths: list[Path]) -> list[dict]:
    """Collect metadata and SHA-256 hashes for supplied files.

    Args:
        paths: Files explicitly supplied for laboratory analysis.

    Returns:
        A list of file inventory records containing the path, size,
        SHA-256 hash, and lowercase file suffix.

    Notes:
        Directories and paths that are not regular files are ignored.
    """
    results = []

    for path in paths:
        if path.is_file():
            stat = path.stat()

            results.append(
                {
                    "path": str(path),
                    "size": stat.st_size,
                    "sha256": sha256(path),
                    "suffix": path.suffix.lower(),
                }
            )

    return results


def main() -> None:
    """Scan supplied lab artifacts and write a JSON inventory."""
    parser = argparse.ArgumentParser(
        description=(
            "Calculate metadata and SHA-256 hashes for "
            "lab-owned artifacts."
        )
    )

    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="Files to include in the laboratory artifact inventory.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/file_inventory.json"),
        help="Output JSON file for the artifact inventory.",
    )

    args = parser.parse_args()

    results = scan(args.paths)

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    args.output.write_text(
        json.dumps(results, indent=2),
        encoding="utf-8",
    )

    print(
        f"Scanned {len(results)} lab-owned files -> {args.output}"
    )


if __name__ == "__main__":
    main()