# FocusFrame Flet Experiment Plan

**Status:** Planned / prototype in progress  
**Owner:** FocusFrame project  
**Experiment branch:** `experiment/flet-focusframe`  
**Scope:** Evaluate Flet as an alternative implementation path; do not replace the production JavaScript application during this experiment.

## 1. Decision to make

Should FocusFrame continue with its current JavaScript web foundation and platform adapters, adopt Flet for some or all clients, or retain a hybrid architecture?

The experiment must produce evidence about development effort, behavioral correctness, platform delivery, UX quality, and maintenance cost. Positive reviews and successful demos are reasons to investigate, not evidence for a migration.

## 2. Hypotheses

1. Flet can implement the same core FocusFrame workflow with less cross-platform UI code.
2. The Python session engine can preserve the existing timestamp-authoritative timing semantics.
3. Flet can deliver acceptable web and desktop experiences and can be packaged for at least one mobile target without major platform-specific workarounds.
4. Any development-speed gains will not be outweighed by startup time, application size, runtime constraints, offline limitations, or platform-specific debugging.

Each hypothesis is provisional. Record both supporting and contradictory evidence.

## 3. Scope lock

### In scope

- Create, start, pause, resume, complete, and recover a focus session.
- Timestamp-authoritative countdown and expiry reconciliation.
- Persist session and preference data across reloads/restarts.
- Capture a reflection and export a Markdown session summary.
- Responsive UI, keyboard/accessibility basics, and safe-area behavior.
- Run in a desktop target and a web target; attempt mobile packaging and test on a real device if available.
- Measure build/run workflow, app footprint, startup behavior, and implementation effort.

### Out of scope for this experiment

- Replacing or deleting the current JavaScript app.
- Backend accounts, sync, analytics, subscriptions, or cloud storage.
- App-store submission, production signing credentials, or release automation.
- Adding unrelated FocusFrame features.
- Treating a simulator/demo as proof of real-device background behavior.

## 4. Baseline and fairness rules

Before making a final decision, use the current JavaScript implementation as the control group. Test the same user workflow and scenarios in both implementations on the same hardware, OS/browser versions, network conditions, and test durations wherever possible.

Record:
- Commit SHA and dependency versions for each implementation.
- Time spent implementing, debugging, and packaging.
- Test results and reproducible failure steps.
- Clean-install build instructions, commands, and logs.
- Package size and cold-start time using the same measurement method.
- Any feature intentionally missing from either implementation.

Do not compare a mature implementation against an unfinished prototype without marking the maturity difference. Do not infer performance from subjective impressions alone.

## 5. Phased execution

### Phase 0 — Establish the experiment harness

**Tasks**
- Keep the Flet code isolated under `experiments/flet/`.
- Run Python unit tests and confirm the CI workflow actually executes.
- Verify the documented setup works from a clean checkout.
- Fix API/import/test failures before expanding the prototype.
- Capture the current JavaScript implementation's commit and baseline behavior.

**Exit gate**
- A clean environment can install dependencies, run tests, and launch the Flet app.
- CI has a visible passing run.
- The baseline workflow is written down.

### Phase 1 — Functional parity

Run these scenarios against both implementations:

| ID | Scenario | Expected result |
|---|---|---|
| F1 | Start a valid task | Session enters active state; deadline is recorded |
| F2 | Start with an empty task | User receives a clear validation message; no session starts |
| F3 | Pause, wait, resume | Time spent paused does not consume focus time |
| F4 | Let the timer expire | Session reconciles to completed with zero time remaining |
| F5 | Reload while active | Persisted state is restored and reconciled against the current timestamp |
| F6 | Restart while paused | Paused state and remaining time are restored consistently |
| F7 | Add a reflection | Text survives reload/restart |
| F8 | Export Markdown | Task, planned duration, status, and reflection are present and readable |
| F9 | Enter Markdown special characters | Export remains structurally valid; content is not unintentionally interpreted as formatting |
| F10 | Change duration preference | Preference is retained without corrupting session state |

**Exit gate**
- All critical functional cases pass.
- Any known parity gaps are documented with severity and a proposed resolution.
- No timer correctness issue is waived because it is difficult to reproduce.

### Phase 2 — Lifecycle, storage, and offline reliability

Test in real browsers/devices where possible:
- Background the app, lock the device, resume, and verify the remaining time.
- Suspend the desktop process or browser tab and restore it.
- Reload during active, paused, and completed states.
- Go offline after first launch; test launch and session completion offline.
- Test a fresh install, corrupt/stale persisted data, and application upgrade.
- Confirm session data remains local and is not unexpectedly sent to a server.
- Confirm user-entered reflection content is exported as content, not executable or malformed markup.

**Exit gate**
- No critical data loss, timer drift from wall-clock/deadline semantics, or unsafe persistence behavior.
- Offline behavior is accurately documented per target.
- Any platform-specific limitation has an explicit product decision.

