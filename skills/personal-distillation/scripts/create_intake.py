#!/usr/bin/env python3
"""Capture one raw source in the pending inbox and update current intake state."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from common import frontmatter, load_state, save_state, slugify, today, unique_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--source", required=True, help="Source name, path, conversation, or URL")
    parser.add_argument("--content-file", help="UTF-8 file whose content should be captured")
    parser.add_argument("--external-reference", action="store_true", help="Store only the source reference")
    parser.add_argument("--privacy", choices=("private", "internal", "shareable", "public"), default="private")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    try:
        state = load_state(root)
    except ValueError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 2
    if args.external_reference and args.content_file:
        print(json.dumps({"ok": False, "error": "Use either --content-file or --external-reference"}, ensure_ascii=False))
        return 2
    content = ""
    if args.content_file:
        try:
            content = Path(args.content_file).expanduser().read_text(encoding="utf-8")
        except OSError as exc:
            print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
            return 2
    elif not args.external_reference:
        content = sys.stdin.read()
        if not content.strip():
            print(json.dumps({"ok": False, "error": "Provide stdin, --content-file, or --external-reference"}, ensure_ascii=False))
            return 2
    source_slug = slugify(Path(args.source).stem if "/" in args.source else args.source, "source")
    filename = f"{today().replace('-', '')}_{slugify(args.title)}_{source_slug}.md"
    path = unique_path(root / "10_inbox" / "pending" / filename)
    body = frontmatter(
        title=args.title, module="10_inbox", status="draft", source=args.source,
        evidence="low", stability="unconfirmed", privacy=args.privacy,
        next_action="Classify, distill, update modules, archive intake, and audit",
    )
    body += f"# {args.title}\n\n## Source\n\n- Reference: {args.source}\n- Capture mode: {'external reference only' if args.external_reference else 'content captured'}\n\n## Raw material\n\n"
    body += ("Content remains at the external reference.\n" if args.external_reference else content.rstrip() + "\n")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    state["current_intake"] = {"path": str(path.relative_to(root)), "stage": "captured", "title": args.title}
    state.setdefault("stats", {})["sources"] = state.get("stats", {}).get("sources", 0) + 1
    save_state(root, state)
    print(json.dumps({"ok": True, "path": str(path), "stage": "captured", "next": "classify"}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
