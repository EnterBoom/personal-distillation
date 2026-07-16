# Personal Distillation

把对话、经历、项目、产品、表达偏好和工作方法，持续整理成一套可追溯、可审计、可投喂给其他 AI 的个人知识库系统。

Personal Distillation is a stateful AI-agent Skill for building and maintaining a personal AI knowledge base. It combines knowledge organization with evidence-aware distillation:

```text
Knowledge system:
inbox -> classify -> module -> audit -> export -> acceptance test

Distillation kernel:
source -> observation -> interpretation -> judgment -> validation -> evidence -> reusable knowledge
```

## Why this is more than note organization

The Skill maintains four independent dimensions for every knowledge document:

- `status`: `empty`, `draft`, `usable`, or `verified`;
- `evidence_level`: `low`, `medium`, or `high`;
- `stability`: `stable`, `stage`, or `unconfirmed`;
- `privacy`: `private`, `internal`, `shareable`, or `public`.

A polished summary is not automatically verified knowledge. A useful document may still be stage-specific or private.

## The 13-module architecture

| Module | Purpose |
|---|---|
| `00_control` | System guide, routing, AI collaboration, status |
| `01_profile` | Identity, direction, capabilities, preferences, boundaries |
| `02_cases` | Resume, project evidence, outcomes, reusable cases |
| `03_offerings` | Products, services, pricing, delivery and acceptance |
| `04_voice` | Positive/negative samples, phrases, channels, QA |
| `05_workflows` | Repeatable SOPs with inputs, outputs and quality rules |
| `06_agents` | Agent roles, contracts, routing and handoffs |
| `07_projects` | Project context, execution, results and retrospectives |
| `08_decisions` | Changes of judgment, tradeoffs and priorities |
| `09_tests` | Ten acceptance domains and current results |
| `10_inbox` | Pending, organized and deferred raw material |
| `11_exports` | Control, full and purpose-specific AI context packs |
| `12_system` | Changelog, TODOs, missing knowledge, questions, versions |

## First use

The Skill does not stop after creating folders. It:

1. explains the system and collects a minimal owner profile;
2. creates the complete V0 workspace without overwriting existing files;
3. bootstraps the system guide, owner profile, and negative-positioning documents;
4. processes one real source through classification, module update, records, and audit;
5. saves state so later sessions resume from the correct stage.

## Install

Copy [`skills/personal-distillation`](skills/personal-distillation) into the Skills directory used by your agent environment. Keep the directory name `personal-distillation`.

Codex example:

```bash
cp -R skills/personal-distillation ~/.codex/skills/
```

The deterministic workspace tools require only Python 3 and the standard library.

## Start

```text
Use $personal-distillation to initialize my personal AI knowledge base and guide the first complete material-ingestion cycle.
```

Daily Chinese entry phrases:

- `整理新素材`
- `继续整理`
- `完善模块`
- `检查缺口`
- `导出投喂包`
- `测试知识库`

## Deterministic tools

```text
scripts/init_workspace.py     initialize the 13-module V0 workspace
scripts/migrate_workspace.py  migrate schema v1 state safely
scripts/create_intake.py      preserve one raw source or external reference
scripts/archive_intake.py     archive a processed or deferred source safely
scripts/audit_workspace.py    refresh status, gaps and maturity
scripts/build_export.py       build purpose-specific AI context packs
```

## Maturity

- **V0**: initialized structure and system records;
- **V1**: personally usable profile plus evidence-backed cases;
- **V2**: offerings, voice and workflows support real work;
- **V3**: agent-callable system with at least 8 of 10 acceptance domains passing.

File existence never advances maturity by itself.

## Privacy

Raw material remains private by default. The Skill never publishes or uploads sources without explicit authorization. Sensitive sources can stay outside the workspace while governed documents retain only a safe reference.

## License

[MIT](LICENSE)
