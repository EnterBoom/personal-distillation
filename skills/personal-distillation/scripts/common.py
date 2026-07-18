#!/usr/bin/env python3
"""Shared constants and helpers for the personal-distillation skill."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path


MODULES = {
    "00_control": "Control and routing",
    "01_profile": "Owner profile",
    "02_cases": "Cases and evidence",
    "03_offerings": "Products and services",
    "04_voice": "Voice and style",
    "05_workflows": "Workflows and SOPs",
    "06_agents": "Agent collaboration",
    "07_projects": "Project knowledge",
    "08_decisions": "Decision history",
    "09_tests": "Acceptance tests",
    "10_inbox": "Raw-material inbox",
    "11_exports": "AI context exports",
    "12_system": "System records",
}

KNOWLEDGE_MODULES = tuple(list(MODULES)[:10])
VALID_STATUS = ("empty", "draft", "usable", "verified")
VALID_EVIDENCE = ("low", "medium", "high")
VALID_STABILITY = ("stable", "stage", "unconfirmed")
VALID_PRIVACY = ("private", "internal", "shareable", "public")
STATUS_SCORE = {"empty": 0, "draft": 35, "usable": 75, "verified": 100}


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def today() -> str:
    return datetime.now().astimezone().date().isoformat()


def load_state(root: Path, supported: int = 2) -> dict:
    path = root / ".distill-state.json"
    if not path.exists():
        raise ValueError(f"Missing state file: {path}")
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Invalid state file: {exc}") from exc
    version = state.get("schema_version")
    if version != supported:
        raise ValueError(f"Unsupported schema_version {version}; expected {supported}")
    return state


def save_state(root: Path, state: dict) -> None:
    state["updated_at"] = now_iso()
    (root / ".distill-state.json").write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def yaml_string(value: str) -> str:
    return json.dumps(str(value), ensure_ascii=False)


def frontmatter(
    *,
    title: str,
    module: str,
    status: str = "empty",
    source: str = "workspace initialization",
    evidence: str = "low",
    stability: str = "unconfirmed",
    privacy: str = "private",
    next_action: str = "Add source-backed content",
) -> str:
    return "\n".join(
        [
            "---",
            f"title: {yaml_string(title)}",
            f"module: {module}",
            f"status: {status}",
            f"last_updated: {today()}",
            f"source: {yaml_string(source)}",
            f"evidence_level: {evidence}",
            f"stability: {stability}",
            f"privacy: {privacy}",
            f"next_action: {yaml_string(next_action)}",
            "---",
            "",
        ]
    )


def parse_frontmatter(path: Path) -> dict[str, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    values: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return values
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        raw = value.strip()
        if raw.startswith('"') and raw.endswith('"'):
            try:
                raw = json.loads(raw)
            except json.JSONDecodeError:
                raw = raw[1:-1]
        values[key.strip()] = str(raw)
    return {}


def markdown_body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return text.strip()
    parts = text.split("---", 2)
    return parts[2].strip() if len(parts) == 3 else text.strip()


def slugify(value: str, fallback: str = "material") -> str:
    slug = re.sub(r"[^\w\u4e00-\u9fff]+", "-", value.strip().lower(), flags=re.UNICODE)
    slug = slug.strip("-_")
    return slug[:60] or fallback


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    for number in range(2, 1000):
        candidate = path.with_name(f"{path.stem}-{number}{path.suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Unable to find a unique path near {path}")
