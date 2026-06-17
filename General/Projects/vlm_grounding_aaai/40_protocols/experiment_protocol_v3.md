# Experiment: Four-Formulation Grounding Comparison

**Goal:** Empirically compare four per-token grounding formulations on four properties:
spatial localization, token selectivity, cross-token discriminability, and causal faithfulness.

**Model:** `llava-hf/llava-1.5-7b-hf` (LLaVA-1.5-7B)
**Null strategy:** Dataset-mean patch (N0) — tiled into all 576 slots in CLIP space (d_v=1024)

---

## Formulations Under Test

| ID | Formula | Label |
|----|---------|-------|
| **F-orig** | Δ_orig[t,j] = cos(H_t^(r), V_j^(r)) - cos(H_t^(0), V_j^(r)) | Original Cosine-Delta |
| **F-mid** | Δ_mid[t,j] = cos(ΔH_t, V_j^(r)) where ΔH_t = H_t^(r) - H_t^(0) | Token-Delta, Static Patches |
| **F-dd** | Δ_dd[t,j] = cos(ΔH_t, ΔV_j) where ΔH_t = H_t^(r) - H_t^(0), ΔV_j = V_j^(r) - V_j^(0) | Delta-Delta |
| **F-w** | Δ_w[t,j] = Δ_orig[t,j] · (‖ΔV_j‖₂ / max_k ‖ΔV_k‖₂) | ΔV-Weighted Cosine-Delta |

All vectors are Layer-32 hidden states (d=4096). V_j^(r) and V_j^(0) are extracted via `extract_l32_patches()` under real and null image respectively.

### Ablation Logic

The four formulations are organized into a **clean decomposition path** that changes one variable at a time, plus an **orthogonal test** of patch informativeness weighting.

**Decomposition path** (one variable at a time):

| Formulation | Token side | Patch side | What changed vs. previous |
|---|---|---|---|
| F-orig | cos(H_t^(r), ·) - cos(H_t^(0), ·) | V_j^(r) | — (baseline) |
| F-mid | cos(ΔH_t, ·) | V_j^(r) | Token: subtraction-of-cosines → cosine-of-delta |
| F-dd | cos(ΔH_t, ·) | ΔV_j | Patch: static V_j^(r) → delta ΔV_j |

- **F-orig → F-mid**: Isolates the effect of switching the token representation from a difference of two cosines to a single cosine of the delta vector.
- **F-mid → F-dd**: Isolates the effect of switching the patch reference frame from static real patches to patch deltas.

**Orthogonal test** (independent of the decomposition path):

| Formulation | What it tests |
|---|---|
| F-w | Does reweighting F-orig scores by patch informativeness (‖ΔV_j‖) improve spatial localization and selectivity, independently of any basis change? |

> **Interpretation note.** F-w and F-dd both suppress uninformative patches, but through different mechanisms: F-w applies an explicit multiplicative scalar to F-orig scores, while F-dd suppresses them implicitly through the cosine denominator ‖ΔV_j‖. These are not equivalent operations.

---

## Step 0 — Sample Selection

*Precondition: must satisfy all criteria before proceeding.*

Select **one** image from the COCO 2017 validation set satisfying:

1. **Single dominant object** with a clean, axis-aligned ground-truth bounding box covering 15–50% of the image area.
2. **Object class** must be a common concrete noun tokenized as a **single token** by the LLaVA tokenizer (e.g., `dog`, `chair`, `cup`, `bird`, `clock`).
3. Run greedy generation on the image with prompt: `"Describe what you see in this image."` The target noun must appear **at least once** in the generated output.
4. Identify the **first occurrence** of the target noun token in the generated sequence. Record its **token index** t* (1-indexed into the answer portion of the sequence).
5. Identify the **first period token** `.` that terminates a sentence in the same generated output. Record its token index t_ctrl.

