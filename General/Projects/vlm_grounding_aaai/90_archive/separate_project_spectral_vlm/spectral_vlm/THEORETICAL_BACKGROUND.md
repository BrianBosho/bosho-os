# Theoretical Background

*Source: Visual Faithfulness Project Handbook — Phase Transitions, Statistical Mechanics, Geometric Analysis sections.*
*This doc condenses three major frameworks used to motivate spectral grounding research.*

---

## Framework 1: Physics of Attention (Hopfield / Energy Landscape)

### Key Insight
The attention operation in Transformers is mathematically equivalent to a Modern Hopfield Network update rule, which minimizes a global energy function:

    E(ξ) = -(1/β) * log(sum_i exp(β * x_i^T * ξ)) + (1/2) * ξ^T * ξ

- First term (LSE): pulls state ξ towards stored patterns x_i
- Second term: regularization preventing magnitude divergence

**Grounded token** = global minimum of E(ξ) where query aligns with retrieved memory.
**Hallucination** = spurious local minimum where energy is locally minimized but state doesn't correspond to a valid memory pattern.

### Phase Transitions & Symmetry Breaking
Generation is modeled as a transition from high-entropy "disordered" phase (uniform vocab probability) to low-entropy "ordered" phase (token selection).

The visual stimulus acts as a symmetry-breaking field H_visual:

    E_total(ξ) = E_internal(ξ) - H_visual^T * ξ

If visual field is too weak to break the symmetry of the language prior, the system drifts into a hallucinated attractor.

### Spectral Flux
    Φ(t) = ||Λ_t - Λ_{t-1}||_F

where Λ_t = diagonal matrix of eigenvalues of hidden state covariance at step t.

- High Φ: transient regime — model actively reorganizing (e.g., just before hallucination)
- Φ ≈ 0: attractor regime — converged or looping

---

## Framework 2: Statistical Mechanics of Embeddings

### Embeddings as Probability Distributions
Any embedding x ∈ R^d can be mapped to a PMF via:

    p_i = σ_i / sum_j σ_j   (normalize singular values)
    or
    p_i = σ_i^2 / sum_j σ_j^2  (normalize eigenvalues)

This allows application of information-theoretic measures (entropy, JSD, etc.) to neural representations.

### Three Key Hypotheses

**H1: Entropy Minimization of Grounding**
Visual grounding manifests as reduction in Spectral Entropy (sharpening of feature distribution) vs. text-only prior:

    ΔH(p) = H(p_grounded) - H(p_text_only) < 0

An ungrounded LLM operates with high effective rank (epistemic uncertainty). Visual evidence collapses this superposition.

**H2: Eigen-Disentanglement of Visual Concepts**
Specific eigenvectors of the local covariance matrix correspond to disentangled visual concepts. The "Dog" concept is a principal direction v_dog such that:

    PMI(u_j; Dog) = log[ P(High_u_j | Dog) / P(High_u_j) ]

High-PMI eigenvectors are the "Eigen-features" responsible for representing that concept.

**H3: Hallucination as Semantic Drift (JSD)**
Hallucinated tokens exhibit a sudden spike in JSD relative to the preceding context window:

    JSD(h_t || h_{t-1}) spikes at onset of hallucination

---

## Framework 3: Geometry of High-Dimensional Activation Spaces

### The Cone Effect (Representation Anisotropy)
Neural representations are not uniformly distributed on the hypersphere. They cluster in narrow sub-regions — the "cone effect."

**Anisotropy Index:**

    A(H) = λ_1 / Tr(Σ)

- A → 1: collapsed to 1D line
- A → 1/d: isotropic

Empirically, A increases in deeper layers ("layer-wise anisotropy accumulation").

**Why it matters for VLMs:** Image and text encoders initialize into *disjoint* cones. The contrastive optimization in CLIP aligns these cones angularly without merging them — the "Modality Gap."

### Effective Rank vs. Participation Ratio

| Metric | Formula | Sensitivity |
|---|---|---|
| eRank | exp(-sum p_i log p_i), p_i = σ_i / sum σ_j | Uses sqrt of eigenvalues, measures volume |
| PR | (Tr Σ)^2 / Tr(Σ^2) | Uses squared eigenvalues, measures sparsity |

