# Operating workflow

## Contents

1. Capture
2. Extract
3. Synthesize
4. Validate
5. Consolidate
6. Status and recovery

## 1. Capture

Accept a bounded source or a reference to it. Give it a stable ID and record origin, date, context, privacy, and whether the source is complete. Keep sensitive sources outside public repositories when necessary; store a reference and a safe summary instead.

Exit condition: the source is identifiable and its boundary is clear.

## 2. Extract

Create a distillation record from the template. Extract:

- observations directly supported by the source;
- tensions, surprises, and recurring signals;
- missing context;
- interpretations labeled as interpretations.

Exit condition: fact and inference are visibly separated.

## 3. Synthesize

Form the smallest useful provisional judgment. Include:

- the claim;
- supporting observations;
- plausible alternatives;
- current confidence: low, medium, or high;
- what evidence could change the claim.

Avoid broad universal principles when the evidence supports only a local conclusion.

Exit condition: one judgment is explicit and falsifiable enough to test.

## 4. Validate

Create an experiment that states:

- action;
- expected observable result;
- timeframe or review trigger;
- disconfirming result;
- actual result, initially pending.

Validation may come from deliberate experiments, later decisions, repeated independent episodes, or credible external evidence. Writing quality and agreement from the agent are not validation.

Exit condition: a concrete test or evidence-gathering action exists.

## 5. Consolidate

During review, choose one outcome:

- retain: evidence is not yet decisive;
- revise: evidence supports a narrower or different claim;
- reject: evidence contradicts the claim;
- promote: repeated or meaningful evidence supports reuse.

For promotion, create a principle containing scope, conditions, counterexamples, evidence links, confidence, and review date. Never delete the earlier reasoning chain.

Exit condition: evidence changes the knowledge base rather than merely accumulating.

## 6. Status and recovery

Keep `.distill-state.json` machine-readable and `STATUS.md` human-readable. Record the current cycle and stage after every artifact change. When resuming, recommend exactly one next action based on the earliest unmet exit condition.

