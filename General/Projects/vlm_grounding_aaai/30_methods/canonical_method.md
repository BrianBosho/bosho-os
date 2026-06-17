---
title: Canonical Method
type: method
created: 2026-06-16
tags: [method, grounding, instrument]
---

# Canonical Method

This document describes the active, canonical methodology for measuring visual grounding. It supersedes all previous implementations (V2, V3, etc.).

## Source Trace
- Absorbed from: `10_paper/PAPER_TRACK_AAAI.md`
- Absorbed from: `10_paper/PAPER_TRACK_FROZEN_v2.md`

## 1. Core Principle
Hold the prompt, token sequence, and decoding policy fixed. Replace the real image with a content-free null visual baseline. Measure how internal states and output probabilities change. Any measurable change is attributed to visual content.

**Why counterfactual, not absolute:** Raw cosine alignments between hidden states and patch vectors have a non-zero floor driven by anisotropy in the embedding space. Even purely textual tokens have non-trivial inner products with every patch vector. Subtracting a null-image pass removes this background correlation, isolating the image-specific signal.

## 2. Null Image Construction
The null image is a tensor `P⁰ ∈ ℝ^{576×1024}` in CLIP space — not a pixel image.

**Canonical null (N0): Dataset-mean patch.** Mean of all CLIP patch vectors across COCO validation. Removes semantic content while preserving the statistical distribution of visual features. Layout-preserving: injects the same number of tokens in the same positions.

*(Note: N0 was empirically validated over patch-shuffle, per-image-mean, and white-noise).*

## 3. Protocol
1. Generate a reference answer on the real image via greedy decoding.
2. Teacher-force the same token sequence under both real and null conditions.
3. Extract Layer-32 hidden states and logits at each token position under both conditions.
4. Extract Layer-32 patch representations from the real-image pass.
5. Compute the three tracks.

## 4. The Three-Track Instrument

### Track 1 — State grounding
Did the real image shift the token's hidden state toward specific patch directions?
- **Cosine delta matrix:** `Δ[t,j] = cos(H^r_t, V_j) − cos(H^0_t, V_j)`
- **Key metric:** `state_delta_var` — spatial variance of the delta row.
- **Interpretation:** High when the image caused a concentrated (not diffuse) state shift. Purely representational/correlational.

### Track 2 — Decision grounding
Did the real image change what the model chose to generate?
- **Probability shift:** `Δp_t = p^r_t(y*) − p^0_t(y*)`
- **Key metric:** `dec_dp_x_cvar = Δp_t × Var_j(concept_profile_j)`
- **Interpretation:** The `×cvar` term penalizes probability shifts with diffuse spatial attribution. This is the champion metric for scalar discrimination.

### Track 3 — Causal grounding
Are the attributed patches actually necessary for the prediction?
- **Procedure:** Identify top-k patches by concept profile, ablate them. Measure log-probability drop vs. matched random ablations of the same cardinality.
- **Key metrics:** `cau_rel_drop`, `cau_specificity_margin`.
- **Interpretation:** Strongest claim level — causal necessity, not just correlation.

## 5. Frozen Design Decisions

| Decision | Choice | Justification |
|----------|--------|---------------|
| Layer | 32 (final) | Grounding suppressed by L32 does not influence output. Measure what actually drives the decision. |
| Null | N0 (dataset-mean patch) | Empirically validated. Preserves CLIP distribution while removing semantic content. |
| Concept conditioning | `×cvar` product | Filters diffuse probability shifts. Expected to improve V/F separation. |
| Space | Raw Layer-32, no whitening | Stage B ablations: raw space dominates for `hallucinated_yes` across all kernels. |
| Random controls | K=3 matched random masks | Required for causal specificity. Cardinality-matched. |