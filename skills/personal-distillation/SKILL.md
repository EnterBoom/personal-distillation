---
name: personal-distillation
description: Build and operate a stateful personal-distillation workflow that turns raw notes, experiences, decisions, project material, or reading highlights into explicit judgments, testable hypotheses, and reusable principles. Use when a user asks to initialize or deploy a personal knowledge-distillation workspace, process new source material, continue an unfinished distillation, validate or review a judgment, promote a validated insight into a principle, inspect workflow status, or learn how the personal-distillation system works. Trigger on phrases such as "个人蒸馏", "开始蒸馏", "继续蒸馏", "初始化蒸馏工作区", "验证这条判断", "复盘", "状态", or "使用说明".
---

# Personal Distillation

Turn lived evidence and source material into knowledge that remains traceable, testable, and reusable.

## Route the request

1. Resolve the target workspace from an explicit user path, otherwise use the current workspace root.
2. Check for `<workspace>/.distill-state.json`.
3. If it is absent, run the first-use workflow in [references/onboarding.md](references/onboarding.md).
4. If it exists, read it together with `STATUS.md`, then route by intent:
   - `开始蒸馏`: create a new cycle from source material.
   - `继续蒸馏`: resume `current_cycle` at its recorded stage.
   - `验证这条判断`: create or update an experiment.
   - `复盘`: record evidence and decide whether to revise, reject, retain, or promote a judgment.
   - `状态`: summarize current work and recommend exactly one next action.
   - `使用说明`: explain the complete loop and the available phrases.
5. Read [references/workflow.md](references/workflow.md) before creating or changing workflow artifacts.
6. Read [references/schemas.md](references/schemas.md) when validating state or artifact structure.

## Preserve the epistemic chain

Keep these layers distinct:

```text
source -> observation -> interpretation -> judgment -> experiment -> evidence -> principle
```

- Preserve links back to source material.
- Separate what the source says from what the user or agent infers.
- Mark uncertainty explicitly.
- Treat a new judgment as provisional.
- Promote a judgment to `principles/` only after meaningful validation or repeated independent evidence.
- Record contradictory evidence instead of smoothing it away.

## Initialize safely

After explaining the workflow and collecting the minimal setup facts, run:

```bash
python3 <skill-dir>/scripts/init_workspace.py \
  --root <workspace> \
  --focus "<primary material>" \
  --outcome "<desired output>" \
  --privacy "<public/private boundary>"
```

The initializer is idempotent and must not overwrite existing files. Inspect its JSON result and report created, preserved, and failed paths accurately.

Do not declare onboarding complete after creating folders. Invite the user to provide one real source and guide one complete minimum cycle through a provisional judgment and validation action.

## Keep interaction progressive

- Start with the map, then show only the current stage in detail.
- Ask only for information required to advance the current stage.
- Prefer one concrete source over broad autobiography.
- End each stage with: artifact created, current confidence, and one next action.
- Persist the full operating guide in `WORKFLOW.md`; do not repeatedly dump it into chat.

## Respect boundaries

- Never publish, upload, or expose source material without explicit authorization.
- Do not copy secrets or sensitive raw material into a public workspace.
- Do not invent source evidence, validation results, or confidence.
- Do not overwrite an existing state file, workflow document, status file, or user artifact.
- Do not treat polished wording as validation.

