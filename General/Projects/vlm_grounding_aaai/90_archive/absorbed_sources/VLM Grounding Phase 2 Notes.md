> [!WARNING]
> Archived note. Checkboxes below are historical and not active.
---
title: VLM Grounding Phase 2 Notes
type: research-note
created: 2026-04-19
tags: [brain-dump, research, vlm, phase-2]
---

# VLM Grounding Phase 2 Notes

Source: [[../../00 Inbox/Workbook q2 wk1 - Raw Archive|Workbook q2 wk1 - Raw Archive]]

## Main concerns recorded in the workbook

- `delta_p` works, but it may be more of a contrastive-decoding basis than the direct contribution
- Spatial attribution was not performed even though the work depends on finding support patches
- The POPE-based setup may be a weak or even mistaken evaluation choice for some tests
- Kernel sensitivity may indicate either a patch-selection problem or a metric problem

## Specific technical questions captured from the workbook

- What exactly do CKA and spatial structure preservation in CLIP tell us here?
- How should spatial localization on POPE be done?
- What does kernel sensitivity reveal about selected patches versus the metric?
- What exactly is being measured in `F2b`?
- Are noun words, function tokens, and adjective tokens being split correctly?
- Can hidden-state deltas for sampled words be visualized to inspect the distribution?
- Are the anisotropy measurements satisfactory?
- Is the null baseline adequate, and if so why are informative patches still hard to distinguish?
- Could patch decoding or a patch logit lens provide a better way to identify support patches?

## Hypotheses and next-experiment ideas

- A better metric should distinguish:
  - random real patches from null-image patches
  - average similarity among null patches versus random real patches
- If null patches are genuinely null, failure to separate them from informative patches is a metric problem
- Patches that decode to clearly meaningful words may provide a more surgical evaluation anchor
- Decision grounding may serve as a strong baseline and anchor point
- Investigating projector-input information flow to layer 32 may itself be a new research direction

## Section-level reminders from the workbook

### F1

- Null baseline may be adequate as a true null
- The unresolved issue is patch-wise difference measurement
- POPE may not be the right place for the core question
- First-token variance before teacher forcing may be more revealing than current tests

### F2

- Need a better account of anisotropy and patch similarity
- Need to test whether cosine is actually the right hidden-state comparison metric
- Need deeper investigation of noun/function/adjective token behavior
- Need to dig deeper into `F2D`

### F3

- Need to double-check how the experiment was run
- Need to investigate prepositions and spatial support
- If supporting patches cannot be identified, the core hypothesis is in trouble

### F4

- Bounding-box design may be distorting the experiment
- Need to test smaller and more concentrated bounding boxes

### F5

- Need to understand MDS and CKA better

### F6

- Decision grounding seems to work and can be used as a baseline

## Explicit next tasks from the workbook

- Complete the review of the Phase 2 report
- Preferably run new experiments
- Reformulate the paper track and log adjacent ideas
- Iterate quickly through the hypothesis
- Double-check how nouns and function words were derived from POPE questions
- Decide which Phase 2 results are adequate
- Decide which results change the hypothesis
- Decide which results are inconclusive and need to be rerun
- Decide what findings are solid
- Separate core paper contributions from adjacent standalone research directions

## Experiment review checklist

- Complete the review of the Phase 2 report.
- Re-check how the experiments were actually run.
- Identify which results are solid enough to keep.
- Identify which results are inconclusive and need reruns.
- Revisit the metric choice for patch comparison.
- Verify token splitting for nouns, function words, and adjectives.
- Decide whether POPE remains part of the core evaluation.
- Separate core-paper contributions from side directions.

## Core issue tracker

| Issue | Current concern | Required action |
|---|---|---|
| `delta_p` interpretation | may be useful but not the true contribution | redefine claim or reposition as baseline |
| Spatial attribution | support patches were not properly localized | design a direct localization experiment |
| POPE setup | may be weak for the core question | decide whether to replace or demote it |
| Kernel sensitivity | may reflect metric failure rather than patch failure | test alternative metrics and controls |
| Null baseline | may be valid but still not separating patches well | check whether the metric is the real bottleneck |

## Section experiment table

| Section | Main question | Next experiment or analysis |
|---|---|---|
| F1 | how should patch-wise differences be measured | test alternatives to current patch-difference approach |
| F2 | are anisotropy and token-similarity analyses meaningful | compare cosine with alternative hidden-state metrics |
| F3 | can supporting patches actually be identified | rerun with stronger spatial-support analysis |
| F4 | are bounding boxes distorting the result | test smaller and tighter boxes |
| F5 | what do MDS and CKA actually reveal here | tighten interpretation and supporting plots |
| F6 | can decision grounding anchor the whole story | formalize it as a baseline or central comparison |

## Decision table

| Decision to make | Good evidence would look like |
|---|---|
| Which results are adequate | stable outcome and clear interpretation |
| Which results change the hypothesis | evidence that forces a different framing |
| Which results are inconclusive | ambiguous outcome or setup uncertainty |
| What belongs in the paper | supports the core claim directly |
| What becomes a side project | interesting but not required for the main paper |

## Immediate next actions

| Order | Action | Output |
|---|---|---|
| 1 | audit all current Phase 2 results by section | keep, rerun, or drop decisions |
| 2 | choose one improved metric or localization test | next experiment definition |
| 3 | state the core paper claim again after the audit | tighter paper track |

