---
type: project-execution
status: active
project: vlm_grounding_aaai
tags: [project, execution, vlm, aaai]
---

# VLM Grounding / AAAI Execution

Project brief: [[00_control/project_index.md|vlm_grounding_aaai]]
Planning: [[10_paper/PAPER_EXECUTION_TODO.md|To-Do]]

## Purpose
This page controls the current VLM execution path. It should keep the project moving toward the July 21 AAAI deadline.

## Current State

| Field | Status |
|---|---|
| Stage | Execution of Paper Experiments |
| Project status | Active |
| Priority | P1 |
| Deadline | 2026-07-21 |
| Current focus | Finalizing Experiments B and C for the paper |
| Current next action | Execute Experiment C: Evidence removal on correct cases |

## Active Deliverables

| Deliverable | Status | Target | Notes / link |
|---|---|---|---|
| Working thesis | Complete | | The intrinsic grounding signal detects failures that accuracy metrics miss. |
| Direction synthesis | Complete | | Absorbed into `OH*` and `concept_library.md`. |
| Experiment B: Causal validation | Active | | Needs formal significance reporting (paired t-test + Cohen's d). |
| Experiment C: Beyond-accuracy | Pending | | The core novel claim. Low-grounding correct answers degrade less under ablation. |
| H2: Token-class annotation | Pending | | Needs 100 POPE samples manually annotated. |

## Selected Actions

The selected checkboxes for the next few days live in [[10_paper/PAPER_EXECUTION_TODO.md|To-Do]]. Pull only 3-5 tasks at a time from the paper's "Blocking the paper" list.

## Blocked / Waiting

| Item | Blocker | Unblock action |
|---|---|---|
| Experiment C | Script not written | Write `run_experiment_c.py` using existing data. |

## Activity Log

| Date | Activity | Result | Next |
|---|---|---|---|
| 2026-06-16 | Structural ROS Migration | Vault reorganized into 10 strict domains (00-90) | Paper execution |
| 2026-06-16 | Knowledge Absorption | Ideas, methods, and hypotheses distilled into atomic schemas | Run Experiment C |
