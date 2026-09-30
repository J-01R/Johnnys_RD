# Defensive Keylogger Analysis Lab

> A controlled Windows security lab for studying keylogger-like behavior through synthetic telemetry, endpoint monitoring, detection engineering, forensic collection, and mitigation analysis.

![Platform](https://img.shields.io/badge/platform-Windows%2011-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-yellow)
![Tests](https://img.shields.io/badge/tests-pytest-green)
![Safety](https://img.shields.io/badge/lab-safe%20simulation-brightgreen)

## Overview

This project recreates the defensive investigation workflow around a keylogger without collecting real keyboard input.

The lab generates synthetic endpoint events, monitors selected processes, applies transparent detection rules, collects forensic metadata, reconstructs a timeline, and produces mitigation-oriented findings.

### Safety boundary

This repository intentionally does **not** implement:

- real keyboard hooks
- keystroke capture
- credential collection
- clipboard theft
- persistence mechanisms
- stealth/evasion
- exfiltration

All input-related telemetry is synthetic and clearly marked as test data.

## Learning objectives

- Understand observable behavior associated with keylogger-like activity.
- Build simple endpoint detection logic.
- Collect reproducible forensic artifacts.
- Correlate events into an investigation timeline.
- Test detection logic automatically.
- Document mitigations and limitations.

## Architecture

```text
Synthetic Event Generator
          |
          v
   JSONL Test Telemetry
          |
    +-----+------+
    |            |
    v            v
Process       Detection
Monitor        Engine
    |            |
    +-----+------+
          |
          v
   Forensic Collector
          |
          v
 Investigation Timeline
          |
          v
   Findings + Mitigation
```

## Quick start

### 1. Create a virtual environment

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 3. Run the controlled experiment

```powershell
python -m lab.simulated_input --output data\synthetic_events.jsonl
```

### 4. Run detection

```powershell
python -m detection.detection_rules --input data\synthetic_events.jsonl --output reports\detections.json
```

### 5. Collect process artifacts

```powershell
python -m forensics.collect_artifacts --output artifacts\process_snapshot.json
```

### 6. Build a timeline

```powershell
python -m forensics.timeline --events data\synthetic_events.jsonl --detections reports\detections.json --output reports\timeline.csv
```

### 7. Run tests

```powershell
python -m pytest
```

## Project structure

```text
defensive-keylogger-analysis-lab/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── requirements.txt
├── .gitignore
├── pyproject.toml
├── lab/
│   ├── __init__.py
│   ├── simulated_input.py
│   └── experiment_config.json
├── detection/
│   ├── __init__.py
│   ├── process_monitor.py
│   ├── detection_rules.py
│   └── artifact_scanner.py
├── forensics/
│   ├── __init__.py
│   ├── collect_artifacts.py
│   └── timeline.py
├── mitigation/
│   └── recommendations.md
├── tests/
│   ├── test_detection.py
│   ├── test_monitor.py
│   └── test_forensics.py
├── data/
│   └── .gitkeep
├── artifacts/
│   └── .gitkeep
└── reports/
    ├── .gitkeep
    └── experiment-report.md
```

## Example investigation output

```text
[HIGH] SYNTHETIC_INPUT_ACTIVITY process=lab_simulator.exe evidence=12
```

Every alert contains a rule ID, severity, evidence count, and rationale.

## Limitations

This is an educational lab, not an EDR product. Process inspection is intentionally lightweight and should not be interpreted as comprehensive malware detection.

## Future extensions

1. Windows Event Log integration.
2. Sysmon-based telemetry.
3. YARA artifact scanning.
4. Sigma-style detection rules.
5. ATT&CK technique mapping.
6. Automated HTML investigation reports.
7. Detection benchmarking.
8. Controlled benign-vs-suspicious process comparisons.

## Author

Security research portfolio project — Project 01 of a larger defensive security lab series.
