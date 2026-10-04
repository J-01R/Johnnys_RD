"""
File Integrity Monitoring - Detection and Forensic Reporting Engine
=====================================================================

Author:
    Jonatan "Johnny" Rassekhnia (@J-01R)

Role:
    Cybersecurity & Information Security Researcher

Project:
    File Integrity Monitoring System

Description:
    Creates a SHA-256 file integrity baseline, compares the current
    filesystem state against that baseline, detects file creation,
    deletion, and modification events, generates forensic reports,
    and supports continuous directory monitoring.

    Continuous monitoring includes session-based alert deduplication
    to prevent the same persistent integrity violation from being
    reported repeatedly during every monitoring interval.

Security Scope:
    This module is intended for authorized defensive monitoring of
    directories owned or explicitly controlled by the researcher.

    It does not execute monitored files, capture keyboard input,
    or modify protected files.

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
import time
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path: Path) -> str:
    """Calculate the SHA-256 hash of a file.

    Args:
        path: File to hash.

    Returns:
        SHA-256 digest as a hexadecimal string.
    """
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def build_baseline(directory: Path) -> dict:
    """Create a file integrity baseline for a directory.

    Args:
        directory: Directory to monitor.

    Returns:
        Dictionary containing baseline metadata and file records.
    """
    files = {}

    for path in directory.rglob("*"):
        if not path.is_file():
            continue

        relative_path = str(path.relative_to(directory))
        stat = path.stat()

        files[relative_path] = {
            "sha256": sha256_file(path),
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(
                stat.st_mtime,
                tz=timezone.utc,
            ).isoformat(),
        }

    return {
        "created_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "directory": str(
            directory.resolve()
        ),
        "files": files,
    }


def load_baseline(path: Path) -> dict:
    """Load a previously generated JSON integrity baseline.

    Args:
        path: Path to the baseline JSON file.

    Returns:
        Parsed baseline data.
    """
    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def compare_baseline(
    baseline: dict,
    current: dict,
) -> list[dict]:
    """Compare a baseline against the current filesystem state.

    Args:
        baseline: Previously recorded file integrity baseline.
        current: Newly generated file integrity state.

    Returns:
        A list of detected file changes with forensic metadata.
    """
    findings = []

    baseline_files = baseline.get(
        "files",
        {},
    )

    current_files = current.get(
        "files",
        {},
    )

    baseline_paths = set(
        baseline_files
    )

    current_paths = set(
        current_files
    )

    detected_at = datetime.now(
        timezone.utc
    ).isoformat()

    # Detect newly created files.
    for path in sorted(
        current_paths - baseline_paths
    ):
        current_file = current_files[path]

        findings.append(
            {
                "event": "CREATED",
                "path": path,
                "detected_at": detected_at,
                "reason": (
                    "File was not present in "
                    "the baseline."
                ),
                "current_sha256": (
                    current_file["sha256"]
                ),
                "current_size": (
                    current_file["size"]
                ),
                "current_modified": (
                    current_file["modified"]
                ),
            }
        )

    # Detect deleted files.
    for path in sorted(
        baseline_paths - current_paths
    ):
        baseline_file = baseline_files[path]

        findings.append(
            {
                "event": "DELETED",
                "path": path,
                "detected_at": detected_at,
                "reason": (
                    "File from the baseline "
                    "is no longer present."
                ),
                "previous_sha256": (
                    baseline_file["sha256"]
                ),
                "previous_size": (
                    baseline_file["size"]
                ),
                "previous_modified": (
                    baseline_file["modified"]
                ),
            }
        )

    # Detect modifications.
    for path in sorted(
        baseline_paths & current_paths
    ):
        baseline_file = baseline_files[path]
        current_file = current_files[path]

        if (
            baseline_file["sha256"]
            != current_file["sha256"]
        ):
            findings.append(
                {
                    "event": "MODIFIED",
                    "path": path,
                    "detected_at": detected_at,
                    "reason": (
                        "SHA-256 hash changed."
                    ),
                    "previous_sha256": (
                        baseline_file["sha256"]
                    ),
                    "current_sha256": (
                        current_file["sha256"]
                    ),
                    "previous_size": (
                        baseline_file["size"]
                    ),
                    "current_size": (
                        current_file["size"]
                    ),
                    "previous_modified": (
                        baseline_file["modified"]
                    ),
                    "current_modified": (
                        current_file["modified"]
                    ),
                }
            )

    return findings


def finding_key(finding: dict) -> tuple:
    """Create a stable identifier for an integrity finding.

    Args:
        finding: Integrity finding dictionary.

    Returns:
        Tuple identifying the finding's current state.
    """
    return (
        finding["event"],
        finding["path"],
        finding.get("previous_sha256"),
        finding.get("current_sha256"),
        finding.get("previous_size"),
        finding.get("current_size"),
    )


def write_report(
    report_path: Path,
    directory: Path,
    baseline_path: Path,
    findings: list[dict],
) -> None:
    """Write detected integrity events to a JSON report.

    Args:
        report_path: Destination for the forensic report.
        directory: Monitored directory.
        baseline_path: Baseline used for comparison.
        findings: Detected integrity events.
    """
    report = {
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "monitored_directory": str(
            directory.resolve()
        ),
        "baseline": str(
            baseline_path.resolve()
        ),
        "finding_count": len(findings),
        "findings": findings,
    }

    report_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_path.write_text(
        json.dumps(
            report,
            indent=2,
        ),
        encoding="utf-8",
    )


def watch_directory(
    directory: Path,
    baseline_path: Path,
    report_path: Path,
    interval: int,
) -> None:
    """Continuously monitor a directory against a baseline.

    Args:
        directory: Directory to monitor.
        baseline_path: Path to the known-good baseline.
        report_path: Path for forensic reports.
        interval: Seconds between integrity checks.
    """
    baseline = load_baseline(
        baseline_path
    )

    reported_findings = set()

    print(
        f"Continuous monitoring started for: "
        f"{directory.resolve()}"
    )

    print(
        f"Check interval: {interval} second(s)"
    )

    print(
        "Press Ctrl+C to stop monitoring.\n"
    )

    try:
        while True:
            current = build_baseline(
                directory
            )

            findings = compare_baseline(
                baseline,
                current,
            )

            new_findings = [
                finding
                for finding in findings
                if finding_key(finding)
                not in reported_findings
            ]

            if new_findings:
                write_report(
                    report_path=report_path,
                    directory=directory,
                    baseline_path=baseline_path,
                    findings=new_findings,
                )

                print(
                    f"[ALERT] Detected "
                    f"{len(new_findings)} new "
                    f"change(s):"
                )

                for finding in new_findings:
                    print(
                        f"  [{finding['event']}] "
                        f"{finding['path']} - "
                        f"{finding['reason']}"
                    )

                    reported_findings.add(
                        finding_key(finding)
                    )

                print(
                    f"  Report: {report_path}\n"
                )

            else:
                print(
                    "[OK] No new changes detected."
                )

            time.sleep(interval)

    except KeyboardInterrupt:
        print(
            "\nMonitoring stopped."
        )


def main() -> None:
    """Create, verify, or continuously monitor a baseline."""
    parser = argparse.ArgumentParser(
        description=(
            "Create, verify, or continuously monitor "
            "a SHA-256 file integrity baseline."
        )
    )

    parser.add_argument(
        "directory",
        type=Path,
        help="Directory to monitor.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "data/baseline.json"
        ),
        help=(
            "Path to the baseline JSON file."
        ),
    )

    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "reports/integrity_report.json"
        ),
        help=(
            "Path to the forensic JSON report."
        ),
    )

    parser.add_argument(
        "--check",
        action="store_true",
        help=(
            "Compare the current directory "
            "against the existing baseline."
        ),
    )

    parser.add_argument(
        "--watch",
        action="store_true",
        help=(
            "Continuously monitor the directory "
            "against the existing baseline."
        ),
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=5,
        help=(
            "Seconds between monitoring checks "
            "(default: 5)."
        ),
    )

    args = parser.parse_args()

    if args.interval < 1:
        raise SystemExit(
            "Interval must be at least 1 second."
        )

    if not args.directory.is_dir():
        raise SystemExit(
            f"Directory does not exist: "
            f"{args.directory}"
        )

    if args.check and args.watch:
        raise SystemExit(
            "--check and --watch cannot "
            "be used together."
        )

    if args.watch:
        if not args.output.exists():
            raise SystemExit(
                f"Baseline does not exist: "
                f"{args.output}"
            )

        watch_directory(
            directory=args.directory,
            baseline_path=args.output,
            report_path=args.report,
            interval=args.interval,
        )

        return

    if args.check:
        if not args.output.exists():
            raise SystemExit(
                f"Baseline does not exist: "
                f"{args.output}"
            )

        baseline = load_baseline(
            args.output
        )

        current = build_baseline(
            args.directory
        )

        findings = compare_baseline(
            baseline,
            current,
        )

        if not findings:
            print(
                "Integrity check passed: "
                "no changes detected."
            )
            return

        write_report(
            report_path=args.report,
            directory=args.directory,
            baseline_path=args.output,
            findings=findings,
        )

        print(
            f"Integrity check detected "
            f"{len(findings)} change(s):"
        )

        for finding in findings:
            print(
                f"[{finding['event']}] "
                f"{finding['path']} - "
                f"{finding['reason']}"
            )

        print(
            f"\nForensic report written to: "
            f"{args.report}"
        )

        return

    baseline = build_baseline(
        args.directory
    )

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    args.output.write_text(
        json.dumps(
            baseline,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        f"Baseline created for "
        f"{args.directory} "
        f"-> {args.output}"
    )


if __name__ == "__main__":
    main()