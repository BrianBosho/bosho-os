---
title: Literature → Method Development (developmental pass)
type: paper-notes
created: 2026-06-17
tags: [paper, aaai, grounding, vlm, methodology, literature]
status: active
---

# Literature → Method Development

A **developmental** reading of the literature (not a defense). The track is not frozen. For each of four threads we ask: what does the literature actually say, how do we operationalize it in *our* instrument, what does it change in the method or contributions, and what design decision is still open.

Priority order (as agreed): **1. Sufficiency · 2. Layer reconsideration · 3. Free-form / PNG arm · 4. Token-position decay.**

> **Neighbor alert (read first).** A very recent paper is close to the free-form + token direction: *"Beyond the Global Scores: Fine-Grained Token Grounding as a Robust Detector of LVLM Hallucinations"* (arXiv 2604.04863, Apr 2026). It already uses **per-token grounding** as a hallucination detector, labels object-token spans (excluding function words), and introduces an **Attention Dispersion Score** and **Cross-modal Grounding Consistency**. This overlaps threads 3 and 4. It is both a resource (their labeling pipeline and metrics) and a novelty pressure point — our counterfactual null + causal-necessity angle is what they lack. Verify its exact claims before building on or around it.

---

## Thread 1 — Sufficiency (two-sided faithfulness)  [do it; easy]

**What the literature says.** ERASER (DeYoung et al., 1911.03429) pairs two erasure metrics, and they are not interchangeable:

- **Comprehensiveness** — remove the top-k important features; a faithful attribution produces a *large* probability drop (the features were *necessary*). This is what our causal track already computes.
- **Sufficiency** — keep *only* the top-k features (remove everything else); a faithful attribution produces a *small* drop, i.e. those features alone are *enough* to sustain the prediction.

In vision this is the **insertion/deletion** game (Petsiuk et al., 2018): deletion ≈ comprehensiveness (AUC should be low), insertion ≈ sufficiency (AUC should be high). Both are reported as area-under-curve over a sweep of k. The standard warning (ROAR, 1806.10758; and the insertion/deletion literature) is that hard removal with a **zero/black baseline pushes inputs out of distribution**, distorting the measurement; a blurred or distribution-matched baseline is preferred.

**Operationalization for us.** We already have the machinery — sufficiency is the mirror image of the ablation we run:

1. *Comprehensiveness (have):* replace top-k concept-profile patches with N0 (dataset-mean), measure Δlog p. Already `cau_rel_drop`.
2. *Sufficiency (add):* replace **all but** the top-k patches with N0, measure Δlog p. Small drop = the support patches are sufficient.
3. Report both as a curve over k (k = 1, 2, 4, 8, 16, 32) → an **insertion/deletion AUC pair** per sample, not a single-k number.
4. Keep the matched-random control on *both* sides (random keep-k vs. concept keep-k).

**What it changes.**
- *Method:* the causal track becomes the **complete attribution-faithfulness pair** (necessity *and* sufficiency) instead of a one-sided necessity test. This is the standard interpretability community expects, so it is strictly stronger.
- *Contribution:* upgrades Contribution 3 from "attributed patches are necessary" to "attributed patches are necessary **and** sufficient under a distribution-matched null."
- *Free win on the OOD critique:* our N0 dataset-mean patch is already an in-distribution baseline, which is exactly the fix the insertion/deletion literature recommends over black/zero masking. State this explicitly — it pre-empts the ROAR objection without retraining.

**Open decision.** Sweep granularity (how many k points) and whether sufficiency is reported per-sample AUC or at a fixed operating k for the headline table. Lean: AUC for the appendix, fixed-k for the main table.

**Cite:** ERASER (1911.03429), Petsiuk insertion/deletion (2018), ROAR (1806.10758).

---

## Thread 2 — Layer of measurement  [investigate; potentially design-changing]

**What the literature says — and it pushes on our L32-only choice.** A consistent picture across recent VLM interpretability work:

- VLMs process vision in **two stages**: *visual enrichment* (early/mid layers move image features into token positions) then *semantic refinement* (late layers reinterpret through language). Source: *Towards Interpreting Visual Information Processing in VLMs* (2410.07149).
- **Grounding signal is richest in the middle, and is suppressed toward the output.** *Devils in Middle Layers* (2411.16724) interprets, detects, and mitigates object hallucination specifically via **middle-layer** attention. Logit-lens object decoding peaks mid-to-late (e.g. ~layer 25/29), not at the final layer.
- **Visual attention degrades as the decoding layer deepens** — later layers involve visual tokens less (same finding echoed in the attention-decay papers under Thread 4).
- ContextualLens / *Beyond Logit Lens* (2411.19187) computes **cosine similarity between answer-token embeddings and image-patch embeddings at middle layers** — which is essentially our **state track**, but mid-layer and without a null subtraction.

