# Grounding V3C: Evidence-Weighted Delta-Residual State Grounding

## 1. Purpose

This document defines the next state-grounding formulation after the V3B patch-evidence repair.

It answers: If V3B gives us a cleaner patch-evidence object than raw `||DeltaV_j||`, how should we build the next token-level state grounding score from `DeltaH_t` and that improved patch-side object?

This is a design source, not an implementation report. It is not implemented yet.

---

## 2. Why This Exists

The repo has gone through three distinct state-side framings:

### 2.1 Original state grounding

Used the cosine-delta matrix:

```
Delta[t,j] = cos(H_t^(r), V_j^(r)) - cos(H_t^(0), V_j^(r))
```

Patch side stayed anchored on `V_real` — not a clean `DeltaH` vs `DeltaV` comparison.

### 2.2 V2

Replaced cosine-delta matrix with a projection formulation:
- `DeltaH_t = H_t^(r) - H_t^(0)`
- `DeltaV_j = V_j^(r) - V_j^(0)`
- Token grounding = "how much of `DeltaH_t` lies in the image-specific patch-difference subspace?"

Cleaner, but still global. Did not ask whether token change aligned with a small, evidence-bearing patch subset.

### 2.3 Original V3 / delta-delta selective grounding

Tried to localize V2: kept `DeltaH_t`, kept `DeltaV_j`, defined patch evidence availability `A_j = ||DeltaV_j||`. Right direction, but raw `||DeltaV_j||` was not a trustworthy evidence signal.

### 2.4 V3A and V3B

V3A reframed patch side as a separate micro-problem: define structured non-null patch evidence in Layer-32 patch space, calibrate globally against a null model. V3B repaired V3A failure modes. The current default patch-side object is the V3B residual-plus-structure evidence family, especially `B1`.

V3C replaces raw `A_j = ||DeltaV_j||` with V3B's calibrated patch evidence.

---

## 3. Core Idea

The next state-grounding score should compare:

1. the token-side image-caused change `DeltaH_t`
2. against the V3B-cleaned patch-side evidence directions
3. while weighting patches by V3B evidence strength

Patch side has two objects:
- a **direction**: which non-null residual direction the patch contributes
- a **strength**: how much calibrated evidence that patch carries

One distinction is crucial:
- the patch-side evidence field is **image-static**
- the token-side support row is **time-varying**

For a fixed image, `{r_j, E_j, w_j}` do not change with token step `t`. What changes with `t` is:
- the token-side vector `DeltaH_t`
- its V3B-space form `h_t`
- the compatibility row `c_{t,:}`
- the selected support subset for that token

V3C = a fixed image-level evidence field + token-conditioned routing over that field.

---

## 4. Inputs

Same Layer-32 extraction objects:

```
H_t^(r), H_t^(0) in R^d
V_j^(r), V_j^(0) in R^d
```

with `t in {1,...,T}` answer tokens, `j in {1,...,M}` spatial patches, `M = 576`, `d = 4096`.

Token delta: `DeltaH_t = H_t^(r) - H_t^(0)`

Do **not** use raw `DeltaV_j` as the final patch-side evidence object. Instead, import the V3B replay/calibration outputs.

---

## 5. Patch-Side Objects Imported From V3B

For each patch `j`, V3B provides:

### 5.1 Residual direction

The cleaned patch residual in the V3B real-whitened space:

```
r_j in R^{K_real}
```

### 5.2 Evidence strength

Use thresholded `B1` as the default evidence weight:

```
E_j := B1_j = max(0, B1_j_raw - gamma_B1)
```

- `E_j = 0`: patch is not promoted as evidence
- large `E_j`: patch carries strong structured non-null evidence

### 5.3 Evidence weights

Normalize:

```
w_j = E_j / (sum_k E_k + epsilon)
```

Active evidence set: `E = {j : E_j > 0}`

If `sum_j E_j = 0`, all downstream state scores are `0`.

---

## 6. Token-Side Representation In The Same V3B Space

Map the token delta into the V3B real-whitened coordinates:

```
g_t = Lambda_real_K^{-1/2} U_real_K^T DeltaH_t  in R^{K_real}
```

Then remove the null/background subspace:

```
h_t = (I - P_null) g_t
```

V3C compares:
- token-side non-null change `h_t`
- patch-side non-null residual `r_j`

inside the same V3B space.

---

## 7. Token-Patch Compatibility

### 7.1 Default kernel: positive cosine alignment

```
c_{t,j} = max(0, cos(h_t, r_j))
```

`E_j` already carries patch magnitude and structure; cosine isolates directional alignment; clipping at `0` keeps support interpretation positive.

### 7.2 Alternative ablations

Projected-response kernel:
```
c_{t,j}^proj = max(0, <h_t, r_j / ||r_j||>)
```

Raw cosine without token null-projection:
```
cos(g_t, r_j)
```

---

## 8. Evidence-Weighted Support Row

### 8.1 Raw evidence-weighted row

```
s_{t,j}^raw = E_j * c_{t,j}
```

Use for: patch heatmaps, support-set selection, causal-mask construction.

### 8.2 Normalized evidence-weighted row

```
s_{t,j} = w_j * c_{t,j}
```

Because `sum_j w_j = 1`, the normalized row gives bounded token scores.

This is the mechanism that handles the static-vs-dynamic mismatch:
- `w_j` is fixed for the image
- `c_{t,j}` changes with token step `t`
- so different token steps can select very different patch subsets even though the underlying image evidence field is fixed

