"""
File Integrity Monitoring - Automated Tests
=============================================

Author:
    Jonatan "Johnny" Rassekhnia (@J-01R)

Role:
    Cybersecurity & Information Security Researcher

Project:
    File Integrity Monitoring System

Description:
    Automated tests for baseline creation and integrity change
    detection.

Security Scope:
    Tests operate exclusively against temporary laboratory
    directories created by the test framework.

Copyright:
    Copyright (c) 2026 Jonatan "Johnny" Rassekhnia
    All Rights Reserved.

License:
    This project is not released under an open-source license.
    See the repository LICENSE file for usage restrictions.
"""

from pathlib import Path

from detection.integrity_monitor import (
    build_baseline,
    compare_baseline,
)


def test_unchanged_file_has_no_findings(
    tmp_path: Path,
) -> None:
    """Verify that an unchanged file produces no findings."""
    test_file = tmp_path / "important.txt"
    test_file.write_text(
        "original content",
        encoding="utf-8",
    )

    baseline = build_baseline(tmp_path)
    current = build_baseline(tmp_path)

    findings = compare_baseline(
        baseline,
        current,
    )

    assert findings == []


def test_created_file_is_detected(
    tmp_path: Path,
) -> None:
    """Verify that a newly created file is detected."""
    original = tmp_path / "important.txt"
    original.write_text(
        "original content",
        encoding="utf-8",
    )

    baseline = build_baseline(tmp_path)

    created = tmp_path / "unauthorized.txt"
    created.write_text(
        "new file",
        encoding="utf-8",
    )

    current = build_baseline(tmp_path)

    findings = compare_baseline(
        baseline,
        current,
    )

    assert len(findings) == 1
    assert findings[0]["event"] == "CREATED"
    assert findings[0]["path"] == "unauthorized.txt"


def test_deleted_file_is_detected(
    tmp_path: Path,
) -> None:
    """Verify that a deleted baseline file is detected."""
    test_file = tmp_path / "important.txt"
    test_file.write_text(
        "original content",
        encoding="utf-8",
    )

    baseline = build_baseline(tmp_path)

    test_file.unlink()

    current = build_baseline(tmp_path)

    findings = compare_baseline(
        baseline,
        current,
    )

    assert len(findings) == 1
    assert findings[0]["event"] == "DELETED"
    assert findings[0]["path"] == "important.txt"


def test_modified_file_is_detected(
    tmp_path: Path,
) -> None:
    """Verify that a modified file is detected."""
    test_file = tmp_path / "important.txt"
    test_file.write_text(
        "original content",
        encoding="utf-8",
    )

    baseline = build_baseline(tmp_path)

    test_file.write_text(
        "modified content",
        encoding="utf-8",
    )

    current = build_baseline(tmp_path)

    findings = compare_baseline(
        baseline,
        current,
    )

    assert len(findings) == 1
    assert findings[0]["event"] == "MODIFIED"
    assert findings[0]["path"] == "important.txt"
    assert (
        findings[0]["previous_sha256"]
        != findings[0]["current_sha256"]
    )


def test_multiple_changes_are_detected(
    tmp_path: Path,
) -> None:
    """Verify that multiple integrity events are detected together."""
    modified = tmp_path / "important.txt"
    deleted = tmp_path / "config.txt"

    modified.write_text(
        "original content",
        encoding="utf-8",
    )

    deleted.write_text(
        "configuration",
        encoding="utf-8",
    )

    baseline = build_baseline(tmp_path)

    modified.write_text(
        "modified content",
        encoding="utf-8",
    )

    deleted.unlink()

    created = tmp_path / "unauthorized.txt"
    created.write_text(
        "new file",
        encoding="utf-8",
    )

    current = build_baseline(tmp_path)

    findings = compare_baseline(
        baseline,
        current,
    )

    events = {
        finding["event"]
        for finding in findings
    }

    assert len(findings) == 3
    assert events == {
        "CREATED",
        "DELETED",
        "MODIFIED",
    }