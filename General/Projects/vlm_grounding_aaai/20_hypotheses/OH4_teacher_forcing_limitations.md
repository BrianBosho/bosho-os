---
title: OH4 - Teacher-Forced Formulation Concerns
type: hypothesis
status: open
created: 2026-06-16
tags: [hypothesis, limitations, theory]
---

# OH4: Teacher-Forced Formulation Concerns

## Source Trace
- Absorbed from: `20_hypotheses/future_hypotheses.md` (H-D)

## Open Question
Is token-level grounding the right unit of analysis, or should we focus on object-level grounding?

## Specific Concerns
1. Teacher forcing isolates token-level evidence — but is this the most meaningful granularity?
2. What if we focus on how the probability of *some* tokens changes when we remove all priors (language prior + image)?
3. Could we model generation as a **trajectory in some latent space**? Then grounding becomes: how much does that trajectory change when we perturb initial conditions (text priors vs. image tokens)?
4. Teacher forcing may be best understood as a way to isolate evidence, not as a complete grounding theory.

## Status
- **Conceptual** — no experiments. Teacher forcing is baked into the current pipeline. Changing this would require a significant scope extension. Low priority for AAAI.
