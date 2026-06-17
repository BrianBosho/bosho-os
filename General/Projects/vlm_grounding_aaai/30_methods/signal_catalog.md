---
title: Signal Catalog
type: method-reference
created: 2026-06-16
tags: [method, signals, metrics]
---

# Signal Catalog

This document is the central dictionary for all explored candidate signals, metrics, and method variants. It maps out what each signal computes, its theoretical justification, and its current status.

## Active Signals (The Three-Track Instrument)

These signals form the core of the current `canonical_method.md` and the AAAI paper.

### 1. `dec_dp_x_cvar` (Decision Grounding Champion)
- **Math:** `Δp_t × Var_j(concept_profile_j)` where `Δp_t = p^r_t(y*) - p^0_t(y*)`
- **What it measures:** The image-conditioned probability shift of the generated token, penalized if the spatial support (concept profile) is diffuse.
- **Status:** **Active Champion**. Achieves AUC 0.885 on POPE adversarial (ablation line). 

### 2. `state_delta_var` (State Grounding)
- **Math:** Spatial variance of the cosine-delta row `Δ[t,j] = cos(H^r_t, V_j) - cos(H^0_t, V_j)`
- **What it measures:** Whether the real image shifted the token's Layer-32 hidden state toward specific, concentrated patch directions.
- **Status:** **Active**. Forms Track 1 of the paper (representational alignment).

### 3. `cau_rel_drop` (Causal Grounding)
- **Math:** `log P(target | ablated top-k) - log P(target | random top-k)`
- **What it measures:** The necessity of the visually supported patches. If the target token's probability drops significantly more when the specific support patches are removed compared to random patches, the token relies causally on that region.
- **Status:** **Active**. Forms Track 3 (Experiment B causal validation).

---

## Baseline Signals

### 4. `dec_log_p_ratio`
- **Math:** `log(p^r_t / p^0_t)`
- **What it measures:** Pure contrastive scalar shift.
- **Status:** **Strong Baseline**. AUC 0.873. Missing spatial/causal granularity, but very competitive as a pure hallucination detector.

### 5. `dec_delta_p`
- **Math:** `p^r_t(y*) - p^0_t(y*)`
- **What it measures:** Raw probability difference without concept conditioning (the `×cvar` term).
- **Status:** **Baseline**. AUC 0.877. 

---

## Archived / Rejected Variants (V2 SVD Formulations)

Detailed autopsy for these can be found in `method_decisions.md`.

### 6. `state_v2_score`
- **Math:** `projected_energy / delta_h_energy` using a truncated SVD basis `U_k`.
- **What it measures:** The fraction of the response magnitude (`delta_h_l2`) that lies within the selected patch-difference subspace.
- **Status:** **Rejected**. Failed to discriminate at the token level effectively.

### 7. Patch Attribution `alpha`
- **Math:** `alpha = DeltaH D_V^+`
- **Status:** **Rejected**. Suffered from subspace mismatch (used full rank pseudoinverse instead of truncated basis).

### 8. `decision_v2_fraction`
- **Math:** Ratio of `delta_logit_projected` to `delta_logit_linear`.
- **Status:** **Rejected**. Omitted the final RMSNorm map, meaning it was a poor surrogate for the actual final logit map.
