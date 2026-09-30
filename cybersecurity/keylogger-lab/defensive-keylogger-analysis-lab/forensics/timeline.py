"""
Investigation Timeline Builder
==============================

Author:
    Jonatan "Johnny" Rassekhnia (@J-01R)

Role:
    Cybersecurity & Information Security Researcher

Project:
    Defensive Keylogger Analysis Lab

Description:
    Builds a simple investigation timeline by combining laboratory
    telemetry events with detection-engine findings and exporting
    the resulting timeline as CSV.

Security Scope:
    This module processes previously generated laboratory telemetry
    and detection results. It does not capture keyboard input or
    collect new endpoint data.

Copyright:
    Copyright (c) 2026 Jonatan "Johnny" Rassekhnia
    All Rights Reserved.

License:
    This project is not released under an open-source license.
    See the repository LICENSE file for usage restrictions.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    """Read non-empty JSON Lines records from a file.

    Args:
        path: Path to the JSONL telemetry file.

    Returns:
        A list of decoded JSON objects.
    """
    with path.open(encoding="utf-8") as handle:
        return [
            json.loads(line)
            for line in handle
            if line.strip()
        ]


def read_json(path: Path) -> list[dict]:
    """Read a JSON file containing a list of detection findings.

    Args:
        path: Path to the JSON detection file.

    Returns:
        A list of detection records.

        If the file does not exist, or the decoded JSON value is not
        a list, an empty list is returned.
    """
    if not path.exists():
        return []

    value = json.loads(path.read_text(encoding="utf-8"))

    return value if isinstance(value, list) else []


def build_timeline(
    events: list[dict],
    detections: list[dict],
) -> list[dict]:
    """Combine telemetry events and detections into a timeline.

    Args:
        events: Laboratory telemetry events.
        detections: Detection-engine findings.

    Returns:
        A combined list of timeline records sorted by timestamp.
    """
    timeline = [
        {
            "timestamp": event.get("timestamp"),
            "source": "synthetic_telemetry",
            "event": event.get("event_type"),
            "process": event.get("process_name"),
            "details": event.get("value"),
        }
        for event in events
    ]

    timeline.extend(
        {
            "timestamp": "",
            "source": "detection_engine",
            "event": finding.get("rule_id"),
            "process": finding.get("process"),
            "details": finding.get("rationale"),
        }
        for finding in detections
    )

    return sorted(
        timeline,
        key=lambda row: row["timestamp"] or "9999",
    )


def write_csv(rows: list[dict], output: Path) -> None:
    """Write investigation timeline records to CSV.

    Args:
        rows: Timeline records to export.
        output: Destination CSV file.
    """
    output.parent.mkdir(parents=True, exist_ok=True)

    fields = [
        "timestamp",
        "source",
        "event",
        "process",
        "details",
    ]

    with output.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    """Build and export the laboratory investigation timeline."""
    parser = argparse.ArgumentParser(
        description=(
            "Build an investigation timeline from lab events "
            "and detection findings."
        )
    )

    parser.add_argument(
        "--events",
        type=Path,
        default=Path("data/synthetic_events.jsonl"),
        help="JSONL file containing laboratory telemetry events.",
    )

    parser.add_argument(
        "--detections",
        type=Path,
        default=Path("reports/detections.json"),
        help="JSON file containing detection-engine findings.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/timeline.csv"),
        help="Output CSV timeline file.",
    )

    args = parser.parse_args()

    rows = build_timeline(
        read_jsonl(args.events),
        read_json(args.detections),
    )

    write_csv(rows, args.output)

    print(
        f"Wrote {len(rows)} timeline records -> {args.output}"
    )


if __name__ == "__main__":
    main()