### Phase 3 — Cross-platform packaging

Attempt, in order:
1. Web run/build.
2. Desktop development run and distributable package on one available OS.
3. Android or iOS build; install and test on a physical device if the required SDK/tooling is available.

For each target, record:
- Exact command and toolchain versions.
- Build success/failure and time to first successful build.
- Clean-install launch success.
- Package size and cold-start time.
- Native permission, storage, navigation, and lifecycle issues.
- Amount of platform-specific code or manual configuration required.

**Exit gate**
- At least web and one desktop target work from documented steps.
- At least one mobile target has a documented build attempt; a real-device test is required before claiming mobile lifecycle readiness.
- Packaging friction is compared against the planned JavaScript + Capacitor/Tauri route.

### Phase 4 — UX and engineering-cost comparison

Evaluate both implementations using the same rubric:

| Dimension | Measurement |
|---|---|
| Functional correctness | Critical scenarios passed / total critical scenarios |
| Development effort | Engineering hours by implementation and debugging |
| UI quality | Responsive layout, accessibility, keyboard use, visual consistency |
| Runtime | Cold-start time and interaction responsiveness |
| Distribution | Package size, clean-build reliability, packaging steps |
| Offline/lifecycle | Passed scenarios by platform |
| Maintainability | Number of platform-specific workarounds, dependency surface, testability |
| Developer experience | Setup friction, useful error messages, repeatability |

Use measured values when possible. For subjective UX ratings, write down the rubric before scoring and have the same reviewer evaluate both versions.

### Phase 5 — Decision review

Produce a short report containing:
- Results for every hypothesis.
- Test matrix with pass/fail/blocked and evidence.
- Comparison table for the current JavaScript path and Flet.
- Known limitations and unresolved risks.
- Recommendation: **adopt**, **hybridize**, **continue the current architecture**, or **run a narrowly scoped follow-up**.
- Migration cost and rollback plan if adoption is recommended.

Do not merge a migration into the production architecture solely because the prototype runs. The decision requires critical functional parity, credible platform evidence, and a clear net benefit.

## 6. Decision thresholds

Use these as initial gates; record any agreed changes before reviewing results.

### Adopt Flet for the primary app only if

- All critical functional tests pass.
- No unresolved critical timer, persistence, privacy, or data-loss defects remain.
- Web and desktop packaging are reproducible; mobile feasibility is demonstrated on at least one target and real-device lifecycle behavior is tested before a mobile production commitment.
- The implementation shows a meaningful reduction in total engineering effort or platform duplication.
- Runtime, app size, UI quality, accessibility, and offline behavior meet product requirements.
- The migration and rollback plan is explicit.

### Prefer a hybrid or limited use if

- Flet clearly benefits a specific target or internal tool, but cannot meet one or more cross-platform product requirements consistently.

### Stop the experiment or retain the current architecture if

- Critical timer or persistence semantics cannot be made reliable.
- Platform packaging requires extensive bespoke work that removes the expected leverage.
- Runtime or UX quality falls below acceptable thresholds.
- The measured advantage is marginal relative to migration and maintenance cost.

A failed hypothesis is a useful result if the failure and evidence are recorded.

## 7. Risks and mitigations

- **Prototype bias:** Flet is less mature than the baseline implementation. Use the same parity checklist and mark incomplete work separately from intrinsic framework limitations.
- **API/version drift:** Pin tested dependency versions for the final comparison; do not rely on a floating version range for reproducibility.
- **False offline confidence:** A local web run is not proof of offline-first behavior. Test after a clean install and after network loss on each target.
- **Lifecycle assumptions:** A ticking UI is not a reliable clock. Keep timestamps/deadlines authoritative and reconcile on resume.
- **Storage differences:** Web browser storage and native preferences have different durability, capacity, and isolation characteristics. Verify the actual platform behavior before choosing a production data model.
- **Packaging environment:** SDK or signing credentials may be unavailable. Mark a target as blocked by environment separately from a framework defect.
- **Scope creep:** Do not add features until the parity checklist is complete.

## 8. Experiment log template

For each run, record:

- Date and tester:
- Implementation and commit SHA:
- Target / OS / device / browser:
- Python, Flet, Node, and relevant SDK versions:
- Exact command or test case:
- Expected result:
- Actual result:
- Pass / fail / blocked:
- Duration / package size / startup measurement, if applicable:
- Logs or screenshots:
- Severity and reproducibility:
- Follow-up issue:

## 9. Current status

The repository contains an initial Flet prototype and a separate Python test workflow. The experiment is **not yet validated**. First priorities are to confirm the CI workflow runs, fix any setup/API/test issues, and establish a reproducible baseline before drawing conclusions about Flet's suitability.
