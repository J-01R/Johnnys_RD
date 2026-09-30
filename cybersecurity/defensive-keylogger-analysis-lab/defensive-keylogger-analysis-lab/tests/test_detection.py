"""
Detection Rule Tests
=====================

Author:
    Jonatan "Johnny" Rassekhnia (@J-01R)

Role:
    Cybersecurity & Information Security Researcher

Project:
    Defensive Keylogger Analysis Lab

Description:
    Validates the behavior of the defensive detection rules used to
    identify synthetic input activity and unexpected input volume.

Security Scope:
    These tests operate only on synthetic laboratory telemetry. They do not
    capture keyboard input or determine malicious activity on their own.

Copyright:
    Copyright (c) 2026 Jonatan "Johnny" Rassekhnia
    All Rights Reserved.

License:
    See the repository LICENSE file.
"""

from detection.detection_rules import detect


def test_synthetic_input_generates_high_finding():
    """Verify that synthetic input activity generates a HIGH finding."""
    events = [
        {
            "synthetic": True,
            "process_name": "lab_simulator.exe",
            "event_type": "synthetic_input",
        }
    ]

    findings = detect(events)

    assert any(
        finding["rule_id"] == "SYNTHETIC_INPUT_ACTIVITY"
        for finding in findings
    )


def test_high_volume_generates_medium_finding():
    """Verify that input above the configured threshold generates a MEDIUM finding."""
    events = [
        {
            "synthetic": True,
            "process_name": "lab_simulator.exe",
        }
        for _ in range(11)
    ]

    findings = detect(events, volume_threshold=10)

    assert any(
        finding["rule_id"] == "UNEXPECTED_INPUT_VOLUME"
        for finding in findings
    )


def test_normal_event_is_ignored():
    """Verify that non-synthetic events are ignored by the detection rules."""
    assert detect(
        [
            {
                "synthetic": False,
                "process_name": "notepad.exe",
            }
        ]
    ) == []