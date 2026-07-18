#!/usr/bin/env python3
"""Migrate a personal-distillation schema-v1 state file to schema v2 safely."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from common import KNOWLEDGE_MODULES, now_iso


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    path = root / ".distill-state.json"
    backup = root / ".distill-state.v1.backup.json"
    try:
        old = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 2
    if old.get("schema_version") == 2:
        print(json.dumps({"ok": True, "migrated": False, "reason": "already schema v2"}, ensure_ascii=False))
        return 0
    if old.get("schema_version") != 1:
        print(json.dumps({"ok": False, "error": f"Unsupported schema_version: {old.get('schema_version')}"}, ensure_ascii=False))
        return 2
    if backup.exists():
        print(json.dumps({"ok": False, "error": f"Backup already exists: {backup}"}, ensure_ascii=False))
        return 3
    backup.write_text(json.dumps(old, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    profile = old.get("profile", {})
    new = {
        "schema_version": 2,
        "system_version": "V0",
        "initialized_at": old.get("initialized_at", now_iso()),
        "updated_at": now_iso(),
        "profile": {
            "owner": profile.get("owner", "Knowledge owner"),
            "focus": profile.get("primary_material", "mixed personal and professional knowledge"),
            "source_method": profile.get("source_method", "manual input"),
            "desired_output": profile.get("desired_output", "reusable knowledge and AI context packs"),
            "privacy_boundary": profile.get("privacy_boundary", "private raw sources / shareable distilled outputs"),
        },
        "onboarding": {"completed": False, "stage": "migration_requires_v2_initialization"},
        "current_intake": old.get("current_cycle"),
        "module_completion": {module: 0 for module in KNOWLEDGE_MODULES},
        "stats": {"sources": 0, "organized_sources": 0, "exports": 0, "tests_passed": 0},
        "last_audit": None,
        "migration": {"from_schema": 1, "at": now_iso(), "legacy_stats": old.get("stats", {})},
    }
    path.write_text(json.dumps(new, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "migrated": True, "backup": str(backup), "next": "Run init_workspace.py to add v2 structure"}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
