"""
Artifact and Timeline Tests
============================

Author:
    Jonatan "Johnny" Rassekhnia (@J-01R)

Role:
    Cybersecurity & Information Security Researcher

Project:
    Defensive Keylogger Analysis Lab

Description:
    Validates artifact hashing and investigation timeline construction
    used by the defensive forensic workflow.

Security Scope:
    These tests operate only on temporary laboratory data and synthetic
    telemetry. They do not capture keyboard input or inspect private
    application content.

Copyright:
    Copyright (c) 2026 Jonatan "Johnny" Rassekhnia
    All Rights Reserved.

License:
    See the repository LICENSE file.
"""

from pathlib import Path

from detection.artifact_scanner import scan
from forensics.timeline import build_timeline


def test_artifact_hash_is_created(tmp_path: Path):
    """Verify that the artifact scanner generates a SHA-256 hash."""
    sample = tmp_path / "sample.txt"
    sample.write_text("lab artifact", encoding="utf-8")

    results = scan([sample])

    assert len(results) == 1
    assert len(results[0]["sha256"]) == 64


def test_timeline_contains_detection():
    """Verify that telemetry and detection records form a timeline."""
    rows = build_timeline(
        [
            {
                "timestamp": "2026-01-01T00:00:00Z",
                "event_type": "synthetic_input",
                "process_name": "lab_simulator.exe",
                "value": "KEY_EVENT_A",
            }
        ],
        [
            {
                "rule_id": "SYNTHETIC_INPUT_ACTIVITY",
                "process": "lab_simulator.exe",
                "rationale": "test",
            }
        ],
    )

    assert len(rows) == 2