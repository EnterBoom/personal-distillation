#!/usr/bin/env python3
"""Audit knowledge metadata, module completeness, evidence gaps, and maturity."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

from common import (
    KNOWLEDGE_MODULES, MODULES, STATUS_SCORE, VALID_EVIDENCE, VALID_PRIVACY,
    VALID_STABILITY, VALID_STATUS, load_state, markdown_body, now_iso, parse_frontmatter, save_state,
)


REQUIRED = (
    "00_control/00_system-guide.md", "00_control/01_module-routing.md",
    "00_control/02_ai-collaboration.md", "01_profile/01_about.md",
    "01_profile/07_not-about.md", "10_inbox/README.md",
    "12_system/CHANGELOG.md", "12_system/TODO.md", "12_system/MISSING.md",
    "12_system/QUESTIONS.md", "12_system/VERSION.md",
)


def module_state(completion: int, counts: Counter) -> str:
    if sum(counts.values()) == 0 or completion == 0:
        return "empty"
    if counts.get("verified", 0) == sum(counts.values()):
        return "verified"
    if completion >= 60 and counts.get("usable", 0) + counts.get("verified", 0) > 0:
        return "usable"
    return "draft"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    try:
        state = load_state(root)
    except ValueError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 2
    gaps: list[dict] = []
    for relative in REQUIRED:
        if not (root / relative).exists():
            gaps.append({"priority": "P1", "path": relative, "issue": "required file missing"})
    modules: dict[str, dict] = {}
    total_docs = 0
    passed_tests: list[str] = []
    for module in KNOWLEDGE_MODULES:
        docs = sorted((root / module).rglob("*.md")) if (root / module).exists() else []
        if module == "00_control":
            docs = [path for path in docs if path.name != "STATUS.md"]
        counts: Counter = Counter()
        evidence: Counter = Counter()
        scores: list[int] = []
        for path in docs:
            total_docs += 1
            meta = parse_frontmatter(path)
            relative = str(path.relative_to(root))
            if not meta:
                gaps.append({"priority": "P1" if module in ("00_control", "01_profile") else "P2", "path": relative, "issue": "missing frontmatter"})
                continue
            status = meta.get("status", "")
            ev = meta.get("evidence_level", "")
            stability = meta.get("stability", "")
            privacy = meta.get("privacy", "")
            if status not in VALID_STATUS:
                gaps.append({"priority": "P1", "path": relative, "issue": f"invalid status: {status}"})
                status = "empty"
            if ev not in VALID_EVIDENCE:
                gaps.append({"priority": "P1", "path": relative, "issue": f"invalid evidence_level: {ev}"})
            if stability not in VALID_STABILITY:
                gaps.append({"priority": "P1", "path": relative, "issue": f"invalid stability: {stability}"})
            if privacy not in VALID_PRIVACY:
                gaps.append({"priority": "P1", "path": relative, "issue": f"invalid privacy: {privacy}"})
            counts[status] += 1
            evidence[ev] += 1
            scores.append(STATUS_SCORE.get(status, 0))
            priority = "P1" if module in ("00_control", "01_profile") else ("P2" if module in ("02_cases", "03_offerings", "05_workflows") else "P3")
            if status == "empty":
                gaps.append({"priority": priority, "path": relative, "issue": "empty document"})
            elif status == "draft":
                gaps.append({"priority": priority, "path": relative, "issue": "draft document"})
            if ev == "low" and status in ("draft", "usable", "verified"):
                gaps.append({"priority": priority, "path": relative, "issue": "low evidence"})
            if not meta.get("next_action"):
                gaps.append({"priority": "P2", "path": relative, "issue": "missing next_action"})
            if module == "09_tests" and path.name != "00_acceptance.md":
                body = markdown_body(path)
                if re.search(r"(?im)^\s*-?\s*result:\s*(pass|passed|通过)\s*$", body):
                    passed_tests.append(relative)
        completion = round(sum(scores) / len(scores)) if scores else 0
        modules[module] = {
            "label": MODULES[module], "state": module_state(completion, counts),
            "completion": completion, "documents": len(docs),
            "status_counts": dict(counts), "evidence_counts": dict(evidence),
        }
    tests_passed = len(passed_tests)
    identity_passed = any(Path(path).name.startswith("01_") for path in passed_tests)
    v1_ready = identity_passed and all(modules[m]["state"] != "empty" for m in ("00_control", "01_profile")) and modules["02_cases"]["state"] in ("usable", "verified")
    v2_ready = v1_ready and all(modules[m]["state"] in ("usable", "verified") for m in ("03_offerings", "04_voice", "05_workflows"))
    v3_ready = v2_ready and all(modules[m]["state"] in ("usable", "verified") for m in ("06_agents", "07_projects", "08_decisions", "09_tests")) and tests_passed >= 8
    maturity = "V3" if v3_ready else ("V2" if v2_ready else ("V1" if v1_ready else "V0"))
    issue_rank = {"required file missing": 0, "missing frontmatter": 1, "empty document": 2, "missing next_action": 3, "draft document": 4, "low evidence": 5}
    gaps.sort(key=lambda item: (item["priority"], issue_rank.get(item["issue"], 1), item["path"], item["issue"]))
    result = {"ok": True, "maturity": maturity, "modules": modules, "gaps": gaps, "tests": {"passed": tests_passed, "passed_files": passed_tests}, "summary": {"documents": total_docs, "gaps": len(gaps)}}
    if args.write:
        status_lines = ["# Knowledge-base status", "", f"- Generated: {now_iso()}", f"- Maturity: {maturity}", f"- Documents scanned: {total_docs}", f"- Open gaps: {len(gaps)}", "", "| Module | State | Completion | Documents | Empty | Draft | Usable | Verified | Low evidence |", "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
        for module, info in modules.items():
            c = info["status_counts"]
            e = info["evidence_counts"]
            status_lines.append(f"| {module} | {info['state']} | {info['completion']}% | {info['documents']} | {c.get('empty', 0)} | {c.get('draft', 0)} | {c.get('usable', 0)} | {c.get('verified', 0)} | {e.get('low', 0)} |")
        next_gap = gaps[0] if gaps else None
        status_lines += ["", "## One next action", "", (f"Resolve {next_gap['priority']} `{next_gap['path']}`: {next_gap['issue']}." if next_gap else "Run an acceptance test and maintain freshness.")]
        (root / "00_control" / "STATUS.md").write_text("\n".join(status_lines) + "\n", encoding="utf-8")
        gap_lines = ["# Missing knowledge", "", f"Generated: {now_iso()}", ""]
        for priority in ("P1", "P2", "P3"):
            gap_lines += [f"## {priority}", ""]
            selected = [g for g in gaps if g["priority"] == priority]
            gap_lines += ([f"- `{g['path']}` - {g['issue']}" for g in selected] or ["- None"])
            gap_lines.append("")
        (root / "12_system" / "MISSING.md").write_text("\n".join(gap_lines), encoding="utf-8")
        state["system_version"] = maturity
        state["module_completion"] = {module: info["completion"] for module, info in modules.items()}
        state.setdefault("stats", {})["tests_passed"] = tests_passed
        state["last_audit"] = {"at": now_iso(), "gaps": len(gaps), "documents": total_docs}
        onboarding = state.setdefault("onboarding", {})
        if onboarding.get("stage") == "first_source_organized_audit_pending":
            onboarding["completed"] = True
            onboarding["stage"] = "completed"
        save_state(root, state)
        result["written"] = [str(root / "00_control" / "STATUS.md"), str(root / "12_system" / "MISSING.md"), str(root / ".distill-state.json")]
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
