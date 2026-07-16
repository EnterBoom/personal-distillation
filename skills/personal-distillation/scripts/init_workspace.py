#!/usr/bin/env python3
"""Initialize a 13-module personal AI knowledge workspace without overwriting files."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from common import MODULES, frontmatter, now_iso, save_state


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Target workspace root")
    parser.add_argument("--owner", default="Knowledge owner", help="Owner or system name")
    parser.add_argument("--focus", default="mixed personal and professional knowledge")
    parser.add_argument("--source-method", default="manual input")
    parser.add_argument("--outcome", default="reusable knowledge and AI context packs")
    parser.add_argument("--privacy", default="private raw sources / shareable distilled outputs")
    return parser.parse_args()


def write_new(path: Path, content: str, created: list[str], preserved: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        preserved.append(str(path))
        return
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    created.append(str(path))


def seeded_documents(owner: str, privacy: str) -> dict[str, str]:
    private = "private" if "private" in privacy.lower() or "私密" in privacy else "internal"
    docs: dict[str, str] = {
        "00_control/00_system-guide.md": frontmatter(
            title="Knowledge system guide", module="00_control", status="draft",
            source="onboarding profile", evidence="medium", stability="stable", privacy="internal",
            next_action="Confirm owner identity, system goals, and AI use rules",
        ) + f"# {owner} knowledge system\n\n## Purpose\n\nMaintain traceable, testable, retrievable knowledge for people and AI agents.\n\n## Operating loop\n\n`capture -> classify -> distill -> update -> audit -> export -> test`\n",
        "00_control/01_module-routing.md": frontmatter(
            title="Module routing rules", module="00_control", status="usable",
            source="personal-distillation v2 architecture", evidence="high", stability="stable", privacy="internal",
            next_action="Test routing with the first three real sources",
        ) + "# Module routing\n\nUse one primary module and optional secondary links. See `WORKFLOW.md` for the module map.\n",
        "00_control/02_ai-collaboration.md": frontmatter(
            title="AI collaboration rules", module="00_control", status="draft",
            source="onboarding profile", evidence="low", stability="unconfirmed", privacy="internal",
            next_action="Collect preferred AI behavior and explicit prohibitions",
        ) + "# AI collaboration\n\n## The AI should\n\n- Preserve sources and uncertainty.\n- Update artifacts, status, gaps, and changelog together.\n\n## The AI must not\n\n- Invent personal facts, evidence, or confirmation.\n",
        "01_profile/01_about.md": frontmatter(
            title=f"About {owner}", module="01_profile", status="empty",
            source="awaiting owner input", evidence="low", stability="unconfirmed", privacy=private,
            next_action="Add a user-confirmed one-line identity and current focus",
        ) + f"# About {owner}\n\n## One-line identity\n\n## Current focus\n\n## Long-term direction\n",
        "01_profile/07_not-about.md": frontmatter(
            title=f"What {owner} is not", module="01_profile", status="empty",
            source="awaiting owner input", evidence="low", stability="unconfirmed", privacy=private,
            next_action="Add user-confirmed negative positioning and boundaries",
        ) + f"# What {owner} is not\n\n## Misclassifications to avoid\n\n## Work or positioning boundaries\n",
        "02_cases/00_index.md": frontmatter(title="Case index", module="02_cases") + "# Case index\n\nNo evidence-backed cases yet.\n",
        "03_offerings/00_overview.md": frontmatter(title="Offering overview", module="03_offerings") + "# Offering overview\n\nNo products or services documented yet.\n",
        "04_voice/00_principles.md": frontmatter(title="Voice principles", module="04_voice") + "# Voice principles\n\nNo confirmed style rules yet. Add positive and negative samples.\n",
        "05_workflows/00_overview.md": frontmatter(title="Workflow overview", module="05_workflows") + "# Workflow overview\n\nNo reusable SOPs documented yet.\n",
        "06_agents/00_architecture.md": frontmatter(title="Agent architecture", module="06_agents") + "# Agent architecture\n\nNo agent contracts documented yet.\n",
        "07_projects/00_index.md": frontmatter(title="Project index", module="07_projects") + "# Project index\n\nNo projects documented yet.\n",
        "08_decisions/00_index.md": frontmatter(title="Decision index", module="08_decisions") + "# Decision index\n\nNo decisions documented yet.\n",
        "09_tests/00_acceptance.md": frontmatter(
            title="Acceptance overview", module="09_tests", status="draft",
            source="personal-distillation v2 acceptance model", evidence="high", stability="stable", privacy="internal",
            next_action="Execute tests after profile and one case become usable",
        ) + "# Acceptance overview\n\nV1 requires accurate identity understanding and at least one evidence-backed case. V3 requires at least 8 of 10 test domains to pass.\n",
        "10_inbox/README.md": "# Raw-material inbox\n\n- `pending/`: captured, not fully integrated.\n- `organized/`: module updates and audit completed.\n- `deferred/`: duplicate, out of scope, low value, or awaiting a prerequisite.\n\nName sources `YYYYMMDD_topic_source.md`. Preserve provenance and privacy.\n",
        "11_exports/README.md": "# AI context exports\n\nGenerated purpose-specific context packs live here. Exports should state intended use, unsuitable use, freshness, exclusions, and unresolved gaps.\n",
        "12_system/CHANGELOG.md": "# Changelog\n\n## Workspace initialized\n- Created the personal-distillation v2 structure.\n",
        "12_system/TODO.md": "# TODO\n\n- [ ] Complete the onboarding profile.\n- [ ] Process the first real source.\n- [ ] Run the first knowledge audit.\n",
        "12_system/MISSING.md": "# Missing knowledge\n\nRun `audit_workspace.py --write` to generate the first gap report.\n",
        "12_system/QUESTIONS.md": "# Questions awaiting owner confirmation\n\n- What one-line identity should the system use?\n- What must other AI agents never assume about the owner?\n",
        "12_system/VERSION.md": "# Version record\n\n## V0 - initialized\n- Structure and system records created.\n- Knowledge content and acceptance tests remain incomplete.\n",
    }
    test_names = (
        "identity-understanding", "case-evidence", "offering-understanding", "voice-style",
        "content-task", "workflow-execution", "agent-routing", "project-requirements",
        "decision-consistency", "knowledge-update",
    )
    for index, name in enumerate(test_names, 1):
        docs[f"09_tests/{index:02d}_{name}.md"] = frontmatter(
            title=name.replace("-", " ").title(), module="09_tests", status="empty",
            source="acceptance framework", evidence="low", stability="unconfirmed", privacy="internal",
            next_action="Define instruction, expected output, and pass criteria",
        ) + f"# {name.replace('-', ' ').title()}\n\n## Test instruction\n\n## Expected output\n\n## Pass criteria\n\n## Common failures\n\n## Latest result\n\n- Result: not run\n- Evidence:\n- Tested at:\n"
    return docs


def workflow_text(owner: str) -> str:
    module_lines = "\n".join(f"- `{name}`: {label}" for name, label in MODULES.items())
    return f"""# {owner} personal knowledge workflow

