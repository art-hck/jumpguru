#!/usr/bin/env python3
"""Report available tools without installing or changing machine configuration."""
import shutil
import sys

missing = []
for tool in ("git", "python3", "java", "javac", "adb", "sdkmanager"):
    path = shutil.which(tool)
    print(f"{tool}: {path or 'MISSING'}")
    if not path:
        missing.append(tool)
print("Gradle: use the checked-in wrapper once JG-001 adds it.")
print("This checks PATH only, not version compatibility, device access or BLE.")
sys.exit(1 if missing else 0)
