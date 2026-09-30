"""
Windows Process Inventory
=========================

Author:
    Jonatan "Johnny" Rassekhnia (@J-01R)

Role:
    Cybersecurity & Information Security Researcher

Project:
    Defensive Keylogger Analysis Lab

Description:
    Collects a lightweight inventory of running Windows processes for
    defensive analysis and forensic investigation.

Security Scope:
    This module collects process metadata from the local endpoint.
    It does not capture keyboard input, user-entered content, or
    application data.

Copyright:
    Copyright (c) 2026 Jonatan "Johnny" Rassekhnia
    All Rights Reserved.

License:
    This project is not released under an open-source license.
    See the repository LICENSE file for usage restrictions.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import psutil


def snapshot_processes() -> list[dict]:
    """Collect metadata for currently running processes.

    Returns:
        A list of process records containing PID, process name,
        executable path, username, and creation time.

    Notes:
        Processes that disappear during collection or cannot be
        accessed due to permissions are skipped.
    """
    results = []

    for proc in psutil.process_iter(
        ["pid", "name", "exe", "username", "create_time"]
    ):
        try:
            info = proc.info

            created = (
                datetime.fromtimestamp(
                    info["create_time"],
                    tz=timezone.utc,
                ).isoformat()
                if info.get("create_time")
                else None
            )

            results.append(
                {
                    "pid": info.get("pid"),
                    "name": info.get("name"),
                    "exe": info.get("exe"),
                    "username": info.get("username"),
                    "create_time": created,
                }
            )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            continue

    return sorted(
        results,
        key=lambda item: (item["name"] or "").lower(),
    )


def main() -> None:
    """Collect the process inventory and write it to JSON."""
    parser = argparse.ArgumentParser(
        description="Collect a lightweight Windows process inventory."
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/process_snapshot.json"),
        help="Output JSON file for the process snapshot.",
    )

    args = parser.parse_args()

    snapshot = snapshot_processes()

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    args.output.write_text(
        json.dumps(snapshot, indent=2),
        encoding="utf-8",
    )

    print(
        f"Captured {len(snapshot)} process records -> {args.output}"
    )


if __name__ == "__main__":
    main()