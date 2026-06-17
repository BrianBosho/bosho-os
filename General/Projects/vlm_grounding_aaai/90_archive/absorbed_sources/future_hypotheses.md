# Open Hypotheses and Research Ideas

*Source: VLM Grounding Ideas doc (Tab 1). Captured 2026-06-16. These are unresolved hypotheses — not yet formalized into experiments.*

---

## H-A: Support Patches Do Not Correspond to Bounding Box Patches at Layer 32

**Observation:** Early results show that the support patches identified through the grounding process (state/decision/causal) do not correlate meaningfully with the patches inside the COCO bounding box at Layer 32.

**Hypothesis:** Support patches are generally not well-correlated with the ground-truth bounding box patches, and masking support patches produces a larger token-probability drop than masking bounding box patches.

**Implication:** If true, this would indicate that visual information has been "smeared" across patches during the LLM's processing — the patches no longer contain spatially localized information in the way they did earlier in the pipeline.

**Proposed experiment:**

1. For a given object token, identify support patches via the grounding procedure (validated causally).
2. Also identify the bounding box patches from COCO annotation (or segmentation mask patches) at Layer 32.
3. Run two separate ablations at Layer 32:
   - Mask the **bounding box patches** → record log P drop for the target token.
   - Mask the **support patches** → record log P drop for the target token.
4. Compare: which ablation produces a larger drop?

**Cascade experiment (if H-A is confirmed):**

To localize *where* the smearing happens, step back through the pipeline:

- Ablate at **projector output space** (replace bounding box patches with null patches at projector output) — does this restore the correlation?
- Ablate at **CLIP space** (before the projector).
- Ablate at **pixel level**.

This creates a localization ladder: LLM layers → projector → CLIP encoder → pixel space. The point in the pipeline where bounding box ablation starts to match support patch ablation is where information dispersion begins.

**Status:** Not yet run. Connects to [[SPATIAL_LOCALIZATION_PROTOCOL_v1]] (which ablates at projector output space, not Layer 32).

---

## H-B: Spatial Structure Matters for Support Row Statistics

**Observation:** The support row `s_t = {k(v_j, h_t)}` over 576 patches is currently summarized with scalar statistics (variance, entropy, max, etc.) that treat it as a flat 1D vector. But the 576 patches form a 24×24 grid.

**Problem:** Three patches with similar values arranged **horizontally** (j, j+1, j+2) look "concentrated" under most 1D statistics. Three patches with the same values arranged **vertically** (j, j+24, j+48) look "dispersed" — even though the spatial concentration is identical.

Current metrics would report these as completely different distributions, but the underlying spatial pattern is the same.

**Hypothesis:** Spatial structure in the support row is informative and current 1D statistics systematically mischaracterize it.

**Possible compensations:**

- Compute 2D spatial statistics on the reshaped (24×24) support map instead of the flat (576,) vector.
- Use IoU-based or region-based metrics rather than scalar reductions.
- Check whether transformers disperse information along a "line" direction rather than a grid — if so, the 1D treatment may be structurally correct for what the model is doing, even if wrong for what the image contains.

**Status:** No experiment run. Relevant to spatial localization test in [[experiment_protocol_v3]] (Step 3) and [[SPATIAL_LOCALIZATION_PROTOCOL_v1]].

---

## H-C: Contrastive Decoding as a Grounding Baseline

**Question:** Can contrastive decoding logit difference serve as a strong baseline for grounding?

Contrastive decoding tells us whether a token is hallucinated or not by comparing logits under real vs. corrupted input. This is essentially what the causal grounding track computes.

**Idea:** Treat contrastive decoding as the baseline grounding signal. Then show that adding state and decision grounding on top provides additional discriminative value.

**Extension:** Can we design a training-free intervention (based on current grounding work) that improves downstream grounding scores? And then, can the grounding signal be used as a training signal?

**Status:** `causal_delta_logp_random` (AUC 0.7667 on POPE-1K) is already essentially a contrastive decoding metric. The question is whether this becomes a formal baseline comparison in the paper.

---

## H-D: Teacher-Forced Formulation Concerns

**Open question:** Is token-level grounding the right unit of analysis, or should we focus on object-level grounding?

**Specific concerns:**

1. Teacher forcing isolates token-level evidence — but is this the most meaningful granularity?
2. What if we focus on how the probability of *some* tokens changes when we remove all priors (language prior + image)?
3. Could we model generation as a **trajectory in some latent space**? Then grounding becomes: how much does that trajectory change when we perturb initial conditions (text priors vs. image tokens)?
4. Teacher forcing may be best understood as a way to isolate evidence, not as a complete grounding theory.

**Status:** Conceptual — no experiments. Teacher forcing is baked into the current pipeline. Changing this would require a significant scope extension.

---

## Prioritization

| Hypothesis | Connection to AAAI paper | Effort | Priority |
|---|---|---|---|
| H-A: Support vs bounding box patches | High — directly extends Experiment C in [[10_paper/PAPER_TRACK_FROZEN_v2.md|PAPER_TRACK_FROZEN_v2]] | Medium | **High** |
| H-B: Spatial structure in support row | Medium — improves Step 3 metrics in spatial protocol | Low-Medium | **Medium** |
| H-C: Contrastive decoding baseline | High — strengthens causal track framing | Low | **High** |
| H-D: Teacher forcing critique | Low for AAAI (scope change) | High | Low (future work) |
