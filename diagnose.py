#!/usr/bin/env python
"""Detailed diagnostic for blueprint registration."""

import sys

print("Step 1: Import routes modules...")
try:
    from app.routes import batiments, api, stats
    print(f"  ✓ batiments.bp = {batiments.bp}")
    print(f"  ✓ api.bp = {api.bp}")
    print(f"  ✓ stats.bp = {stats.bp}")
except Exception as e:
    print(f"  ✗ Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nStep 2: Create app...")
try:
    from app import create_app
    app = create_app()
    print(f"  ✓ App created: {app}")
except Exception as e:
    print(f"  ✗ Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nStep 3: Check registered blueprints...")
try:
    blueprints = app.blueprints
    print(f"  Registered blueprints: {list(blueprints.keys())}")
    for name, bp in blueprints.items():
        print(f"    - {name}: {bp}")
except Exception as e:
    print(f"  ✗ Failed: {e}")
    sys.exit(1)

print("\nStep 4: Check URL rules...")
try:
    for rule in app.url_map.iter_rules():
        print(f"  {rule.rule} ({rule.methods - {'HEAD', 'OPTIONS'}})")
except Exception as e:
    print(f"  ✗ Failed: {e}")
    sys.exit(1)

print("\n✅ Diagnostic complete")
