#!/usr/bin/env python3
"""Initialize a personal-distillation workspace without overwriting user files."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


DIRECTORIES = ("inbox", "distillations", "principles", "experiments", "reviews", "templates")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Target workspace root")
    parser.add_argument("--focus", default="mixed", help="Primary material type")
    parser.add_argument("--source-method", default="manual input", help="How sources are provided")
    parser.add_argument("--outcome", default="reusable principles", help="Desired output")
    parser.add_argument(
        "--privacy",
        default="private raw sources / shareable distilled outputs",
        help="Privacy boundary",
    )
    return parser.parse_args()


def write_new(path: Path, content: str, created: list[str], preserved: list[str]) -> None:
    if path.exists():
        preserved.append(str(path))
        return
    path.write_text(content, encoding="utf-8")
    created.append(str(path))


def workflow_text() -> str:
    return """# Personal Distillation Workflow

## The loop

```text
capture -> extract -> synthesize -> validate -> consolidate
```

1. Put or reference bounded raw material in `inbox/`.
2. Separate observations from interpretations in `distillations/`.
3. State one provisional judgment and its uncertainty.
4. Define an observable validation action in `experiments/`.
5. Record evidence in `reviews/`; retain, revise, reject, or promote.
6. Put supported reusable knowledge in `principles/`.

## Everyday phrases

- `开始蒸馏`: process a new source.
- `继续蒸馏`: resume the current cycle.
- `验证这条判断`: define or update a validation action.
- `复盘`: record evidence and update the judgment.
- `状态`: show progress and one next action.
- `使用说明`: explain this workflow again.

## Evidence rule

Keep source, observation, interpretation, judgment, experiment, evidence, and principle distinct. A polished judgment is not a validated principle.
"""


def status_text() -> str:
    return """# Personal Distillation Status

- Mode: ready for first distillation
- Onboarding: workspace initialized; first cycle pending
- Distillations: 0
- Active experiments: 0
- Principles: 0
- Reviews: 0

## Next action

Provide one bounded note, experience, decision, project episode, or excerpt and say `开始蒸馏`.
"""


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    created: list[str] = []
    preserved: list[str] = []

    root.mkdir(parents=True, exist_ok=True)
    for directory in DIRECTORIES:
        path = root / directory
        if path.exists():
            preserved.append(str(path))
        else:
            path.mkdir()
            created.append(str(path))

    state_path = root / ".distill-state.json"
    if state_path.exists():
        try:
            existing = json.loads(state_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(json.dumps({"ok": False, "error": f"Invalid existing state: {exc}"}, ensure_ascii=False))
            return 2
        version = existing.get("schema_version")
        if version != 1:
            print(json.dumps({"ok": False, "error": f"Unsupported existing schema_version: {version}"}, ensure_ascii=False))
            return 2
        preserved.append(str(state_path))
    else:
        state = {
            "schema_version": 1,
            "initialized_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
            "onboarding_completed": False,
            "mode": "ready_for_first_distillation",
            "profile": {
                "primary_material": args.focus,
                "source_method": args.source_method,
                "desired_output": args.outcome,
                "privacy_boundary": args.privacy,
            },
            "current_cycle": None,
            "stats": {
                "distillations": 0,
                "active_experiments": 0,
                "principles": 0,
                "reviews": 0,
            },
        }
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        created.append(str(state_path))

    write_new(root / "WORKFLOW.md", workflow_text(), created, preserved)
    write_new(root / "STATUS.md", status_text(), created, preserved)

    template_source = Path(__file__).resolve().parent.parent / "assets" / "workspace-template" / "templates"
    for source in sorted(template_source.glob("*.md")):
        destination = root / "templates" / source.name
        if destination.exists():
            preserved.append(str(destination))
        else:
            shutil.copy2(source, destination)
            created.append(str(destination))

    print(
        json.dumps(
            {"ok": True, "root": str(root), "created": created, "preserved": preserved},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
