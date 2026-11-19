#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Test the imports that might be failing
try:
    from core.config import get_config
    print("✓ Config imported successfully")
except Exception as e:
    print(f"✗ Failed to import config: {e}")

try:
    from core.actions.close import Closer
    print("✓ Closer imported successfully")
except Exception as e:
    print(f"✗ Failed to import Closer: {e}")

# Now test the exact code that's failing in close.py
try:
    from voice_commander.core.config import get_config
    print("✓ Direct import of config works")
    result = get_config('confirmations', True)
    print(f"✓ Config value retrieved: {result}")
except Exception as e:
    print(f"✗ Failed to get config directly: {e}")