## Operating loop

`capture -> classify -> distill -> update -> audit -> export -> test`

## Modules

{module_lines}

## Everyday phrases

- `整理新素材`
- `继续整理`
- `完善模块`
- `检查缺口`
- `导出投喂包`
- `测试知识库`

## Integrity rule

Keep status, evidence, stability, and privacy independent. Do not promote knowledge to `verified` without explicit owner confirmation.
"""


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    created: list[str] = []
    preserved: list[str] = []
    updated: list[str] = []
    root.mkdir(parents=True, exist_ok=True)

    state_path = root / ".distill-state.json"
    existing: dict | None = None
    if state_path.exists():
        try:
            existing = json.loads(state_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(json.dumps({"ok": False, "error": f"Invalid existing state: {exc}"}, ensure_ascii=False))
            return 2
        version = existing.get("schema_version")
        if version == 1:
            print(json.dumps({"ok": False, "error": "Schema v1 requires migrate_workspace.py first"}, ensure_ascii=False))
            return 3
        if version != 2:
            print(json.dumps({"ok": False, "error": f"Unsupported schema_version: {version}"}, ensure_ascii=False))
            return 2

    for module in MODULES:
        path = root / module
        if path.exists():
            preserved.append(str(path))
        else:
            path.mkdir(parents=True)
            created.append(str(path))
    for child in ("pending", "organized", "deferred"):
        path = root / "10_inbox" / child
        if path.exists():
            preserved.append(str(path))
        else:
            path.mkdir()
            created.append(str(path))

    for relative, content in seeded_documents(args.owner, args.privacy).items():
        write_new(root / relative, content, created, preserved)
    write_new(root / "WORKFLOW.md", workflow_text(args.owner), created, preserved)

    template_source = Path(__file__).resolve().parent.parent / "assets" / "workspace-template" / "templates"
    target_templates = root / "templates"
    target_templates.mkdir(exist_ok=True)
    for source in sorted(template_source.glob("*.md")):
        destination = target_templates / source.name
        if destination.exists():
            preserved.append(str(destination))
        else:
            shutil.copy2(source, destination)
            created.append(str(destination))

    if existing is None:
        state = {
            "schema_version": 2,
            "system_version": "V0",
            "initialized_at": now_iso(),
            "updated_at": now_iso(),
            "profile": {
                "owner": args.owner,
                "focus": args.focus,
                "source_method": args.source_method,
                "desired_output": args.outcome,
                "privacy_boundary": args.privacy,
            },
            "onboarding": {"completed": False, "stage": "workspace_initialized"},
            "current_intake": None,
            "module_completion": {module: 0 for module in list(MODULES)[:10]},
            "stats": {"sources": 0, "organized_sources": 0, "exports": 0, "tests_passed": 0},
            "last_audit": None,
        }
        save_state(root, state)
        created.append(str(state_path))
    else:
        changed = False
        onboarding = existing.setdefault("onboarding", {})
        if onboarding.get("stage") == "migration_requires_v2_initialization":
            onboarding["stage"] = "workspace_initialized"
            changed = True
        profile = existing.setdefault("profile", {})
        if profile.get("owner") in (None, "", "Knowledge owner") and args.owner != "Knowledge owner":
            profile["owner"] = args.owner
            changed = True
        if changed:
            save_state(root, existing)
            updated.append(str(state_path))
        else:
            preserved.append(str(state_path))

    print(json.dumps({"ok": True, "schema_version": 2, "root": str(root), "created": created, "updated": updated, "preserved": preserved}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
