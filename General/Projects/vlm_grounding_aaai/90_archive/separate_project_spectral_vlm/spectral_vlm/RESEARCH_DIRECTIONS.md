# Research Directions & Micro-Experiments

*Source: Visual Faithfulness Project Handbook — Research directions section + MATs Application.*
*Each micro-experiment is a 3–10 hour work unit.*

---

## MATs Hypotheses (High-Level)

### H1: Metastable Trap of Hallucination
Hallucinations correspond to the system getting stuck in a spurious minimum of the energy landscape.
Prediction: Hopfield energy E(ξ) of hallucinated sequence is locally minimized (∇E ≈ 0) but globally higher than grounded truth.

### H2: Symmetry Breaking Failure (Object Hallucination)
Object hallucination = failure of spontaneous symmetry breaking where the visual field H_visual is insufficient to overcome the entropic barrier of the language prior.
Prediction: In hallucinated generations, susceptibility χ = ∂ξ/∂H_visual will be low (visual decoupling).

### H3: Spectral Flux Divergence at Onset of Fabrication
Just before the first hallucinated token, Φ(t) (spectral flux) spikes, then collapses into a low-complexity limit cycle.

---

## Direction 1: Mechanistic Flow & Information Decay

*How the visual signal physically survives the journey from Pixel to Token.*

1. **The Scrambling Test** — Does the projector (T) preserve semantic rank of CLIP (F)?
   - Metric: Effective Dimensionality at F vs T
   - Pass: lower rank at T proves projector is bottleneck

2. **The 4096-D Expansion** — Does increasing dim add noise or detail?
   - Metric: Sparsity Index at projector station
   - Pass: high sparsity confirms expansion is mathematical padding, not semantic enhancement

3. **Layer-wise Decay** — At what layer does visual signal become "invisible"?
   - Metric: Preservation Ratio R at every 4th layer
   - Pass: decay curve identifies "Amnesia Point"

4. **The Attention Bottleneck** — Does the model "look" but not "extract"?
   - Metric: Correlate attention head activation with Information Gain (Δ_out)
   - Pass: high attention + low SpecVIG = "looks but doesn't listen"

5. **The Residual Leak** — Does visual signal bypass attention heads via residual stream?
   - Metric: Cosine similarity between Layer 0 and Layer 32 (Residual Trace)
   - Pass: high similarity = "passing through" pixels rather than reasoning

---

## Direction 2: Manifold Migration & The "Nudge"

*Tracking the transformation of "alien" visual patches into "native" linguistic embeddings.*

6. **Migration Speed** — Does the "nudge" happen early or late?
   - Metric: JSD Gradient across all layers
   - Pass: locates the "Translation Engine" in the architecture

7. **Manifold Displacement** — How far is the "Cat" from the Cat?
   - Metric: Euclidean distance between concept-pairs (Image/Text)
   - Pass: reveals a "Universal Translation Constant"

8. **Rotation Index** — Is the "nudge" a rotation or a scale?
   - Metric: Procrustes Analysis on hidden states
   - Pass: determines if model preserves "Visual Energy" during translation

9. **The Semantic Landing Zone** — Do all "Cats" land in the same spot?
   - Metric: Cluster Density of cat images at Layer 0 vs Layer 32
   - Pass: proof of conceptual convergence

10. **Path Divergence** — Do different questions nudge the same pixels to different places?
    - Metric: Final coordinates of a single patch under two different prompts

---

## Direction 3: Grounding vs. Fabrication (PRIORITY — "Smoking Gun")

*Is the model faking the evidence or seeing it?*

11. **The Null-Image Fabrication Test** — Do gray patches move toward the answer?
    - Metric: E_i (transformation energy) for gray vs real image
    - Pass: if E_null ≈ E_real → model is fabricating

12. **The Fabrication Index (Φ)** — Quantify "lying":
    - Φ = E_null / E_real
    - Pass: Φ > 0.8 predicts hallucination

13. **Information Work Principle** — Does the model work harder for truth?
    - Metric: Total JSD for correct vs hallucinated responses
    - Pass: faithful answers require less transformation work