> **Note on scope.** The single-token constraint excludes many COCO categories. This is acceptable for pipeline validation; the multi-image extension should relax this to include multi-token objects.

**Report at end of this step:**
```
COCO image ID: <id>
Object class: <class>
Token ID of focal noun: <token_id>
Token index t*: <index>
Token index t_ctrl: <index>
Generated description (full): "<text>"
```

---

## Step 1 — Tensor Extraction

Run two teacher-forced forward passes on the fixed generated sequence Y* from Step 0.

**Pass 1 (real image):** Extract from Layer 32:
- H^(r) ∈ R^{T×4096} — all answer token hidden states
- V^(r)_L32 ∈ R^{576×4096} — image-position hidden states at Layer 32

**Pass 2 (null image — N0 mean patch):** Extract from Layer 32:
- H^(0) ∈ R^{T×4096}
- V^(0)_L32 ∈ R^{576×4096}

Also extract:
- P^(r)_t[y_t] — real-image token probabilities for all t (from softmax over logits)
- P^(0)_t[y_t] — null-image token probabilities for all t

**Sanity checks (abort if any fail):**
- ‖V^(r)_L32‖_{row mean} ∈ [80, 130] (Layer-32 norms; not CLIP-space norms)
- ‖V^(0)_L32‖_{row mean} ∈ [80, 130]
- H^(r) and H^(0) have identical shape (T, 4096)

> **Calibration note.** The [80, 130] range is empirical. If this is the first run, compute the actual distribution over 10 images and set bounds at ±2σ from the observed mean.

---

## Step 2 — Formulation Computation

Compute score vectors over all M = 576 patches for the focal token t*, the control token t_ctrl, and **all** T answer tokens.

### Shared intermediates

1. ΔH_t = H_t^(r) - H_t^(0) for all t ∈ {1, …, T}
2. ΔV_j = V_j^(r) - V_j^(0) for all j ∈ {1, …, 576}
3. w_j = ‖ΔV_j‖₂ / max_k ‖ΔV_k‖₂ — normalized ΔV magnitudes (shape: 576)

### F-orig

Δ_orig[t, j] = cos(H_t^(r), V_j^(r)) - cos(H_t^(0), V_j^(r))

Compute for all t ∈ {1, …, T}, all j ∈ {1, …, 576}.

### F-mid

Δ_mid[t, j] = cos(ΔH_t, V_j^(r))

Compute for all t ∈ {1, …, T}, all j ∈ {1, …, 576}. Uses the same ΔH_t as F-dd but the same static patch basis as F-orig.

### F-dd

Δ_dd[t, j] = cos(ΔH_t, ΔV_j)

Compute for all t ∈ {1, …, T}, all j ∈ {1, …, 576}.

### F-w

Δ_w[t, j] = Δ_orig[t, j] · w_j

Element-wise product of the F-orig matrix with the broadcast weight vector.

**Report:** For each of the eight focal/control vectors (2 tokens × 4 formulations), report: min, max, mean, std. Also report: min, max, mean of w_j (the ΔV weight vector) and count of patches where w_j < 0.1 (effectively suppressed patches).

---

## Step 3 — Spatial Localization Test

1. Reshape each focal vector (orig_focal, mid_focal, dd_focal, w_focal) from shape (576,) to (24, 24).
2. Upsample each (24, 24) grid to the original image resolution (336×336) using bilinear interpolation.
3. Min-max normalize each heatmap to [0, 1].
4. Convert the COCO ground-truth bounding box to a binary mask at 336×336 resolution.

**Threshold-based IoU** (at threshold = 0.5):
5. Threshold each heatmap at 0.5 to produce a binary activation mask.
6. Compute IoU between each binary activation mask and the GT bounding box mask.

**Threshold-free metrics:**
7. **Pointing accuracy**: Does the argmax patch (in the 24×24 grid) fall inside the GT bounding box? Report as 1/0 per formulation.
8. **Energy-inside-box**: What fraction of total heatmap mass falls inside the GT bounding box region?

