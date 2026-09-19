---
name: jumpguru-ui-ux
description: Design and review JumpGuru native Android screens, visual tokens, workout flows, accessible interactions and honest measurement statistics. Use for UI and UX work, not BLE protocol or estimator implementation.
---

Read docs/ui-ux.md from the repository root. Preserve the current task scope.

For new product screens, define the user's action and loading, empty, error and partial-data states first.
For initial visual direction, show two coherent concepts on the same key screens; do not pick a permanent brand palette from a generic generator result.
Use Material 3 and shared color, type, spacing, shape and icon tokens. Support Cyrillic and light/dark themes.
Keep recording status and the main action obvious, with one-handed use during sport in mind.
Never imply a healthy recording when storage or connection has failed. Expose gaps and invalid-height counts next to results.
Separate detected jumps from usable heights. Do not display unknown height as zero or connect chart lines across missing data.
Use native Android dp/sp, at least 48 dp touch targets, accessible semantics and labels; never import CSS, hover-only interactions or browser libraries into the app.
Verify font scales 1.0/1.5/2.0, TalkBack, compact windows, system insets, themes and interrupted recordings.
Read the adaptive skill for window/layout changes and edge-to-edge for system bars/IME. Apply only relevant stable APIs; do not broaden MVP devices or change the toolchain to satisfy a sample.
Before implementing main screens, present visual concepts. During implementation, inspect actual renders and have an independent reviewer inspect screenshot diffs before the agent updates baselines.
Provide the owner with visible results and simple usability steps, not code-editing or testing chores.
Record what was visually inspected versus what still needs a real phone. Never claim a docs-only change is validated UI.