**Why this matters for us.** Measuring only at L32 (final) means we read the signal *after* semantic refinement has folded vision into language — i.e. the **most degraded** version of the grounding signal. Two consequences:

1. The L32-only choice may be *under-powering* the state track. ContextualLens gets its grounding from middle layers for exactly this reason.
2. More interestingly, the **middle→final loss of grounding is itself a candidate measure**, and it lines up with the paper's headline idea. "Right for the wrong reason" plausibly *is* a case where grounding was present mid-stack and got overwritten by the language prior before L32. A `state_grounding(L16) − state_grounding(L32)` differential would operationalize that directly.

**Operationalization for us.**
- *Cheap diagnostic first:* recompute the state track (and the decision/causal tracks where feasible via logit lens) at a small ladder — L8, L16, L24, L32 — on the existing POPE extraction. Plot grounding vs. layer for `hallucinated_yes` vs. `correct`. This is a few hours of re-reading cached activations, no new generation.
- *If the differential separates the classes:* promote a **mid-vs-final grounding-loss** measure to a candidate track and test its AUC against the current L32 measures.
- *Either way:* the layer ladder answers the reviewer-and-design question "why L32?" with evidence instead of assertion. Right now L32 is frozen by fiat (PAPER_TRACK design table) and listed as a limitation; the literature says that choice is non-obvious and possibly suboptimal.

**What it changes.**
- *Method:* potentially moves the primary measurement layer, or adds a cross-layer differential measure. This is the one thread that could genuinely alter the design, so do the cheap diagnostic before freezing the layer.
- *Risk / tension:* the project's stated scope explicitly excludes layer-traversal analysis (PAPER_TRACK "what this is not"). The literature is pushing back on that exclusion. Decision needed: keep L32-only and cite the layer literature as a *justified* limitation, or admit a minimal two-layer (mid + final) measurement because the evidence says the final layer is the wrong place to look. Recommend at least running the diagnostic before deciding — it's too cheap not to.

**Cite:** Towards Interpreting Visual Information Processing (2410.07149), Devils in Middle Layers (2411.16724), Beyond Logit Lens (2411.19187), Hidden in Plain Sight (2506.08008).

---

## Thread 3 — Free-form / exhaustive-label arm  [resolves per-token honesty gap; adds a dataset]

**Correction to the earlier plan.** I previously called Panoptic Narrative Grounding "exhaustively annotated." That is **not quite right and matters.** PNG grounds only a **subset** of phrases: 726k noun phrases over COCO, but it covers **47.5% of COCO panoptic segments** and **45.1% of Localized-Narrative noun phrases** — on average only **5.1 of 11.3** noun phrases per caption are grounded (2109.04988). So PNG's *phrase-grounding layer is partial* and would re-introduce the exact partial-labeling trap we are trying to avoid.

**What is actually exhaustive** is the layer underneath PNG: **COCO panoptic segmentation** labels *every pixel* (every thing + stuff instance). That is the clean substrate. So:

- Use **COCO panoptic instance labels** as the exhaustive object inventory: "object token not in the panoptic label set" reliably means "not in the image."
- Use **PNG** for the *phrase→region* supervision where we want to check that our high-support patches land on the right region (spatial-correspondence validation), accepting its partial coverage there.

**Operationalization for us (a real per-token result, not an asserted one).**
1. Generate free-form captions on a COCO val subset with LLaVA-1.5-7B.
2. Label object tokens. The field standard (per 2604.04863 and the CHAIR-style pipeline) is to align generated object nouns to the ground-truth object list, marking each correct/hallucinated; function words excluded. Use COCO panoptic labels as the inventory so "absent" is trustworthy. A GPT-4o-assisted labeling pass with the image + panoptic object list is the common practice for span-level labels.
3. Run the instrument (state / decision / causal, with the Thread-1 sufficiency addition) on each labeled object token.
4. Evaluate exactly as Experiment A, but now on **genuinely generated tokens**: does grounding separate hallucinated-object tokens from correct-object tokens in free-form output?
5. Optional spatial check: do top-k support patches overlap the PNG/panoptic region for that object (IoU)?

