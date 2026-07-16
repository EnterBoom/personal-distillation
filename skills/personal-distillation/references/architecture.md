# Knowledge architecture

## Module map

| ID | Directory | Answers | Typical content |
|---|---|---|---|
| 00 | `00_control` | How should AI use this system? | system guide, routing, collaboration rules, status |
| 01 | `01_profile` | Who is the owner and who are they not? | identity, main line, judgments, audience, abilities, preferences, boundaries |
| 02 | `02_cases` | What evidence supports capability? | resume, outcomes, project and delivery cases |
| 03 | `03_offerings` | What is offered and to whom? | product/service matrix, pricing, boundaries, acceptance |
| 04 | `04_voice` | How does the owner communicate? | positive/negative samples, phrases, channels, quality rules |
| 05 | `05_workflows` | How is work performed? | SOPs with inputs, steps, outputs, QA, errors |
| 06 | `06_agents` | How should AI work for the owner? | agent roles, inputs, outputs, routing and handoffs |
| 07 | `07_projects` | What happened in specific projects? | context, design, execution, results, retrospectives |
| 08 | `08_decisions` | Why did direction change? | context, old/new judgment, tradeoffs, impact, priority |
| 09 | `09_tests` | Is the knowledge base usable? | test prompts, expected output, criteria, results |
| 10 | `10_inbox` | What has not been organized? | pending, organized, and deferred raw material |
| 11 | `11_exports` | What should another AI receive? | control, full, and purpose-specific context packs |
| 12 | `12_system` | What is missing or changing? | changelog, TODO, missing, questions, version |

## Classification rules

Use one primary module and optional secondary links:

- identity or preference -> `01_profile`;
- demonstrated history or result -> `02_cases`;
- product, customer, delivery, pricing -> `03_offerings`;
- liked/disliked expression or channel style -> `04_voice`;
- repeatable process -> `05_workflows`;
- AI role, prompt contract, handoff -> `06_agents`;
- bounded project material -> `07_projects`;
- change of judgment, tradeoff, priority -> `08_decisions`;
- evaluation prompt or pass criteria -> `09_tests`.

If a source spans modules, keep one source in the inbox archive and link it from every updated document. Do not duplicate raw material across modules.

## Required document shapes

- Case: background, owner's contribution, actions, result, evidence, reusable lessons, applicable scenarios.
- Offering: fit/non-fit, pain, value, deliverables, required inputs, workflow, acceptance, exclusions, upgrade path.
- Style: positive/negative samples, pattern, channel, do/don't rules, QA criteria.
- SOP: scenario, inputs, steps, outputs, QA, errors, missing user input, reusable prompt.
- Agent: responsibility, suitable/unsuitable tasks, required modules, input, output contract, QA, handoff conditions.
- Project: background, goals, design, execution, issues, results, review, reusable knowledge.
- Decision: date, context, old view, new judgment, reasons, deferred actions, next priority, affected modules.
- Test: instruction, expected output, pass criteria, common failures, latest result.
