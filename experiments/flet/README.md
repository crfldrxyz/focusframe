# FocusFrame — Flet experiment

This is an isolated proof of concept for evaluating Flet against the existing JavaScript implementation. It does not replace the production app.

## Run locally

Requires Python 3.10+.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

python -m pip install -e ".[dev]"
flet run main.py
```

To try it in a browser, run `flet run --web main.py`.

## Scope

- Start, pause, resume, and complete a focus session.
- Timestamp-authoritative timing; the displayed countdown is only a view of that state.
- Persist session state and preferences with Flet's `SharedPreferences` client-side service.
- Capture a reflection and prepare/copy a Markdown export.
- Unit tests for session transitions and expiry reconciliation.

## Evaluation boundaries

This prototype proves the basic implementation path, not production readiness. Test offline behavior, background/resume on real devices, platform packaging, accessibility, UI fidelity, and storage isolation before considering a migration. Flet's client storage maps to browser local storage on web and platform-specific preferences on desktop/mobile; it is appropriate for this experiment, but a production data-retention decision must account for those platform differences.

The production JavaScript implementation remains the baseline. No Flet platform build or end-to-end device test is claimed by this repository change.