eRank measures the "volume" of the state space; PR measures "inequality" in variance distribution.

### ZCA Whitening (Optimal for MLLMs)
Among all whitening transforms W s.t. W Σ W^T = I, ZCA minimizes distortion:

    W_ZCA = U Λ^{-1/2} U^T

This preserves local topology and semantic alignment of individual tokens while removing anisotropy. Unlike PCA whitening, it does not suffer from "stochastic axis swapping" between batches.

**Application:** Decorrelated Batch Normalization (DBN) applies ZCA to mini-batch inputs, explicitly forcing layer activations toward isotropy.

### Three Geometric Hypotheses for Hallucination Detection

**H1: Spectral Entropy Divergence**
Hallucinated tokens occupy a locally higher-dimensional subspace (higher eRank) than grounded tokens:

    eRank(H_halluc) >> eRank(H_ground)
    ScreeSlope(H_halluc) < ScreeSlope(H_ground)   (flatter slope = heavier tail = more uncertainty)

**H2: Visual Hallucination via Subspace Misalignment**
Object hallucinations occur when image embeddings fall into the null space of the text manifold projection. Given text manifold basis U_txt:

    P(Hallucination | v) ∝ ||v - U_txt @ U_txt^T @ v||^2    (off-manifold residual energy)

High residual = visual signal is noise to the decoder.

**H3: Anisotropy-Induced Semantic Drift**
High anisotropy compresses the angular margin between factual and counterfactual tokens, making them indistinguishable under cosine similarity. ZCA whitening restores the margin:

    Acc_probe(Z_ZCA) > Acc_probe(X_raw)

Gain ΔAcc is proportional to A(X_raw).

---

## The Modality Gap (CLIP)

Image embedding centroid μ_I and text centroid μ_T are separated by a persistent shift vector Δ_gap = μ_I - μ_T, even for "perfect" pairs. Two competing explanations:

1. **Cone Effect (initialization)**: Vision and text transformers are initialized independently, mapping to different random cones. Contrastive training aligns cones angularly without merging them.

2. **Temperature stabilization (optimization)**: The modality gap acts as a buffer stabilizing the InfoNCE loss. Gap distance decays only logarithmically, so it persists through finite training.

**Implication for grounding**: Images that lie further from the text manifold (high off-manifold residual ρ) are more prone to causing hallucinations where the LLM ignores the visual prompt.

---

## Dimensional Collapse

A catastrophic failure mode in self-supervised learning where the embedding space degenerates:

- **Neural Collapse (NC1)**: Within-class variability → 0; all samples collapse to class mean
- **Dimensional Collapse in SSL**: trivial solution to similarity maximization = constant vector for all inputs (eRank = 1)

**The paradox:**
- Low ID (collapse) is bad: limits expressivity, causes blind spots
- Low ID is good (manifold hypothesis): truthful data lies on structured low-dim manifold; hallucinations are high-dim excursions

Resolution (Queipo-de-Llano 2025): massive activations in specific tokens (e.g., BOS) act as "attention sinks," creating "compression valleys" in middle layers. Reliability depends on whether this compression retains the correct semantic topology.

---

## Spectral Forward Pass (Full Pipeline)

One inference pass should produce four spectra:

1. **CLIP spectra** — input image patches in CLIP space (1024-D)
2. **Projector/Adapter spectra** — image patches in projector output space (4096-D)
3. **Input spectra** — text + image input embeddings in Vicuna space
4. **Output spectra** — final generated tokens in Vicuna space

Per-patch analysis at any station: raw spectrum plot, PMF spectrum, energy distribution, entropy, most active eigenvectors.

Cross-patch analysis: compare patches to find if they correspond to same concepts; check bounding box patches vs. random patches.

---

## Related

- [[METRIC_DEFINITIONS]] — all metric formulas with precise definitions
- [[PSC_METHODS]] — interventions motivated by ZCA/whitening theory
- [[RESEARCH_DIRECTIONS]] — experimental operationalizations of these hypotheses
- [[PROJECT_OVERVIEW]] — how these frameworks map to POPE experiments
