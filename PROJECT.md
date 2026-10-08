# FocusFrame – Living Project Plan

## Vision

A calm, single-purpose tool that helps someone start and finish one focused work session.

## Architecture baseline

One product core with Browser, Capacitor, and Tauri adapters. Core behavior is shared; operating-system behavior is isolated.

## Success criteria

- Start a session in under 30 seconds.
- Interface feels peaceful, not busy.
- Timer remains correct after backgrounding, sleep, reload, and resume.
- Session data persists locally.
- Session exports as clean Markdown.
- Works offline after first load.
- Looks good on phone and desktop.
- Complexity remains low enough for a non-technical maintainer.

## Current phase

Phase 1 — Core foundation implemented.

## Decisions

- 2026-08-23: Project created as pure frontend.
- 2026-10-08: IndexedDB is the session persistence layer; localStorage is limited to preferences.
- 2026-10-08: Timestamp-based session engine is authoritative; workers are not a reliability guarantee.
- 2026-10-08: Platform-specific behavior must pass through adapters.
- 2026-10-08: Release lifecycle is commit → validate → build → sign → verify → stage → approve → distribute → rollback.

## Next actions

1. Validate core flow on real browsers/devices.
2. Add Capacitor projects and adapters.
3. Add Tauri projects and adapters.
4. Expand CI into platform build/signing pipelines after credentials are configured.
5. Establish release-candidate and rollback procedures.
