# Metric Definitions (Version 1.0)

*Source: Visual Faithfulness Project Handbook — Metric Registry + Visual Grounding Metrics Explained.*
*Locked 2026-06-16. Do not modify definitions without bumping version.*

---

## Notation

- x ∈ R^d — raw embedding vector
- c ∈ R^d — spectral coefficient vector (after SVD projection)
- p_i = c_i^2 / sum(c_j^2) — spectral PMF (energy distribution)
- λ_i — eigenvalues of covariance matrix Σ (sorted descending)
- σ_i = sqrt(λ_i) — singular values

---

## Core Spectral Metrics

### Spectral PMF
Convert any spectrum c to a probability distribution:

    p_i = c_i^2 / sum_j(c_j^2)

Satisfies p_i ≥ 0, sum p_i = 1.

---

### Spectral Entropy (H)
Measures spread/ambiguity of representation:

    H(p) = -sum_i p_i * log(p_i)

- High H = generic/abstract, energy spread across many dims
- Low H = specific/grounded, energy concentrated

---

### Effective Rank (eRank)
Continuous measure of intrinsic dimensionality:

    p_i = σ_i / sum_j(σ_j)          (normalize singular values, not squared)
    eRank(X) = exp(-sum_i p_i * log(p_i))

Note: eRank uses σ_i (singular values), not λ_i (eigenvalues). This differs from the PMF entropy above which uses c_i^2.

- eRank = d → isotropic (all dims equally active)
- eRank = 1 → rank-1 collapse
- White noise → eRank ≈ d (high), blank gray → eRank much lower

---

### Participation Ratio (PR)
Counts "active" dimensions, robust to noise eigenvalues:

    PR(X) = (sum_i λ_i)^2 / sum_i(λ_i^2) = Tr(Σ)^2 / Tr(Σ^2)

Range: [1, d]. Closely related to eRank but uses squared eigenvalues — more sensitive to dominant directions.

---

### Effective Dimensionality
Scalar interpretable form of entropy:

    d_eff = exp(H(p))        (perplexity form)
    d_eff = 1 / sum_i(p_i^2) (inverse participation, L2-based)

"Cat uses ~247 effective dimensions; 'the' uses ~886."

---

## Cross-Station Grounding Metrics

### Spectral Efficiency (η) — PRIMARY METRIC

    η = eRank(T) / eRank(F)

Quantifies information preservation through the projector (Station F → Station T).

- η → 1.0: projector preserves rank
- η < 0.5: predicts hallucination (expected AUC > 0.70 on POPE)
- η > 1.0: theoretically possible (expansion), rare in practice

Calculation: subtract per-station global mean before computing eRank. Use scipy.linalg.svd, full_matrices=False.

---

### SpecVIG (Spectral Visual Information Gain)
JSD between real and null image spectral PMFs at a given station:

    SpecVIG = JSD(p_real || p_null)
            = 0.5 * KL(p_real || m) + 0.5 * KL(p_null || m)

where m = 0.5 * (p_real + p_null).

Range: [0, ln(2)] ≈ [0, 0.693]

Empirical values (one image):
- CLIP (Station F): ~0.38 (strong visual divergence)
- Projector (Station T): ~0.21 (moderate)
- Input manifold: ~0.04 (text tokens dominate)
- Output manifold (z): ~0.06

---

### Grounding Ratio
Fraction of input visual signal that survives to output:

    Grounding Ratio = SpecVIG_output / SpecVIG_CLIP

Empirical: ~0.147 (14.7% of CLIP signal reaches output).

---

### Grounding Delta (Δ)
Measures visual "work" vs. texture-matched baseline:

    Δ = JSD(P_T(I_real) || P_T(I_texture))

where I_texture = Perlin noise matched to I_real frequency content.

Interpretation:
- Δ < 0.4: low grounding (perceptual failure)
- 0.4 < Δ < 0.7: moderate
- Δ > 0.7: high grounding (if hallucination still occurs → cognitive failure)

Texture generation: Perlin octaves=4, persistence=0.5. Average over 10 random seeds (variance ±0.05).

---

### Fabrication Index (Φ)
Ratio of null-image to real-image transformation energy:

    Φ = Mean_E_i(Null Pass) / Mean_E_i(Real Pass)

where E_i = JSD(P_initial_i || P_final_i) for patch i (Layer 0 to Layer 32).

- Φ ≈ 0: faithful — model only transforms patches when visual evidence present
- Φ → 1: pre-emptive fabricator — model reshapes patches to match prior regardless of input

---

### Transformation Energy (E_i)
Per-patch "work" done by the LLM across 32 layers:

    E_i = JSD(P_{initial, i} || P_{final, i})

where P_initial = spectral PMF at Layer 0, P_final = spectral PMF at Layer 32, for image patch i.

---

## Divergence Metrics

### Jensen-Shannon Divergence (JSD)
Symmetric, bounded ∈ [0, ln2]:

    JSD(p||q) = 0.5 * KL(p||m) + 0.5 * KL(q||m),  m = 0.5(p+q)

Use case: compare any two spectral PMFs (tokens, time steps, passes).

---

### Semantic Drift
JSD between projector and output spectral PMFs:

    Drift = JSD(p_projector || p_output)

Empirical: ~0.58 (84% of maximum) — projector and output are nearly orthogonal.

---

### Cross-Station Alignment (Cosine)
    Alignment = c_projector · c_output / (||c_projector|| * ||c_output||)

Empirical: ~0.048 — output spectrum points in almost a completely different direction than projector.

---

## Token-Level Metrics

### Spectral Flux
Rate of semantic change along a sequence:

    Φ_t^(JSD) = JSD(p_t, p_{t-1})

High flux = model actively reorganizing semantic focus (transient regime).
Zero flux = attractor regime (converged or looping).

---

### Null–Semantic Energy Ratio
Given null basis N (d×k, orthonormal columns) from PSC-3:

    c_null = N * N^T * c          (projection onto null subspace)
    c_sem  = c - c_null

    ρ_null = ||c_null||^2 / ||c||^2     (prior dominance index)
    ρ_sem  = 1 - ρ_null

"the" → high ρ_null; "Nairobi" → low ρ_null.

---

## Anisotropy

### Anisotropy Index (A)
    A(H) = λ_1 / sum_i(λ_i) = λ_1 / Tr(Σ)

- A → 1: all embeddings cluster around one direction (cone effect)
- A → 1/d: isotropic

ZCA whitening removes the cone effect; expected to increase probe accuracy for hallucination detection.

---

## Gini Coefficient (Sparsity)
    G = sum_i sum_j |a_i - a_j| / (2 * d * sum_i a_i)

where a_i = |c_i|.

- High G → few axes dominate (localist/sparse)
- Low G → diffuse (ambiguous)

---

## Intensity Gain
    Intensity Gain = ||c_real||_1 / ||c_null||_1

Empirical: ~0.66 at CLIP (real image has less total spectral energy than gray). At output: ~1.01 (equalize).

---

## Grounding Density (Γ)
Per-token grounding quality combining spatial anchor proximity and transformation energy:

    Γ_j = S_{j,i} × E_i

where S_{j,i} = cosine similarity between generated token j and its nearest-neighbor patch i at Layer 32.

- High Γ: word anchored to a heavily transformed patch → faithful
- Low Γ: word points to a "lazy" (low E_i) patch → hallucinated

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-06-16 | Initial definitions from handbook |