EnergyInBox(F) = Σ_{(i,j) ∈ GT} heatmap(i,j) / Σ_{(i,j)} heatmap(i,j)

**Report:**
```
         IoU  PointAcc  EnergyInBox
F-orig:  <value>  <0|1>  <value>
F-mid:   <value>  <0|1>  <value>
F-dd:    <value>  <0|1>  <value>
F-w:     <value>  <0|1>  <value>

Save heatmap overlays as: heatmap_orig.png, heatmap_mid.png, heatmap_dd.png, heatmap_w.png
```

---

## Step 4A — Token Selectivity Test

Using the focal and control vectors from Step 2:

SelectivityRatio(F) = Var(focal scores under F) / Var(ctrl scores under F)

Also compute a bounded contrast metric:

SelectivityContrast(F) = (Var_focal - Var_ctrl) / (Var_focal + Var_ctrl)

**Report:**
```
         Var_focal  Var_ctrl  Ratio  Contrast
F-orig:  <value>    <value>   <value>  <value>
F-mid:   <value>    <value>   <value>  <value>
F-dd:    <value>    <value>   <value>  <value>
F-w:     <value>    <value>   <value>  <value>
```

---

## Step 4B — Cross-Token Discriminability Test

Using the full (T, 576) score matrices from Step 2, compute a scalar grounding score per token per formulation.

**Token classification.** Manually annotate each token in the generated sequence into one of three classes:
- **(V)** Visual object noun — a concrete noun referring to an object visible in the image
- **(A)** Attribute — an adjective or modifier describing a visual property (color, size, position)
- **(F)** Function word — articles, prepositions, conjunctions, copulas, punctuation

**Per-token scalar.** For each formulation F ∈ {F-orig, F-mid, F-dd, F-w}, compute a scalar grounding score per token as the variance of the patch score vector:

G_F(t) = Var_j(Δ_F[t, j]), j ∈ {1, …, 576}

**Evaluation.** Compute mean G_F per class.

**Report:**
```
         mean_V  mean_A  mean_F  ratio_V/F  ordering_holds
F-orig:  <val>   <val>   <val>   <val>      <V>A>F? yes/no>
F-mid:   <val>   <val>   <val>   <val>      <V>A>F? yes/no>
F-dd:    <val>   <val>   <val>   <val>      <V>A>F? yes/no>
F-w:     <val>   <val>   <val>   <val>      <V>A>F? yes/no>
```

**Passing criterion (at scale, N≥20 images).** V > A > F for each adjacent comparison at p < 0.01 (Wilcoxon signed-rank), with V/F ratio ≥ 2.0.

---

## Step 5 — Causal Ablation Test

**Patch identification** (using adaptive support sets):

For each formulation F ∈ {F-orig, F-mid, F-dd, F-w}:
- Compute s_j = max(0, Δ_F[t*, j]) for all j (positive contributions only).
- Sort patches by s_j descending, accumulate normalized mass until cumulative coverage ≥ 0.90 with minimum 10 patches → Ω_F.
- Record |Ω_F| (the adaptive set size per formulation).

**Random baseline:**
- Sample max(|Ω_orig|, |Ω_mid|, |Ω_dd|, |Ω_w|) random patch indices (seed=42), excluding any overlap with any Ω_F → Ω_rand.

**Ablation procedure** (five forward passes, teacher-forced on Y*):

For each Ω ∈ {Ω_orig, Ω_mid, Ω_dd, Ω_w, Ω_rand}:
- Replace the Layer-0 projector output X^(0,r) at positions j ∈ Ω with the corresponding null projector output X^(0,0) (i.e., the null-image projected patches, in projector output space d=4096).
- Run teacher-forced forward pass and extract log P_ablated[y_{t*}].

> **Critical:** Ablation injects null patches in **projector output space** (Layer-0 / X^(0,r) space, d=4096), not Layer-32 space. Do not use V^(0)_L32 vectors here.

