---
name: jumpguru-android-ble
description: Implement or review continuous WT9011DCL acquisition in the JumpGuru Android app, including BLE protocol, foreground recording, loss tracking and raw export.
---

Read docs/hardware.md and docs/architecture.md. The sensor has no recording memory.
Verify actual model/firmware, GATT characteristics and payload format from vendor sources and real captures.
Do not substitute a similar WIT UART or BLE model protocol. Do not invent packet checksums or timestamps.
Keep raw bytes and monotonic receive times before decoding; preserve connection epochs and observed gaps.
Serialize GATT operations and define bounded retry/reconnect and shutdown behavior.
Keep the callback free of disk I/O; record queue overflow explicitly. UI throttling must not throttle recording.
Start recording from a user action and use current Android connectedDevice foreground-service requirements.
Check permissions against target/runtime Android; request only those required by actual operations.
Use fakes for transport tests, captured packets for decoder tests, and a real phone/sensor for radio acceptance.
Test screen-off, Bluetooth disabled, reconnect, storage exhaustion and interrupted-session recovery.
No estimator may bridge missing data. App must show incomplete recording and retain recoverable data.
Document manual steps for the owner; do not require them to edit code or interpret raw logs.
