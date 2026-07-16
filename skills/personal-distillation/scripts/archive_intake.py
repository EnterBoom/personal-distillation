#!/usr/bin/env python3
"""Move a pending intake to organized or deferred and update workspace state."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from common import KNOWLEDGE_MODULES, load_state, save_state, unique_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--path", help="Pending intake path; defaults to state current_intake")
    parser.add_argument("--destination", choices=("organized", "deferred"), required=True)
    parser.add_argument("--reason", help="Required when destination is deferred")
    parser.add_argument("--updated-file", action="append", default=[], help="Knowledge file updated from this intake; repeat as needed")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    try:
        state = load_state(root)
    except ValueError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 2
    if args.destination == "deferred" and not args.reason:
        print(json.dumps({"ok": False, "error": "--reason is required for deferred intake"}, ensure_ascii=False))
        return 2
    if args.destination == "organized" and not args.updated_file:
        print(json.dumps({"ok": False, "error": "At least one --updated-file is required for organized intake"}, ensure_ascii=False))
        return 2
    validated_updates: list[str] = []
    for relative_update in args.updated_file:
        update = (root / relative_update).resolve()
        try:
            relative_path = update.relative_to(root)
        except ValueError:
            print(json.dumps({"ok": False, "error": f"Updated file is outside workspace: {update}"}, ensure_ascii=False))
            return 2
        if not relative_path.parts or relative_path.parts[0] not in KNOWLEDGE_MODULES or not update.is_file():
            print(json.dumps({"ok": False, "error": f"Updated file must exist in modules 00-09: {relative_update}"}, ensure_ascii=False))
            return 2
        validated_updates.append(str(relative_path))
    relative = args.path or (state.get("current_intake") or {}).get("path")
    if not relative:
        print(json.dumps({"ok": False, "error": "No pending intake specified"}, ensure_ascii=False))
        return 2
    source = (root / relative).resolve()
    pending_root = (root / "10_inbox" / "pending").resolve()
    try:
        source.relative_to(pending_root)
    except ValueError:
        print(json.dumps({"ok": False, "error": "Intake must be inside 10_inbox/pending"}, ensure_ascii=False))
        return 2
    if not source.is_file():
        print(json.dumps({"ok": False, "error": f"Pending intake not found: {source}"}, ensure_ascii=False))
        return 2
    destination = unique_path(root / "10_inbox" / args.destination / source.name)
    if args.reason:
        with source.open("a", encoding="utf-8") as handle:
            handle.write(f"\n## Archive decision\n\n- Destination: {args.destination}\n- Reason: {args.reason}\n")
    destination.parent.mkdir(parents=True, exist_ok=True)
    source.replace(destination)
    state["last_intake"] = {
        "path": str(destination.relative_to(root)),
        "destination": args.destination,
        "reason": args.reason or "module updates and audit completed",
        "updated_files": validated_updates,
    }
    state["current_intake"] = None
    if args.destination == "organized":
        stats = state.setdefault("stats", {})
        stats["organized_sources"] = stats.get("organized_sources", 0) + 1
        onboarding = state.setdefault("onboarding", {})
        if not onboarding.get("completed"):
            onboarding["stage"] = "first_source_organized_audit_pending"
    save_state(root, state)
    print(json.dumps({"ok": True, "from": str(source), "to": str(destination), "destination": args.destination}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
