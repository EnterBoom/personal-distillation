# First-use onboarding

## Goal

Give the user a complete mental model, initialize a safe workspace, and finish one minimum real distillation cycle.

## Stage 1: Explain the system

Explain these points concisely before changing files:

1. Personal distillation converts raw material into traceable judgments and reusable principles.
2. The loop is `capture -> extract -> synthesize -> validate -> consolidate`.
3. The user supplies lived context, corrections, and real-world evidence.
4. The agent structures material, separates fact from inference, exposes uncertainty, and maintains artifacts.
5. A draft judgment is not a principle until evidence supports it.

Also name the six everyday entry phrases:

- `开始蒸馏`
- `继续蒸馏`
- `验证这条判断`
- `复盘`
- `状态`
- `使用说明`

## Stage 2: Collect the deployment profile

Collect only:

- primary material: experiences, reading, projects, decisions, content, or mixed;
- current source location or delivery method;
- desired output: principles, methods, articles, decisions, or mixed;
- privacy boundary: what may be public and what must remain private.

If the user asks for defaults, use `mixed`, `manual input`, `reusable principles`, and `private raw sources / shareable distilled outputs`.

## Stage 3: Initialize

Run `scripts/init_workspace.py` with the selected values. Summarize what it created and what it preserved. If `.distill-state.json` already exists, stop treating the session as first use and resume from its state.

## Stage 4: Complete the first minimum cycle

Ask for one bounded source: a note, event, decision, project episode, or excerpt. Then:

1. Save or reference the source in `inbox/`.
2. Create one record in `distillations/`.
3. Separate observations from interpretations.
4. Form one provisional judgment with a confidence label.
5. Define one observable validation action in `experiments/`.
6. Update `.distill-state.json` and `STATUS.md`.

Do not force principle promotion in the first cycle.

## Stage 5: Handoff

Finish with:

- what was created;
- the provisional judgment;
- how it will be validated;
- the exact phrase the user can say next.

Mark `onboarding_completed` true only after the first distillation and its validation action exist.

