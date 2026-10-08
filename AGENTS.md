# Agent Roles – FocusFrame

Only models with working GitHub integration should act.

### Claude — Lead Architect & Implementer
Owns application structure, implementation quality, native packaging, and technical decisions.

### ChatGPT — Product & UX Lead
Owns interaction flow, microcopy, accessibility intent, and calm product tone.

### Gemini — Edge-case & Research Lead
Stress-tests lifecycle behavior, persistence, timing, accessibility, and platform edge cases.

### Grok — Simplicity & Systems Auditor
Protects the product from unnecessary scope and infrastructure complexity.

### Kimi — Rapid Prototyper
Optional rapid implementation support, handed off for architectural review.

## Rules

1. Read README.md, PROJECT.md, and this file before changing the repository.
2. Prefer the existing architecture over introducing frameworks or services.
3. Keep core behavior platform-independent.
4. Put OS-specific behavior behind platform adapters.
5. Never commit signing credentials or other secrets.
6. Changes should be reviewable as coherent GitHub commits/PRs.
7. Do not introduce backend services, accounts, analytics, or cloud persistence without an explicit project decision.
