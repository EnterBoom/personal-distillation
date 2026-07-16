# Personal Distillation

把原始笔记、个人经历、项目材料、阅读摘录和决策记录，持续转化为可追溯的判断、可验证的假设与可复用的原则。

Personal Distillation is a stateful AI-agent Skill for turning raw material into traceable judgments, testable hypotheses, and reusable principles.

## Core workflow

```text
source -> observation -> interpretation -> judgment -> experiment -> evidence -> principle
```

这套工作流刻意区分“材料里实际发生了什么”与“我们如何解释它”，避免把表达得很漂亮的总结误认为经过验证的认知。

## What happens on first use

首次触发时，Skill 会：

1. 完整说明个人蒸馏的工作方式，以及用户与 AI 各自负责什么；
2. 确认主要材料、输入方式、期望产物和隐私边界；
3. 创建一个不会覆盖现有文件的状态化工作区；
4. 带用户用一份真实材料完成首次蒸馏和验证动作；
5. 保存当前状态，让下一次会话能够从正确阶段继续。

初始化后的工作区：

```text
.distill-state.json
WORKFLOW.md
STATUS.md
inbox/
distillations/
experiments/
reviews/
principles/
templates/
```

## Install

将 [`skills/personal-distillation`](skills/personal-distillation) 复制到你的 Agent Skills 目录，并保留目录名 `personal-distillation`。

Codex 示例：

```bash
cp -R skills/personal-distillation ~/.codex/skills/
```

除用于确定性初始化工作区的 Python 3 外，本 Skill 没有其他运行时依赖。

## Start

```text
Use $personal-distillation to initialize my workspace and guide my first complete distillation.
```

也可以使用以下中文入口：

- `初始化蒸馏工作区`
- `开始蒸馏`
- `继续蒸馏`
- `验证这条判断`
- `复盘`
- `状态`
- `使用说明`

## Repository structure

```text
skills/personal-distillation/
├── SKILL.md
├── agents/openai.yaml
├── scripts/init_workspace.py
├── references/
└── assets/workspace-template/
```

## Privacy

原始材料默认保持私密，蒸馏后的产物可以选择公开。Skill 不会在未经明确授权的情况下发布或上传材料。敏感来源可以保留在仓库之外，工作区只记录引用和安全摘要。

## License

[MIT](LICENSE)

