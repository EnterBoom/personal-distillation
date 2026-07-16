# New-material ingestion

## Preflight

Read:

- `.distill-state.json`;
- `00_control/STATUS.md`;
- `12_system/MISSING.md`;
- `12_system/TODO.md`;
- `12_system/QUESTIONS.md`;
- relevant module indexes.

## Capture

Use `create_intake.py` when material is supplied as text or a local file. Preserve provenance, date, privacy, and completeness. Never copy a secret or sensitive source into a public workspace; store a safe external reference instead.

Intake lifecycle:

- `pending`: captured but not fully integrated;
- `organized`: knowledge updates and system audit completed;
- `deferred`: out of scope, low value, duplicate, or awaiting a prerequisite; record the reason.

## Classify

Select categories from:

```text
A profile       B case/evidence    C offering
D voice/style   E workflow/SOP     F agent rule
G project       H decision         I test/acceptance
J ambiguous/deferred
```

Use [architecture.md](architecture.md) for module mapping.

## Distill

Extract three stability groups:

- stable: likely durable for 6-12 months;
- stage: current project, strategy, or temporary preference;
- unconfirmed: inference or ambiguity requiring a question.

Within each group, keep observations separate from interpretations and judgments. Attach source IDs.

## Update

Update the smallest relevant documents. Merge duplicate claims, preserve contradictions, and never replace a confirmed durable claim with a stage-specific statement.

After updates:

1. set accurate metadata;
2. append changelog;
3. add unresolved questions and TODOs;
4. archive the intake only after successful module updates using `archive_intake.py --updated-file <path>` for every changed knowledge document;
5. run the audit with `--write`;
6. output the ingestion report.

## Ingestion report

```markdown
# Material ingestion report
## Source captured
## Classification and rationale
## Stable knowledge
## Stage-specific knowledge
## Unconfirmed knowledge
## Files changed
## Gaps and questions
## One next action
```
