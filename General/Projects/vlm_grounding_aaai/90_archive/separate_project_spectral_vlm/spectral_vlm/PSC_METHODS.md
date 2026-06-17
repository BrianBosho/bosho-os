# Principal Subspace Calibration (PSC) Methods

*Source: Visual Faithfulness Project Handbook — Regularization section.*
*PSC = removing "null content" (stopword/syntax axes) from spectral representations.*

---

## Setup & Notation

- Embedding dimension: d (e.g., 4096)
- Spectrum in global SVD basis: c ∈ R^d
- Null probes: W_null (stopwords, punctuation, glue tokens)
- For each w ∈ W_null: spectrum c(w) ∈ R^d

Build:
- Null matrix S ∈ R^{n_null × d}, S_{i,:} = c(w_i)^T
- Per-dimension null energy: E^null_j = (1/n_null) * sum_i c_j(w_i)^2
- Normalized nullness score: r_j = E^null_j / max_k E^null_k ∈ [0, 1]

Every PSC method is a linear transform T applied to c:  **PSC(c) = c_tilde = T @ c**

---

## PSC-1: Hard Axis Masking

Zero out dimensions that carry most stopword energy.

1. Sort indices by descending null energy: π = argsort(E^null)[::-1]
2. Choose K (fixed) or cumulative threshold η (e.g., 90%):
   find smallest K s.t. sum_{k=1}^K E^null_{π_k} / sum_j E^null_j ≥ η
3. Null index set: I_null = {π_1, ..., π_K}
4. Transform:
   c_tilde_j = 0       if j ∈ I_null
   c_tilde_j = c_j     otherwise

In code: precompute Boolean mask, do `c[mask] = 0`.

---

## PSC-2: Soft Axis Shrinkage (Diagonal Reweighting)

Shrink high-null dimensions with a weight w_j ∈ (0, 1].

1. Compute nullness scores r_j ∈ [0, 1]
2. Choose shrinkage strength α ≥ 0

Linear shrink:
    w_j = 1 - α * r_j   (clipped to [β, 1], e.g., β=0.1)

Or inverse:
    w_j = 1 / (1 + α * r_j)

3. Transform: c_tilde_j = w_j * c_j

Matrix form: c_tilde = W @ c, W = diag(w_1, ..., w_d)

---

## PSC-3: Null-Subspace Projection (Canonical PSC)

Learn a null subspace from stopwords; project onto its orthogonal complement.

1. Build S ∈ R^{n_null × d} (optionally center rows)
2. SVD: S = U_s Σ_s V_s^T
3. Choose k s.t. first k singular values explain ≥ 90–95% of stopword variance
4. Null basis: N = [v^(s)_1, ..., v^(s)_k] ∈ R^{d × k} (orthonormal columns)
5. Projectors:
   P_null = N @ N^T      (project onto null subspace)
   P_sem  = I_d - P_null (project onto semantic complement)
6. Transform: c_tilde = P_sem @ c = c - N @ (N^T @ c)

**This is the canonical PSC: remove the null-subspace component from c.**

---

## PSC-4: Null Covariance Whitening / Mahalanobis Shrinkage

Use covariance of null spectra to shrink directions of high null variance.

1. Compute centered null matrix: S_hat, covariance Σ_null = (1/(n-1)) * S_hat^T @ S_hat
2. Add ridge: Σ_λ = Σ_null + λ*I (λ > 0 for stability)
3. Whitening operator (using eigen decomposition Σ_λ = Q Λ Q^T):
   Full: T = Σ_λ^{-1/2} = Q @ Λ^{-1/2} @ Q^T
   Mild: T = Σ_λ^{-γ} = Q @ Λ^{-γ} @ Q^T,  0 < γ ≤ 1/2
4. Transform: c_tilde = T @ (c - μ_null)

Intuition: dimensions where stopwords have high variance get down-weighted.

---

## PSC-5: Regression-Based Null Prediction (Nuisance Regression)

Learn a linear map that predicts the null component, then subtract it.

1. Fit linear map N ∈ R^{d × d} minimizing:
   min_N sum_{w ∈ W_null} ||c(w) - N @ c(w)||^2 + λ||N||_F^2
2. For arbitrary c:
   c_null = N @ c
   c_tilde = c - c_null = (I_d - N) @ c

N captures typical null patterns; we subtract them from all spectra.

---

## PSC-6: Discriminative Null vs. Content Subspace (LDA-Style)

Use labeled data (stopwords vs. content words) to find discriminant directions.

1. Build S_null ∈ R^{n_null × d} and S_cont ∈ R^{n_cont × d}
2. Compute class means μ_null, μ_cont
3. Within-class scatter S_W, between-class scatter S_B
4. Solve generalized eigenproblem: S_B @ v = λ * S_W @ v
5. Large λ → strongly discriminates (semantic directions)
   Small λ → both classes look similar (null directions)
6. Threshold on λ, form P_sem from semantic eigenvectors
7. Transform: c_tilde = P_sem @ c

---

## PSC-7: Hybrid (Projection + Diagonal Shrink)

Combine PSC-3 (null subspace removal) then PSC-2 (soft shrinkage):

1. Compute null basis N and P_sem (PSC-3)
2. First project: c' = P_sem @ c
3. Then apply diagonal shrink with weights w_j: c_tilde_j = w_j * c'_j

---

## Unified Code Interface

```python
def apply_psc(c, mode="projection", params=None):
    if mode == "none":
        return c
    elif mode == "mask":         # PSC-1
        mask = params["mask"]    # bool array length d
        c = c.clone()
        c[mask] = 0.0
        return c
    elif mode == "soft":         # PSC-2
        w = params["weights"]    # shape [d]
        return w * c
    elif mode == "projection":   # PSC-3
        N = params["N"]          # shape [d, k], orthonormal cols
        return c - N @ (N.T @ c)
    elif mode == "whiten":       # PSC-4
        T = params["T"]          # shape [d, d], precomputed
        return T @ (c - params.get("mu_null", 0.0))
    elif mode == "regress":      # PSC-5
        N = params["N"]          # shape [d, d] or [d, r]
        return c - (N @ c)
    elif mode == "lda":          # PSC-6
        P_sem = params["P_sem"]  # shape [d, d]
        return P_sem @ c
    else:
        raise ValueError(f"Unknown PSC mode {mode}")
```

---

## Recommended Variants for Primary Use

For an initial ablation, prioritize:
1. **PSC-3 (projection)** — canonical, interpretable
2. **PSC-1 (mask)** — simplest, fast sanity check
3. **PSC-2 (soft)** — smooth trade-off between 1 and 3

Compare their effects on: eRank, anisotropy index A, and POPE accuracy.

---

## Related

- [[METRIC_DEFINITIONS]] — ρ_null, ρ_sem (null-semantic energy ratio), anisotropy index A
- [[PROJECT_OVERVIEW]] — PSC as H4 intervention
