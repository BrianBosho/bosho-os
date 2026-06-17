# POPE-200 Methodology-Aligned Ablation Plan (Chronological)

**Date:** 2026-03-05 \n**Dataset:** `runs/pope_raw200/inputs/manifest_pope_adversarial_200.csv` (200 samples) \n**Scope:** end-to-end ablations that propagate through **state**, **decision**, and **causal** grounding.

## 1) What We Are Doing (In Order)

We will ablate at each stage of the grounding methodology, in chronological order:

1\. Define real and null visual conditions.
2\. Extract token states (`H_real`, `H_null`) and patch states.
3\. Choose vector space treatment (raw vs whitened).
4\. Choose comparison kernels between text/patched representations.
5\. Choose aggregation/distribution summaries.
6\. Compute state/decision/causal track metrics.
7\. Evaluate on POPE targets and combined models.

This avoids ad-hoc metric mixing and guarantees every ablation cascades consistently to downstream tracks.

## 2) Methodology Pipeline and Ablation Points

### Stage A. Visual Conditions (Input Counterfactual Design)

**Fixed real condition:** `I_real` — original image from POPE sample.

**Ablated null conditions:**
- `N0_dataset_mean_patch`: dataset-wide mean patch null (current baseline).
- `N1_white_noise`: Gaussian null patch control.
- `N2_per_image_mean`: per-image mean patch null (must be truly per-sample in runner).

**Outputs affected:** Caption generation under null-sensitive dynamics. `H_null`, `V_null_l32`, and all downstream real-vs-null deltas.

### Stage B. Token/Patch Representation Space

**Space options:**
- `S0_raw`: current raw Layer-32 vectors.
- `S1_whitened`: whitened vectors for `H_real`, `H_null`, `V_l32`, and concept profile computations.

**Whitening specification:**
- Transform: PCA whitening `x_w = W(x - mu)`.
- Basis candidates:
  - `B0`: basis fit on POPE-200 run tensors (analysis-local basis).
  - `B1`: external fixed basis (if reusing prior experiment basis).
- Rule: use one locked basis per ablation block; do not mix bases inside a comparison.

**Outputs affected:** State similarity maps. Decision concept profiles/JSD. Causal support mask construction when concept profile uses whitened vectors.

### Stage C. Vector Comparison Kernels

**Kernel family:**
- `K0_cosine`
- `K1_dot`
- `K2_l2neg`
- `K3_bilinear_drift`

**Where kernels apply:**
- State: directly on `H_real/H_null` vs patches.
- Decision: concept profile similarity (`W_u` vs `V_real/V_null`) for footprint/JSD variants.
- Causal: support mask profile and optional contrastive profile variants.

### Stage D. Distribution and Aggregation

**Aggregation family:**
- Spread/shape: `var`, `std`, `max`, `range`, `kurtosis`.
- Mass/concentration: `pos_mass`, entropy/effective-rank.
- Ratio/margin: probability/log-prob ratios, contrast margins.
- Divergence: JSD family across temperatures.

**Track mapping:**
- State: patch-level deltas -> scalar token metrics.
- Decision: token probability shifts + concept-profile divergence.
- Causal: targeted counterfactual drops + random-control specificity + contrastive drops.

### Stage E. Final Evaluation

**Targets:**
- `is_correct`
- `is_hallucinated_yes`
- `within_yes`
- `within_no`

**Reports:**
- Single-metric ROC-AUC ranking (top-15 per target).
- Combined feature-set CV AUC (`state_only`, `decision_only`, `causal_only`, `dec+cau`, `all_tracks`, `all+cross`).

## 3) Practical Experiment Design (Factorized, Not Combinatorial)

We will not run all combinations at once. We run in three blocks, each locking earlier stages:

1\. **Block 1 (Null ablation):** vary Stage A only; keep `S0_raw`, `K0_cosine`, baseline aggregations.
2\. **Block 2 (Space ablation):** on best null from Block 1, compare `S0_raw` vs `S1_whitened`.
3\. **Block 3 (Kernel/Aggregation ablation):** on chosen null+space, vary kernels/aggregations.

This gives interpretability and manageable compute.

## 4) Run Blocks and IDs

### Block 1: Null ablations (forward-pass reruns)

| Run ID | Null | Space | Kernel | Notes |
|---|---|---|---|---|
| `B1_N0` | `dataset_mean_patch` | raw | cosine | baseline anchor |
| `B1_N1` | `white_noise` | raw | cosine | robustness check |
| `B1_N2` | `per_image_mean` | raw | cosine | requires true per-sample null wiring |

### Block 2: Space ablations (analysis-time if possible)

For the selected null from Block 1:

| Eval ID | Space | Whitening basis |
|---|---|---|
| `B2_S0` | raw | none |
| `B2_S1_B0` | whitened | POPE-200 fitted basis |
| `B2_S1_B1` | whitened | external fixed basis (optional) |

### Block 3: Kernel + aggregation ablations

Run using selected null+space:
- Kernels: `cosine`, `dot`, `l2neg`, `bilinear_drift`.
- Aggregation sets:
  - `A0_core`: variance + entropy + pos_mass + JSD core.
  - `A1_extended`: add form variants, ratio/margin families, contrastive families.

## 5) Cascading to State/Decision/Causal (Hard Requirement)

Any chosen `(null, space, kernel, aggregation)` setting must be applied consistently:

1\. **State track:** recompute token-level state metrics.
2\. **Decision track:** recompute probability shift and concept-footprint metrics in same space/kernel family.
3\. **Causal track:** recompute support masks and causal contrasts under same representation assumptions.

No mixed-condition tables are accepted as final evidence.

## 6) Implementation Status and Gaps

**Already available:**
- Multi-target eval includes `within_no`.
- Top-metrics-by-AUC table utility.
- Contrastive causal metrics in pipeline (`delta_logp_contrast`, `delta_p_contrast`, Yes/No contrasts).
- Extended derived decision/causal metric utilities in notebook.

**Gaps to close before full ablation:**
1\. `state.whitened_robustness` exists in config but is not wired in grounding execution.
2\. `per_image_mean` null currently behaves like run-level single null unless runner is refactored for per-sample null generation.

## 7) Outputs Per Run/Eval Block

Store under: `docs/experiments/results/pope_200_ablation/<block_or_run_id>/`

Required files:
- `dataset_all_tracks_<space>.csv`
- `auc_target_is_correct.csv`
- `auc_target_hallucinated_yes.csv`
- `auc_target_within_yes.csv`
- `auc_target_within_no.csv`
- `top15_by_target.csv`
- `combined_model_cv.csv`
- `summary.json`

## 8) Final Deliverables

1\. Chronological ablation report: what changed at each stage and why.
2\. Final comparison table:

| Target | Best metric | Track | Null | Space | Kernel | AUC |
|---|---|---|---|---|---|---|
| is_correct | ... | ... | ... | ... | ... | ... |
| is_hallucinated_yes | ... | ... | ... | ... | ... | ... |
| within_yes | ... | ... | ... | ... | ... | ... |
| within_no | ... | ... | ... | ... | ... | ... |

3\. Decision memo: selected methodology configuration for publication runs.

## 9) Immediate Next Actions

1\. Implement/fix `per_image_mean` null to be truly per-sample.
2\. Implement whitening path (or locked notebook-side recompute path) and basis selection protocol.
3\. Execute Block 1 null ablations on POPE-200.
4\. Freeze best null, then run Block 2 and Block 3.