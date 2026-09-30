# Legacy Keylogger — Technical Analysis

## Purpose

This document analyzes the original private implementation used during the
development of this defensive security lab.

The public repository contains a **sanitized, non-functional excerpt** rather
than the complete implementation.

## Original implementation

The private implementation used `pynput.keyboard.Listener`.

Its basic behavior was:

1. receive keyboard events through a callback;
2. print the received key representation;
3. attempt to obtain character data from the event;
4. append captured character data to a local file;
5. keep the listener running.

The complete private implementation is intentionally not reproduced in this
public repository.

## Sanitized public code

See:

`analysis/legacy_keylogger_excerpt.py`

Security-sensitive operations have been replaced with `REDACTED` comments.

This allows the project to demonstrate that the technique was understood and
analyzed without publishing a ready-to-run system-wide input-capture program.

## Security-relevant components

### `pynput.keyboard`

The original implementation imported the keyboard listener functionality
from `pynput`.

### Event callback

The callback received keyboard events and converted the event into a
representation that could be printed or processed.

### Character extraction

The original implementation attempted to access the character associated
with the event.

### Local file storage

The original implementation persisted captured input to a file named
`keyfile.txt`.

This creates a useful forensic artifact for a defensive investigation:
a process associated with keyboard-input collection may create or modify a
local file containing captured data.

### Listener lifecycle

The original implementation started a keyboard listener independently of a
dedicated test-input widget.

That is the key architectural difference between the legacy implementation
and the controlled lab application.

## Defensive evidence to investigate

For an authorized investigation, useful evidence can include:

- process name and executable path;
- parent/child process relationships;
- file creation and modification events;
- suspicious files created by the process;
- persistence mechanisms;
- process command-line arguments;
- network activity;
- timestamps correlating process execution with file activity.

## Controlled replacement

The public project uses:

`lab/controlled_input.py`

That application captures real keyboard events only while the user is
interacting with its own text widget.

The controlled implementation:

- requires the user to start recording;
- does not install a system-wide keyboard hook;
- does not capture input from other applications;
- records event metadata rather than the typed character;
- produces JSONL telemetry for the defensive detection pipeline.

## Why the distinction matters

The goal of this project is to demonstrate both sides of a defensive
investigation:

**Technique understanding → observable artifacts → detection → forensics →
mitigation**

The public repository therefore documents the legacy technique while keeping
the executable reproduction constrained to an explicit laboratory application.

## Lessons learned

A keyboard-input collection mechanism should be investigated in context.
The presence of a keyboard-related API alone is not sufficient to determine
malicious intent.

Defenders should correlate:

- process behavior,
- input-capture mechanisms,
- persistence,
- file activity,
- network activity,
- execution context,
- and other endpoint telemetry.

## Scope

All testing in this project is intended for systems and applications owned by
the researcher or explicitly authorized for testing.