# Knowledge governance

## Required frontmatter

Every maintained knowledge document in modules `00` through `09` uses:

```yaml
---
title: Document title
module: 01_profile
status: empty
last_updated: YYYY-MM-DD
source: user statement, file path, or source IDs
evidence_level: low
stability: unconfirmed
privacy: private
next_action: What must happen next
---
```

Allowed values:

- `status`: `empty`, `draft`, `usable`, `verified`;
- `evidence_level`: `low`, `medium`, `high`;
- `stability`: `stable`, `stage`, `unconfirmed`;
- `privacy`: `private`, `internal`, `shareable`, `public`.

## Keep dimensions independent

- `status` measures usability and completeness.
- `evidence_level` measures support.
- `stability` measures expected change over time.
- `privacy` controls exposure.

A document may be usable but stage-specific, high-evidence but private, or well-structured but still unconfirmed.

## Status transitions

- `empty -> draft`: at least one source-backed item exists.
- `draft -> usable`: required structure is filled enough for an AI task, limitations are explicit, and source links exist.
- `usable -> verified`: the user explicitly confirms the document as durable knowledge.
- Downgrade when contradictory evidence materially affects use; preserve the reason in changelog.

## Evidence levels

- `high`: explicit source file, direct quote, project result/data, or user confirmation.
- `medium`: repeated independent occurrences with incomplete primary evidence.
- `low`: inference, single ambiguous mention, or incomplete context.

Never increase evidence because prose became more polished.

## Stability

- `stable`: expected to remain valid for 6-12 months or more.
- `stage`: current project, strategy, preference, or temporary constraint.
- `unconfirmed`: plausible but requires clarification or evidence.

Put stage-specific strategy in projects or decisions rather than rewriting durable profile claims.

## Change records

Append one changelog entry for each transaction:

```markdown
## YYYY-MM-DD HH:MM - <source ID>
- Classification:
- Files changed:
- Knowledge added or revised:
- Status/evidence changes:
- Questions created:
- Next action:
```
