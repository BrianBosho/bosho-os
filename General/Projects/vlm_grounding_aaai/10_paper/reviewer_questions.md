---
title: Reviewer Questions
type: paper-notes
created: 2026-06-16
tags: [paper, review, defense]
---

# Reviewer Questions & Defense

## Source Trace
- Absorbed from: `10_paper/PAPER_TRACK_FROZEN_v2.md` (Experiment A section)

## The ratio baseline — addressed head-on

**Reviewer challenge:** `dec_log_p_ratio` achieves AUC 0.873 — within 1.2 points of the champion on scalar detection. Why do we need the complex instrument if a simple ratio does almost as well?

**Defense:**
The instrument's value over the ratio is not improved scalar detection. It is decomposition into three distinct questions about the image's role:

1. **Where** the image matters (spatial localization via the concept profile — the ratio is a scalar with no spatial information)
2. **Whether** the image matters (decision-level probability shift — shared with the ratio, but concept-conditioned by `×cvar` to filter diffuse shifts)
3. **Whether necessarily** the image matters (causal track — the ratio cannot distinguish causal from correlational evidence)

This must be argued concretely with worked examples, not just asserted.