14. **The Hallucination Floor** — What does the model "see" by default on null input?
    - Metric: Spectral signature of gray image response
    - Pass: reveals the model's internal world bias

15. **Distortion Metric** — How much does the model "warp" the pixels?
    - Metric: Change in eigenvalue distribution across migration
    - Pass: separates "smooth translation" from "violent overwriting"

---

## Direction 4: Causal Anchoring & Source Credit

*Which pixels are the "witnesses" for each word?*

16. **The Anchor Search** — Which patch is the "Cat" word closest to?
    - Metric: Nearest Neighbor mapping in the final layer
    - Pass: spatial heatmap of evidence

17. **The Lazy Patch Anomaly** — Do words ever point to "still" patches?
    - Metric: Correlation between Semantic Proximity S_j and Transformation Energy E_i
    - Pass: hallucinated words point to low-E_i patches

18. **The Pivot Patches** — Are 90% of patches redundant?
    - Metric: Gini Coefficient of E_i across the image
    - Pass: energy concentrated in ~10% of patches

19. **The Cross-Modal Anchor** — Does a "sink" patch look like the "sink" word?
    - Metric: Compare Top-K eigenvectors of anchor patch vs word
    - Pass: spectral isomorphism between vision and language

20. **The Attention Sink Effect** — Are patches just "placeholders"?
    - Metric: Check if E_i is concentrated in a single patch
    - Pass: reveals degenerate grounding strategy

---

## Direction 5: Linguistic Priors & Bias

*How much is the model "leading the witness"?*

21. **PDI Spike** — Does specificity kill grounding?
    - Metric: Prior Dominance Index (ρ_null) for general vs specific prompts

22. **Blur Collapse** — At what blur level does the model stop looking?
    - Metric: Preservation Ratio R as function of blur amount

23. **Prompt-Induced Amnesia** — Can a question make the model "forget" pixels?
    - Metric: SpecVIG decay under high-complexity prompts

24. **Vocabulary Bias** — Do rare words require more grounding?
    - Metric: Correlate token frequency with Preservation Ratio R

25. **Question-Pixel Synergy** — Does a well-formed question sharpen the manifold?
    - Metric: Effective Dimensionality under different quality prompts

---

## Direction 6: Representational Geometry

*The "shape" of the internal data.*

26. **The Universal Basis** — Is there a hidden rotation aligning all modes?
    - Metric: Canonical Correlation Analysis (CCA) to find shared vision-language subspace

27. **Manifold Curvature** — Are hallucinations "straight lines"?
    - Metric: Curvature of hidden state path across 32 layers

28. **Information Entropy** — Do hallucinations have lower entropy?
    - Metric: Shannon Entropy of spectral coefficients per segment

29. **Redundancy Ratio** — How much information is "double-counted"?
    - Metric: Mutual Information between adjacent patch hidden states

30. **Semantic Drift Constant** — How much "meaning" is lost per layer?
    - Metric: Drift Gradient (JSD per layer pair) for benchmark images

---

## Execution Order (Recommended)

Phase 1 (Hours 1–8): Direction 3 — Fabrication vs. Truth
- Run Null-Image test (#11) first → most likely "smoking gun"
- This requires only: hooks at Layer 0 and Layer 32 + JSD computation

Phase 2 (Hours 9–20): Direction 4 — Causal Anchoring
- Nearest neighbor mapping (#16, #17) on results from Phase 1

Phase 3 (Hours 21+): Direction 2 — Migration Heatmap
- Layer-by-layer JSD gradient (#6) for full picture

---

## Conflict Probing (Causal Validation)

Use adversarial images where model "should" see one thing but priors say another (e.g., blue oranges, 3-legged dogs, DALL-E generated anomalies).

Expected result: High Δ + hallucination → cognitive failure (H3). Patching projector activations from a grounded run into a hallucinated run should correct the output AND spike the SpecVIG monitor simultaneously. This proves the monitor tracks a causal mechanism.

---

## Related

- [[PROJECT_OVERVIEW]] — hypotheses H1–H4 and timeline
- [[METRIC_DEFINITIONS]] — all metric formulas
- [[THEORETICAL_BACKGROUND]] — physics foundations for MATs hypotheses
