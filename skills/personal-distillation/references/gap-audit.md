# Status and gap audit

## Run the deterministic scan

```bash
python3 <skill-dir>/scripts/audit_workspace.py --root <workspace> --write
```

Review its JSON output before summarizing.

## Scan priorities

1. Missing required control and system files.
2. Documents with missing or invalid metadata.
3. `empty` modules and documents.
4. `draft` documents blocking current goals.
5. `low` evidence and `unconfirmed` claims used by exports.
6. Unfinished `next_action` items.
7. Modules without usable acceptance tests.
8. Pending sources that have become stale.

## Gap levels

- P1: blocks identity accuracy, privacy, routing, or current user goal.
- P2: blocks products, repeatable work, commercial use, or exports.
- P3: improves coverage, style fidelity, or later automation.

Recommend exactly one next action using this priority order. Do not rank by easiest file to fill.

## Completion is evidence-based

Completion percentages are navigation aids, not truth. A module with many draft files is not more mature than one concise verified file. Always show state distribution and evidence warnings beside percentages.
