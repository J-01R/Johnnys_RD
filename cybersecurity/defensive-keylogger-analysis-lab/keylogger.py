"""
Legacy Keylogger — Sanitized Public Analysis Excerpt
======================================================

Author:
    Jonatan "Johnny" Rassekhnia (@J-01R)

Role:
    Cybersecurity & Information Security Researcher

Project:
    Defensive Keylogger Analysis Lab

Description:
    Documents the structure and behavior of a legacy keyboard-input
    collection implementation without reproducing its security-sensitive
    functionality.

Security Scope:
    This file is intentionally NON-FUNCTIONAL.
    It does not start a keyboard listener, capture system-wide input,
    or persist captured keystrokes.

    Security-sensitive operations from the original private implementation
    have been replaced with REDACTED comments for defensive analysis.

Copyright:
    Copyright (c) 2026 Jonatan "Johnny" Rassekhnia
    All Rights Reserved.

License:
    This project is not released under an open-source license.
    See the repository LICENSE file for usage restrictions.
"""

from pynput import keyboard


def keyPressed(key):
    """Display a sanitized representation of a keyboard event.

    The original implementation performed additional processing of
    keyboard events. Those security-sensitive operations are intentionally
    omitted from this public analysis excerpt.
    """
    print(str(key))

    # REDACTED:
    # Original implementation extracted character data
    # and persisted it to a local file.
    pass


if __name__ == "__main__":
    # REDACTED:
    # Original implementation started a keyboard listener.
    #
    # This public excerpt deliberately does not reproduce that behavior.
    print("Sanitized analysis excerpt — no keyboard listener started.")