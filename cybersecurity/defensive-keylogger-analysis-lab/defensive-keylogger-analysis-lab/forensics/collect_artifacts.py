"""
Endpoint Process Metadata Collector
===================================

Author:
    Jonatan "Johnny" Rassekhnia (@J-01R)

Role:
    Cybersecurity & Information Security Researcher

Project:
    Defensive Keylogger Analysis Lab

Description:
    Collects minimal, reproducible endpoint process metadata for
    defensive investigation and forensic analysis.

Security Scope:
    This module collects endpoint metadata required by the laboratory's
    forensic workflow. It does not collect keyboard input or user-entered
    content.

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
import platform
import socket
from datetime import datetime, timezone
from pathlib import Path

from detection.process_monitor import snapshot_processes


def collect() -> dict:
    """Collect minimal endpoint and process metadata.

    Returns:
        A dictionary containing the collection timestamp, hostname,
        operating-system platform information, Python version, and
        a snapshot of running processes.
    """
    return {
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "processes": snapshot_processes(),
    }


def main() -> None:
    """Collect endpoint metadata and write the forensic snapshot."""
    parser = argparse.ArgumentParser(
        description="Collect minimal endpoint process metadata."
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/process_snapshot.json"),
        help="Output JSON file for the forensic process snapshot.",
    )

    args = parser.parse_args()

    data = collect()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8",
    )

    print(f"Wrote forensic snapshot -> {args.output}")


if __name__ == "__main__":
    main()