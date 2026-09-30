"""
Process Snapshot Tests
=======================

Author:
    Jonatan "Johnny" Rassekhnia (@J-01R)

Role:
    Cybersecurity & Information Security Researcher

Project:
    Defensive Keylogger Analysis Lab

Description:
    Validates that the process-monitoring component returns process
    records containing the metadata required by the forensic workflow.

Security Scope:
    This test validates locally collected process metadata. It does not
    capture keyboard input or inspect user-entered content.

Copyright:
    Copyright (c) 2026 Jonatan "Johnny" Rassekhnia
    All Rights Reserved.

License:
    See the repository LICENSE file.
"""

from detection.process_monitor import snapshot_processes


def test_process_snapshot_has_expected_fields():
    """Verify that process snapshots contain the required metadata."""
    processes = snapshot_processes()

    assert processes

    assert {
        "pid",
        "name",
        "exe",
        "username",
        "create_time",
    } <= set(processes[0])