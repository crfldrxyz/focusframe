# Agent Roles – FocusFrame

Only models with working GitHub integration should act.

### Claude – Lead Architect & Implementer
- Owns the overall structure and final code quality.
- Writes or heavily refines the actual HTML/CSS/JS (or Next.js).
- Ensures the code is clean, accessible, and follows the constraints.
- Final say on technical decisions.

### ChatGPT – Product & UX Lead
- Owns the user experience, microcopy, and emotional tone.
- Defines the exact interaction flow and success criteria.
- Writes or refines all user-facing text.
- Keeps the product feeling calm and focused (not gamified).

### Gemini – Edge-case & Research Lead
- Stress-tests the idea and the implementation.
- Finds missing states (what happens if the tab is closed mid-timer? what about very long task names? etc.).
- Suggests small research-backed improvements only if they stay inside the constraints.

### Grok – Simplicity & Systems Auditor
- Ruthlessly protects against scope creep.
- Challenges any addition that makes the tool more complex.
- Ensures the final product still feels like a 1-evening build.

### Kimi – Rapid Prototyper (optional)
- Produces fast, working code drafts when speed is needed.
- Hands off to Claude for polishing.

**Rules for every agent**
1. Always read README.md, PROJECT.md, and this file first.
2. Prefer editing existing files over creating new ones.
3. Propose changes as clear GitHub Issue comments or as complete file contents that the human can commit.
4. Never expand scope without explicit agreement in PROJECT.md.