**What it changes.**
- *Honesty of the claim:* turns "per-token instrument (validated on one yes/no token)" into "per-token instrument validated on free-form generated object tokens." This is the CQ5 fix done properly.
- *Contribution:* adds a **second dataset and a second task** (generation, not just discrimination), broadening the paper past POPE-only — a frequent reviewer ask.
- *Connects Thread 4:* once we have per-token scores over a generated sequence, the decay experiment (below) is free.
- *FaithScore (2311.01477)* gives the atomic-decomposition principle if we later want attributes/relations, not just objects — but objects-against-panoptic is the clean first version.

**Open decision.** How much of this is a *headline* experiment vs. a *qualitative illustration*. Minimum viable: a small labeled set (50–100 captions) for a qualitative + small-quantitative result. Full version: a few hundred captions for a real AUC. The minimum already removes the "you never actually score generated tokens" objection.

**Cite:** PNG (2109.04988, with the coverage caveat), COCO panoptic, CHAIR (1809.02156), FaithScore (2311.01477), Beyond the Global Scores (2604.04863).

---

## Thread 4 — Token-position decay (external-validity test)  [free once Thread 3 exists]

**What the literature says — and it's robust.** A well-replicated phenomenon:

- **Conditioning dilution / "fading memory":** as more tokens are generated, reliance on the image drops; M3ID (2403.14003) builds its entire decoding correction on this, scaling its image-amplification coefficient *up* as generation proceeds.
- **Visual attention declines with sequence position**, and **hallucinated tokens cluster later** and in low-attention positions: TARAC (2504.04099), IKOD (2508.03469), The Hidden Life of Tokens (2502.03628), Dual-Level Attention Intervention (2506.12609). The same papers note attention to vision *also* declines with layer depth — which ties back to Thread 2.

**Operationalization for us.** This is a validation experiment the instrument should *pass* if it measures what we claim:

1. On the Thread-3 free-form captions, plot per-token grounding score vs. token position (and vs. object-mention index).
2. **Prediction:** grounding decreases with position. If it does, the instrument independently recovers a phenomenon established by an entirely different method (attention/MI analysis) — strong **external validity**.
3. **Sharper prediction:** within a caption, the *drop* in grounding from early to late mentions should be larger for captions that end in hallucination. This links decay to the failure directly.
4. Cheap robustness: confirm the decay is not an artifact of token type by controlling for V/A/F token class (you already plan the token-selectivity annotation).

**What it changes.**
- *Contribution:* a new, low-cost validation result — "the instrument reproduces the known visual-conditioning decay" — that costs almost nothing once Thread 3 produces per-token sequences. Good for the Method/internal-validation section.
- *Caution:* because decay is already well documented, frame this as **convergent validation of our instrument**, not as a new discovery about VLMs. The novelty is that an *internal counterfactual* recovers it, not that decay exists.

**Cite:** M3ID (2403.14003), TARAC (2504.04099), IKOD (2508.03469), Hidden Life of Tokens (2502.03628), Dual-Level Attention Intervention (2506.12609).

---

## Cross-thread synthesis

The four threads are not independent — three of them compound:

- **Thread 3 unlocks Thread 4** (per-token sequences make decay free) and supplies the substrate for a spatial-correspondence check (PNG/panoptic IoU).
- **Thread 2 connects to Thread 4** through the shared finding that visual involvement decays with *both* layer depth and token position — a mid-vs-final differential and a position decay are two cuts of the same underlying suppression.
- **Thread 1 is standalone and immediate** — do it now regardless of the others.

**Suggested execution sequence given the above:**
1. **Thread 1 sufficiency** — implement on existing POPE causal pipeline (days).
2. **Thread 2 layer ladder diagnostic** — re-read cached activations at L8/16/24/32; decide layer question from data before freezing (days, no new generation).
3. **Thread 3 free-form arm (minimum viable)** — 50–100 captions, panoptic-labeled object tokens, run instrument (week).
4. **Thread 4 decay** — read off the Thread-3 sequences (hours).

**Two things to verify before building:**
- The exact metrics and claims of **Beyond the Global Scores (2604.04863)** — closest neighbor on the token/free-form axis; confirm what is left for us (the counterfactual null + causal necessity + the correct-but-ungrounded failure mode).
- The **VAUQ** core-region-masking detail (still unverified) — its masking is a *targeted spatial* null, the closest thing in the literature to what our concept-profile + ablation does at the input. Worth a direct comparison once confirmed.
