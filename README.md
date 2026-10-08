# FocusFrame

A calm, local-first, single-purpose focus session tool.

## Architecture

One product core; platform-specific behavior is isolated behind adapters.

- Web/PWA: browser + Service Worker
- Mobile: Capacitor adapter for iOS/Android
- Desktop: Tauri adapter for macOS/Windows
- Persistence: IndexedDB for sessions; localStorage only for small preferences
- Timer: timestamp-based session engine; a worker is optional optimization, never the source of truth
- Export: platform-independent Markdown

## Development

Requires Node 20+.

~~~bash
npm test
npm run check
~~~

Serve the repository with a local HTTP server to exercise Service Worker/PWA behavior.

## Session integrity

Active sessions store `startedAt` and `endAt`. Remaining time is derived from the current timestamp, so suspension, sleep, reload, and app resume do not require a continuously running JavaScript countdown.

FocusFrame is not a tamper-resistant timing system; system clock changes can affect wall-clock calculations.

## Release architecture

The target lifecycle is:

commit → validate → build → sign → verify → stage → approve → distribute → rollback.

Native signing and store credentials stay outside the repository and are supplied through protected CI configuration.

## Scope

No backend, accounts, cloud database, or analytics are required for the initial product.