---

## 9. Token-Level State Grounding Scores

### 9.0 Token-side amplitude diagnostics

```
M_t^abs = ||h_t||_2^2
M_t^ratio = ||h_t||_2^2 / (||g_t||_2^2 + epsilon)
```

### 9.1 Total aligned evidence mass

```
G_t^mass = sum_j s_{t,j}
```

Bounded in [0, 1]. What fraction of the image's promoted evidence mass is positively aligned with token `t`?

### 9.2 Top-k aligned evidence mass (default score)

```
G_t^{top-k} = sum_{j in TopK(s_t)} s_{t,j}
```

Default `k = 8`. This should be the **default token score**.

### 9.3 Support concentration

```
pi_{t,j} = s_{t,j} / (sum_k s_{t,k} + epsilon)
G_t^conc = 1 - entropy(pi_t) / log(|E| + epsilon)
```

High when token-aligned evidence is focused on a small evidence-bearing patch subset.

### 9.4 Concentration-aware selective score

```
G_t^cap = G_t^{top-k} * G_t^conc
```

Main secondary diagnostic.

### 9.5 Non-evidence alignment leak

```
a_{t,j} = max(0, cos(h_t, r_j))
G_t^leak = sum_{j: E_j=0} a_{t,j} / (sum_j a_{t,j} + epsilon)
```

Low leak is desirable.

---

## 10. Sample-Level Aggregation

Let `C` be the content-token set.

```
G^mean = (1/|C|) sum_{t in C} G_t^{top-k}
G^cap-mean = (1/|C|) sum_{t in C} G_t^cap
G^leak-mean = (1/|C|) sum_{t in C} G_t^leak
```

---

## 11. Relation To V2

**V2 asks:** How much of `DeltaH_t` lies in the image-specific patch-difference subspace? (Global subspace explainability)

**V3C asks:** Does `DeltaH_t`, expressed in the V3B evidence space, align with a small subset of patches that carry calibrated non-null evidence? (Selective evidence-alignment)

The intended reading:
- high V2, high V3C: token change is globally visual and locally supported by evidence-bearing patches
- high V2, low V3C: token change is globally visual but not cleanly concentrated on strong evidence patches
- low V2, high V3C: unlikely — would suggest the V2 global subspace model is missing a selective local effect

V3C is the local/selective refinement of the V2 idea, not an unrelated branch.

---

## 12. Relation To The Old V3 Delta-Delta Spec

This formulation preserves the structure of `groundingv3.md`, but swaps in a better patch-side primitive.

Old V3 used: `A_j = ||DeltaV_j||`  
New V3C uses: patch direction `r_j` + patch evidence strength `E_j = B1_j`

Structural replacement: raw patch delta availability → V3B-calibrated patch evidence.

---

## 13. Causal Bridge

The raw evidence-weighted support row `s_{t,j}^raw = E_j * c_{t,j}` defines targeted support sets for causal ablation.

**Top-k support set:** `J_t = TopK(s_t^raw)`

**Top-mass support set:** Choose smallest `J_t` such that `sum_{j in J_t} rho_{t,j} >= alpha` with `alpha in [0.5, 0.8]`.

Natural causal handoff:
- V3B identifies evidence-bearing patches
- V3C identifies which of those patches support token `t`
- causal grounding can then intervene on that token-conditioned support set

---

## 14. Minimal Implementation Recipe

**Step 1:** Load `H_real`, `H_null`, V3B calibration tensors, per-sample V3B patch outputs (residuals and `B1`).

**Step 2:** Compute `DeltaH_t = H_t^(r) - H_t^(0)`

**Step 3:** Map into V3B space: `g_t = Lambda_real_K^{-1/2} U_real_K^T DeltaH_t`, then `h_t = (I - P_null) g_t`

**Step 4:** Load from V3B: `r_j`, `E_j = B1_j`, `w_j`

**Step 5:** Compute `c_{t,j} = max(0, cos(h_t, r_j))`

**Step 6:** Build `s_{t,j}^raw = E_j * c_{t,j}` and `s_{t,j} = w_j * c_{t,j}`

**Step 7:** Write token rows with:
- `state_v3c_token_nonnull_energy`
- `state_v3c_token_nonnull_ratio`
- `state_v3c_topk_mass`
- `state_v3c_mass`
- `state_v3c_conc`
- `state_v3c_cap`
- `state_v3c_leak`

**Step 8:** Aggregate across content tokens to sample-level scores.

---

## 15. First Experiment Block

The first implementation/evaluation block should compare:

1. original cosine-delta state grounding
2. V2 projection replay
3. original V3 delta-delta selective support
4. V3C evidence-weighted delta-residual support

The critical comparison: does replacing raw patch availability with V3B-calibrated patch evidence produce more selective, more stable, and more interpretable token support?

---

## 16. What This Formulation Claims

This formulation does **not** claim:
- that every changed patch should support every token
- that raw patch change magnitude is itself evidence
- that V3B patch evidence alone proves token grounding
- that the patch-side evidence field must vary with token time in order for token support to be selective

It **does** claim:

> A token is more state-grounded when its image-caused state change aligns with a small, concentrated subset of V3B-promoted evidence patches in the shared V3B semantic space.

Equivalently: state grounding here is token-conditioned routing over a fixed image evidence field.