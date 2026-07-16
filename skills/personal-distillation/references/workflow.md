# End-to-end workflow

## Mutation transaction

Every new source follows this order:

1. **Preflight** - Read state, status, missing items, questions, TODOs, and relevant module indexes.
2. **Capture** - Save the source or safe reference in `10_inbox/pending/` with provenance and privacy metadata.
3. **Classify** - Select one primary module and optional secondary modules. Use `deferred` only with a recorded reason.
4. **Distill** - Separate observations, interpretations, judgments, validation needs, and reusable knowledge.
5. **Stability split** - Label extracted items `stable`, `stage`, or `unconfirmed`.
6. **Update** - Modify the smallest set of module documents; preserve conflicting or superseded claims.
7. **Archive intake** - Move the intake to `organized/` after successful updates, otherwise keep it pending. Move low-value or out-of-scope material to `deferred/`.
8. **Record system changes** - Append changelog, questions, TODOs, and version notes when maturity changes.
9. **Audit** - Refresh status and missing reports using `audit_workspace.py --write`.
10. **Report** - Name source, classification, files changed, extracted knowledge, uncertainties, and one next action.

## Epistemic kernel

Within the distillation step, preserve:

```text
source -> observation -> interpretation -> judgment -> validation -> evidence -> reusable knowledge
```

- Observation: directly supported by the source.
- Interpretation: an explicit reading of the observation.
- Judgment: a claim useful for decisions or future work.
- Validation: a falsifiable action, later evidence, independent repeated occurrence, or user confirmation.
- Reusable knowledge: a scoped claim with evidence, boundaries, counterexamples, and retrieval location.

## Failure recovery

- If capture succeeds but later steps fail, keep the intake in `pending/` and record the failure in TODO.
- If a module update succeeds but the audit fails, report partial completion and rerun the audit before continuing other work.
- If classification is ambiguous, record up to three candidates and one clarifying question; do not force a module.
- If new evidence contradicts verified knowledge, preserve both sources, downgrade only with user confirmation, and create a decision or review record.

