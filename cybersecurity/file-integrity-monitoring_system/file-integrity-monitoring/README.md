# File Integrity Monitoring System

A defensive cybersecurity laboratory project for monitoring files and detecting unauthorized filesystem changes using SHA-256 integrity verification.

## Overview

The File Integrity Monitoring System establishes a known-good baseline of files within a monitored directory and compares the current filesystem state against that baseline.

The system detects:

- File creation
- File deletion
- File modification
- Content replacement at an existing file path, reported as `MODIFIED`

Detected changes can be reported through a forensic JSON report.

The project also supports continuous polling-based monitoring with session-based alert deduplication.

## Security Purpose

File Integrity Monitoring (FIM) is a defensive security technique used to identify unexpected changes to files that are considered important, sensitive, or protected.

This laboratory demonstrates how integrity monitoring can be used to identify filesystem changes that may indicate:

- Unauthorized modification
- Unexpected file creation
- File deletion
- Configuration tampering
- Replacement of protected content
- Other filesystem integrity violations

The project is designed for authorized laboratory and defensive security research.

## Features

### SHA-256 Integrity Verification

Files are hashed using SHA-256.

The generated baseline records:

- Relative file path
- SHA-256 hash
- File size
- Last modification timestamp

### Baseline Creation

A known-good filesystem state can be captured as a JSON baseline.

Example:

```powershell
python -m detection.integrity_monitor lab\protected