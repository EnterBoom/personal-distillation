#!/usr/bin/env python3
"""Build a purpose-specific AI context pack from governed knowledge documents."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from common import KNOWLEDGE_MODULES, load_state, markdown_body, parse_frontmatter, save_state, today, unique_path


PURPOSES = {
    "control": ("00_control", "01_profile", "06_agents"),
    "full": KNOWLEDGE_MODULES,
    "copy": ("01_profile", "04_voice", "05_workflows", "09_tests"),
    "product": ("01_profile", "02_cases", "03_offerings", "05_workflows", "08_decisions"),
    "sales": ("01_profile", "02_cases", "03_offerings", "04_voice", "05_workflows"),
    "engineering": ("00_control", "05_workflows", "06_agents", "07_projects", "08_decisions"),
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--purpose", choices=tuple(PURPOSES) + ("custom",), required=True)
    parser.add_argument("--modules", help="Comma-separated modules for custom export")
    parser.add_argument("--include-draft", action="store_true")
    parser.add_argument("--include-private", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    try:
        state = load_state(root)
    except ValueError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 2
    if args.purpose == "custom":
        modules = tuple(filter(None, (item.strip() for item in (args.modules or "").split(","))))
        invalid = [module for module in modules if module not in KNOWLEDGE_MODULES]
        if not modules or invalid:
            print(json.dumps({"ok": False, "error": f"Custom export needs valid modules; invalid={invalid}"}, ensure_ascii=False))
            return 2
    else:
        modules = PURPOSES[args.purpose]
    allowed_status = {"usable", "verified"} | ({"draft"} if args.include_draft else set())
    allowed_privacy = {"internal", "shareable", "public"} | ({"private"} if args.include_private else set())
    included: list[tuple[Path, dict[str, str]]] = []
    excluded: list[dict[str, str]] = []
    for module in modules:
        for path in sorted((root / module).rglob("*.md")):
            if path.name == "STATUS.md":
                continue
            meta = parse_frontmatter(path)
            relative = str(path.relative_to(root))
            reason = ""
            if not meta:
                reason = "missing metadata"
            elif meta.get("status") not in allowed_status:
                reason = f"status={meta.get('status')}"
            elif meta.get("privacy") not in allowed_privacy:
                reason = f"privacy={meta.get('privacy')}"
            if reason:
                excluded.append({"path": relative, "reason": reason})
            else:
                included.append((path, meta))
    output = unique_path(root / "11_exports" / f"{today().replace('-', '')}_{args.purpose}-context-pack.md")
    lines = [
        f"# {args.purpose.title()} AI context pack", "",
        f"- Owner: {state.get('profile', {}).get('owner', 'Knowledge owner')}",
        f"- Generated: {today()}", f"- System maturity: {state.get('system_version', 'V0')}",
        f"- Intended use: {args.purpose} tasks", "- Unsuitable use: claims outside included modules or unresolved gaps",
        f"- Included documents: {len(included)}", f"- Excluded documents: {len(excluded)}", "",
        "## Usage constraints", "", "Treat draft, stage-specific, and low-evidence statements as provisional. Preserve privacy and do not infer missing personal facts.", "",
    ]
    current_module = None
    for path, meta in included:
        module = meta.get("module", path.parent.name)
        if module != current_module:
            lines += [f"# Module: {module}", ""]
            current_module = module
        lines += [f"## {meta.get('title', path.stem)}", "", f"Source file: `{path.relative_to(root)}`", f"Status: {meta.get('status')} | Evidence: {meta.get('evidence_level')} | Stability: {meta.get('stability')} | Updated: {meta.get('last_updated')}", "", markdown_body(path), ""]
    lines += ["# Known exclusions and gaps", ""]
    lines += ([f"- `{item['path']}` - {item['reason']}" for item in excluded] or ["- None"])
    output.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    state.setdefault("stats", {})["exports"] = state.get("stats", {}).get("exports", 0) + 1
    save_state(root, state)
    print(json.dumps({"ok": True, "output": str(output), "purpose": args.purpose, "modules": modules, "included": [str(path.relative_to(root)) for path, _ in included], "excluded": excluded}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
