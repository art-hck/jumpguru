---
name: jumpguru-delivery
description: Coordinate JumpGuru implementation, independent review and testing across isolated agent worktrees, then produce a reproducible handoff.
---

Read AGENTS.md, docs/agent-workflow.md and the assigned task before dispatch.
Capture base SHA, allowed paths, acceptance criteria and test owner. Use one worktree per writer.
Delegate only independent bounded work; do not assign shared build files to concurrent writers.
For substantial measurement, BLE, storage, build or agent-policy changes, request independent review.
For behavior changes also request independent testing of the same candidate SHA.
Never equate bootstrap CI, emulator tests or synthetic replay with hardware validation.
Do not rerun an expensive suite without a changed hypothesis; stop workers when the owner asks to stop.
Integrate the reviewed change, check the resulting SHA, and report passes, failures and skipped checks separately.
If custom agent roles are unavailable, pass their instructions to ordinary agents; report the limitation.
Keep human approval focused on product decisions and genuinely unauthorized external actions.
Do not publish, upload recordings or send messages to third parties just because a delivery task is complete.
