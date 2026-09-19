---
name: jumpguru-measurement
description: Validate JumpGuru IMU timing, jump detection, height estimates and replay experiments. Use for measurement algorithms, calibration or accuracy claims.
---

Read docs/measurement.md and docs/hardware.md before changing measurement behavior.
Define the measurand, coordinate system, units and reference method first.
Preserve raw packets; distinguish sensor time from Android receive time and report unknown timing.
Compare candidate algorithms on the same versioned data and split by participant.
Test gaps, irregular timing, clipping, orientation changes and non-jump movements.
Keep detection validity separate from height validity; never integrate across connection gaps.
Report height error together with event precision/recall and valid-height coverage over all reference jumps.
Synthetic trajectories establish mathematical behavior, not real-world accuracy.
Keep held-out data untouched during tuning. Identify dataset, labels, config and algorithm hashes.
Before claiming accuracy, obtain independent review of reference measurements, exclusions and metrics.
If no hardware/reference data exists, deliver an experiment plan and explicitly mark accuracy unverified.