**Report:**
```
log P(y_t*) — real image (baseline): <value>

              log_P_ablated  drop  |Ω|  specificity_margin
F-orig ablation:  <value>   <val>  <N>  <value>
F-mid ablation:   <value>   <val>  <N>  <value>
F-dd ablation:    <value>   <val>  <N>  <value>
F-w ablation:     <value>   <val>  <N>  <value>
Random ablation:  <value>   <val>  <N>  —

(specificity margin = drop(F) - drop(random))
```

---

## Step 6 — Inter-Formulation Agreement

Compute pairwise Spearman rank correlations between all four formulations' patch score vectors at the focal token t*:

ρ(F-orig, F-dd) = SpearmanR(Δ_orig[t*, :], Δ_dd[t*, :])

and similarly for all six pairs. The decomposition path comparisons are the most informative:
- **F-orig ↔ F-mid**: How much does the token-side basis change affect patch ranking?
- **F-mid ↔ F-dd**: How much does the patch-side basis change affect patch ranking?
- **F-orig ↔ F-w**: Does multiplicative ΔV weighting reorder patches, or just rescale?

**Report:**
```
Focal-token rank correlation:
  F-orig ↔ F-mid: ρ = <value>  (token-side change)
  F-mid ↔ F-dd:   ρ = <value>  (patch-side change)
  F-orig ↔ F-dd:  ρ = <value>  (full change)
  F-orig ↔ F-w:   ρ = <value>  (weighting only)
  F-mid ↔ F-w:    ρ = <value>
  F-dd ↔ F-w:     ρ = <value>

Mean rank correlation across all T tokens:
  F-orig ↔ F-mid: ρ = <value>
  F-mid ↔ F-dd:   ρ = <value>
  F-orig ↔ F-dd:  ρ = <value>
  F-orig ↔ F-w:   ρ = <value>
  F-mid ↔ F-w:    ρ = <value>
  F-dd ↔ F-w:     ρ = <value>
```

---

## Final Report

Produce a structured JSON file `results.json` with all reported values, plus `scope: "single-image diagnostic (not a statistical comparison)"` and interpretation notes on:
- `decomposition_interpretation`: which variable change (token-side vs patch-side) contributed more
- `weighting_interpretation`: whether F-w improved over F-orig independently
- `overall_diagnostic`: which formulation performed best across all four properties

Save outputs: `heatmap_orig.png`, `heatmap_mid.png`, `heatmap_dd.png`, `heatmap_w.png`, `results.json`

---

## Design Rationale: Changes from v1

| Change | Reason |
|--------|--------|
| Added **F-mid** (token-delta, static patches) as decomposition intermediate | Creates a clean one-variable-at-a-time path: F-orig → F-mid changes only the token representation, F-mid → F-dd changes only the patch reference frame. |
| Reframed **F-w** as an orthogonal test, not a decomposition step | F-w and F-dd suppress uninformative patches through different mechanisms; F-orig → F-w → F-dd was not a clean decomposition. |
| Added **Step 4B** (cross-token discriminability) | The test that killed projection R². A formulation that scores function words as highly as visual nouns is structurally broken. |
| Added **Step 6** (inter-formulation agreement) | Tests whether formulations are measuring the same spatial construct at different scales, or genuinely different constructs. |
| Added **pointing accuracy** and **energy-in-box** to Step 3 | Threshold-free alternatives to IoU; more robust for single-image diagnostics. |
| Added **SelectivityContrast** (bounded) to Step 4A | The raw Var ratio is unbounded and inflated when ctrl variance is near zero. |
| Changed causal ablation to **adaptive support sets** (α=0.90 coverage) | Fixed top-10 doesn't respect formulation-specific concentration profiles. |
| Added **ΔV weight vector diagnostics** to Step 2 | Characterizes how much of patch space F-w treats as uninformative. |
