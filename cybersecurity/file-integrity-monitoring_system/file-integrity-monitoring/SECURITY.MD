# Security Policy

## File Integrity Monitoring System

This document describes the security scope, responsible use, reporting expectations, and limitations of the File Integrity Monitoring System.

## Security Purpose

The File Integrity Monitoring System is a defensive cybersecurity laboratory project designed to detect unexpected changes to files within an authorized monitored directory.

The system uses SHA-256 integrity verification to establish a known-good baseline and identify differences between the baseline and the current filesystem state.

The project is intended for:

- Defensive security research
- Cybersecurity education
- Detection engineering practice
- File integrity monitoring research
- Authorized laboratory testing
- Forensic analysis exercises

## Authorized Use

This project must only be used against systems, directories, and files that the user owns or has explicit authorization to monitor.

Examples of appropriate use include:

- Personal laboratory environments
- Test directories
- Systems owned by the researcher
- Authorized enterprise security testing
- Educational cybersecurity environments

Do not use this project to monitor files or systems without appropriate authorization.

## Security Monitoring Scope

The current implementation detects:

- File creation
- File deletion
- File modification
- Content replacement at an existing file path when the SHA-256 hash changes

A replacement at an existing path is classified by the system as a `MODIFIED` event.

The system does not determine whether a detected change is malicious.

A detected integrity change should therefore be treated as an indicator requiring investigation rather than automatic proof of compromise.

## Integrity Verification

The project uses SHA-256 hashes to compare files against a known-good baseline.

The baseline records information including:

- Relative file path
- SHA-256 hash
- File size
- Modification timestamp

If the current SHA-256 value differs from the baseline value, the file is reported as modified.

## Baseline Security

The integrity baseline is an important security artifact.

If an attacker can modify both:

```text
data/baseline.json