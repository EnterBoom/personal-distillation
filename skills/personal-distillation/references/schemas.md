# Artifact schemas

## State

Required `.distill-state.json` fields:

```json
{
  "schema_version": 1,
  "initialized_at": "ISO-8601 timestamp",
  "onboarding_completed": false,
  "mode": "ready_for_first_distillation",
  "profile": {
    "primary_material": "mixed",
    "source_method": "manual input",
    "desired_output": "reusable principles",
    "privacy_boundary": "private raw sources / shareable distilled outputs"
  },
  "current_cycle": null,
  "stats": {
    "distillations": 0,
    "active_experiments": 0,
    "principles": 0,
    "reviews": 0
  }
}
```

Preserve unknown fields for forward compatibility. Reject unsupported future schema versions instead of silently rewriting them.

## IDs and filenames

Use `YYYYMMDD-<short-slug>` for human-created cycle IDs. If a collision exists, append `-2`, `-3`, and so on. Use the same cycle ID across source references, distillations, experiments, and reviews.

## Confidence

Use `low`, `medium`, or `high`, with a one-sentence reason. Confidence describes current support, not importance or writing quality.

## Promotion requirement

A principle must contain:

- claim;
- scope and boundary conditions;
- evidence links;
- known counterexamples;
- confidence and reason;
- created and next-review dates.

