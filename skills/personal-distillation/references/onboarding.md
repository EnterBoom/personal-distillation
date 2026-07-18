# First-use onboarding

## Goal

Give the user a complete mental model, initialize a safe V0 workspace, and process one real source. Folder creation alone is not completed onboarding.

## 1. Explain the system

Explain concisely:

- The system turns raw material into maintained knowledge modules that other AI agents can retrieve.
- The operating loop is `capture -> classify -> distill -> update -> audit -> export -> test`.
- The agent structures, traces, audits, and maintains artifacts.
- The user supplies context, corrections, privacy boundaries, and confirmation.
- New claims remain drafts until evidence and confirmation justify promotion.

Name the six everyday phrases: `整理新素材`, `继续整理`, `完善模块`, `检查缺口`, `导出投喂包`, and `测试知识库`.

## 2. Collect the minimum profile

Collect only information that changes deployment:

- owner or system name;
- primary roles and current focus;
- main material types and how sources will be supplied;
- desired outputs and AI consumers;
- privacy boundary and public/private workspace choice.

Use safe defaults when requested: mixed material, manual input, reusable knowledge plus AI context packs, and private raw sources with shareable distilled outputs.

## 3. Initialize V0

Run:

```bash
python3 <skill-dir>/scripts/init_workspace.py \
  --root <workspace> \
  --owner "<name>" \
  --focus "<current focus>" \
  --source-method "<source method>" \
  --outcome "<desired output>" \
  --privacy "<privacy boundary>"
```

Report created and preserved paths accurately. V0 requires the full directory structure, control documents, status board, inbox rules, system records, and templates.

## 4. Bootstrap three control documents

Fill only user-confirmed information in:

- `00_control/00_system-guide.md`;
- `01_profile/01_about.md`;
- `01_profile/07_not-about.md`.

Leave missing sections explicit rather than inventing completeness.

## 5. Process one real source

Ask for one bounded source. Run the full ingestion transaction through module update, system records, and audit. Define a validation action when the source produces a judgment rather than a confirmed fact.

## 6. Complete onboarding

Set `onboarding.completed` true only when one intake is organized, at least one knowledge document was updated, and the audit completed. Finish with current maturity, created knowledge, unresolved questions, and one exact next phrase.

