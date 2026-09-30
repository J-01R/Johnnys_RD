# Mitigation Analysis

## Endpoint

- Keep Microsoft Defender protections enabled.
- Apply Windows security updates promptly.
- Review unexpected processes and unsigned executables.
- Restrict unnecessary software execution where appropriate.
- Use application control in managed environments.

## Detection

Monitor for combinations of:

- unusual input-related behavior
- unexpected process ancestry
- suspicious executable locations
- anomalous persistence
- unusual outbound network activity

A single indicator should generally be treated as context, not automatic proof of malicious activity.

## Investigation

1. Record timestamps and affected process information.
2. Preserve relevant logs and hashes.
3. Establish process lineage.
4. Determine whether the executable is expected.
5. Correlate endpoint and network telemetry.
6. Contain the endpoint if evidence warrants it.
7. Document the conclusion and evidence.

## Lab-specific limitation

The simulator deliberately produces synthetic events. A detection hit demonstrates that the defensive pipeline observed expected laboratory behavior; it does not establish that a real keylogger exists or is active.
