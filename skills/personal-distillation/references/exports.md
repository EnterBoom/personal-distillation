# AI context exports

## Export types

- `control`: identity, current focus, collaboration rules, module routing.
- `full`: all usable and verified knowledge, grouped by module.
- `copy`: profile, voice, relevant SOPs, positive/negative examples, QA.
- `product`: profile, offerings, product-design SOPs, delivery boundaries, decisions.
- `sales`: profile, offerings, cases, sales workflows, relevant style and objections.
- `engineering`: collaboration rules, agent contracts, engineering workflows, project constraints.
- `custom`: only user-selected modules and documents.

## Rules

- Default to `usable` and `verified` documents.
- Exclude private material unless the user explicitly authorizes the target context.
- Label draft, stage-specific, and unconfirmed information when explicitly included.
- Keep source references and update dates.
- State intended use, unsuitable use, missing knowledge, and freshness.
- Prefer a small relevant pack over an overloaded complete dump.

Run:

```bash
python3 <skill-dir>/scripts/build_export.py \
  --root <workspace> \
  --purpose <control|full|copy|product|sales|engineering|custom> \
  [--modules 01_profile,04_voice] \
  [--include-draft]
```

Review the file list and exclusions in the JSON result.
