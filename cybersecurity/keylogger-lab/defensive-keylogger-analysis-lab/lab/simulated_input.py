"""
Safe Synthetic Telemetry Generator
===================================

Author:
    Jonatan "Johnny" Rassekhnia (@J-01R)

Role:
    Cybersecurity & Information Security Researcher

Project:
    Defensive Keylogger Analysis Lab

Description:
    Generates safe synthetic keyboard-input telemetry for testing
    defensive detection and forensic-analysis components.

Security Scope:
    This module never reads from the keyboard and never captures
    real user input. All generated events are synthetic test data.

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
import random
from datetime import datetime, timezone
from pathlib import Path


def generate_events(
    count: int = 12,
    process_name: str = "lab_simulator.exe",
) -> list[dict]:
    """Generate synthetic input events for defensive testing.

    Args:
        count: Number of synthetic events to generate.
        process_name: Process name to associate with the test events.

    Returns:
        A list of synthetic telemetry events.

    Notes:
        No real keyboard input is accessed or recorded.
    """
    keys = [
        "KEY_EVENT_A",
        "KEY_EVENT_B",
        "KEY_EVENT_ENTER",
        "KEY_EVENT_SPACE",
    ]

    return [
        {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": "synthetic_input",
            "process_name": process_name,
            "pid": 0,
            "sequence": index + 1,
            "synthetic": True,
            "value": random.choice(keys),
        }
        for index in range(count)
    ]


def write_jsonl(events: list[dict], output: Path) -> None:
    """Write telemetry events to a JSON Lines file.

    Args:
        events: Synthetic telemetry events to write.
        output: Destination JSONL file.
    """
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", encoding="utf-8") as handle:
        for event in events:
            handle.write(json.dumps(event) + "\n")


def main() -> None:
    """Parse command-line arguments and generate synthetic telemetry."""
    parser = argparse.ArgumentParser(
        description="Generate safe synthetic input telemetry."
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/synthetic_events.jsonl"),
        help="Output JSONL file.",
    )

    parser.add_argument(
        "--count",
        type=int,
        default=12,
        help="Number of synthetic events to generate.",
    )

    args = parser.parse_args()

    if args.count < 1 or args.count > 1000:
        raise SystemExit("--count must be between 1 and 1000")

    events = generate_events(args.count)
    write_jsonl(events, args.output)

    print(
        f"Generated {len(events)} synthetic events -> {args.output}"
    )


if __name__ == "__main__":
    main()