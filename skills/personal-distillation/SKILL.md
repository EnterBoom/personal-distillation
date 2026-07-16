---
name: personal-distillation
description: Build and operate a stateful personal AI knowledge-base system that captures raw material, routes it into 13 knowledge modules, separates stable facts from stage-specific and unconfirmed claims, maintains evidence and usability states, audits gaps, exports purpose-specific AI context packs, and tests system maturity from V0 to V3. Use when a user asks to initialize a personal knowledge base, organize new notes or conversations, update a profile/case/product/style/SOP/agent/project/decision module, inspect knowledge gaps or status, continue unfinished knowledge work, export a prompt or agent context pack, test whether a knowledge base is usable, or perform personal distillation. Trigger on phrases such as "个人蒸馏", "初始化知识库", "整理新素材", "开始蒸馏", "继续整理", "完善模块", "检查缺口", "导出投喂包", "测试知识库", "状态", or "使用说明".
---

# Personal Distillation

Operate a personal knowledge system, not a folder of summaries. Preserve the chain from raw evidence to reusable knowledge while keeping the workspace usable by other AI agents.

## Resolve the workspace

1. Use an explicit user path when provided; otherwise use the current workspace root.
2. Check `<workspace>/.distill-state.json`.
3. If absent, follow [references/onboarding.md](references/onboarding.md).
4. If `schema_version` is `1`, run `scripts/migrate_workspace.py` before any other mutation.
5. If `schema_version` is newer than supported, stop without rewriting it.
6. Read `00_control/STATUS.md`, `12_system/MISSING.md`, and `12_system/TODO.md` before modifying knowledge.

## Route the intent

- `初始化知识库`: follow onboarding and initialize the 13-module workspace.
- `整理新素材` or `开始蒸馏`: follow [references/ingestion.md](references/ingestion.md).
- `继续整理`: resume `current_intake` from state and its earliest incomplete stage.
- `完善模块`: read the target module and its specification in [references/architecture.md](references/architecture.md), then fill evidence-backed gaps.
- `检查缺口` or `状态`: follow [references/gap-audit.md](references/gap-audit.md).
- `导出投喂包`: follow [references/exports.md](references/exports.md).
- `测试知识库`: follow [references/acceptance.md](references/acceptance.md).
- `使用说明`: explain the system map, six daily entry phrases, current maturity, and exactly one next action.

Read [references/governance.md](references/governance.md) before changing metadata or promoting knowledge. Read [references/workflow.md](references/workflow.md) for the full mutation transaction.

## Preserve two linked systems

Maintain both:

```text
Knowledge organization:
inbox -> classify -> module -> audit -> export -> acceptance test

Epistemic distillation:
source -> observation -> interpretation -> judgment -> validation -> evidence -> reusable knowledge
```

Do not collapse either chain. Module placement does not prove a claim, and a validated claim is not useful until it is retrievable from the correct module.

## Make every mutation transactional

For each accepted source:

1. Read current status, gaps, questions, and TODOs.
2. Preserve the raw source or a safe reference in `10_inbox/pending/`.
3. Classify it into one or more modules and stable, stage-specific, or unconfirmed information.
4. Update only relevant documents and preserve source references.
5. Move the intake to `organized/` or `deferred/` with a reason.
6. Append `12_system/CHANGELOG.md` and update questions/TODOs.
7. Run `scripts/audit_workspace.py --write` to refresh status and gaps.
8. Report changed files, extracted knowledge, unresolved questions, and one next action.

Do not report success if file changes, system records, or the audit did not complete.

## Use deterministic scripts

- Initialize: `scripts/init_workspace.py`
- Migrate v1: `scripts/migrate_workspace.py`
- Capture a source: `scripts/create_intake.py`
- Archive a processed source: `scripts/archive_intake.py`
- Audit status and gaps: `scripts/audit_workspace.py`
- Build an AI context pack: `scripts/build_export.py`

Inspect each command's JSON output. Never claim a path was written when the result marks it preserved or failed.

## Respect evidence and privacy

- Never invent identity, experience, results, data, preferences, or confirmation.
- Never promote a document to `verified` without explicit user confirmation.
- Keep `status`, `evidence_level`, and `stability` independent.
- Preserve contradictions and superseded decisions in history.
- Keep private raw material out of public repositories; store a safe reference when needed.
- Never publish or upload material without explicit authorization.
- Do not overwrite an existing user artifact; update deliberately or create a new version.
