# Experiment Report

## Objective

Evaluate whether the lab can generate synthetic keylogger-like telemetry and reliably detect it without collecting real keyboard input.

## Environment

- Windows 11 Pro
- Python 3.11+
- Project version: 0.1.0

## Expected result

The synthetic simulator produces clearly marked events. The detection engine identifies those events and records explainable findings.

## Evidence

After running the experiment, preserve:

- `data/synthetic_events.jsonl`
- `reports/detections.json`
- `artifacts/process_snapshot.json`
- `reports/timeline.csv`

## Interpretation

A detection confirms the defensive pipeline observed expected laboratory behavior. It is not evidence that a real keylogger is installed or active.
