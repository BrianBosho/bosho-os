---
title: AAAI Paper Track
type: paper-track
created: 2026-06-16
tags: [paper, aaai, grounding, vlm]
---

# AAAI Paper Track

**Target:** AAAI 2027 (deadline July 21, 2026)
**Based on:** `PAPER_TRACK_FROZEN_v2.md`

---

## Paper claim

> We introduce a training-free, per-token instrument that measures whether a VLM's generated tokens are genuinely supported by visual evidence — distinguishing image-conditioned answers from prior-driven answers that happen to be correct.

---

## What this paper is

A **measurement paper**. It defines an instrument, validates that the instrument produces a meaningful signal, and shows that the signal reveals a failure mode that output-level evaluation misses.

The core insight is that correctness and grounding are different things. A model can be correct because the image supported the answer, or correct because a language prior happened to agree with the ground truth regardless of the image. Behavioral benchmarks cannot distinguish these two cases. This paper provides a method that can.

---

## What this paper is not

The following ideas are **explicitly out of scope** for this paper. Each is a legitimate research direction, but none enters this paper:

- Pipeline information flow (CLIP encoder → projector → LLM): how much visual information survives each stage
- Layer-traversal grounding analysis: computing grounding signals at L8, L16, L24
- Patch logit lens: decoding patch embeddings through the LM head
- Spatial structure analysis: 2D statistics on the 24×24 patch grid
- Bounding-box localization as a headline claim
- Training-based methods or fine-tuning
- Models other than LLaVA-1.5-7B
- Benchmarks other than POPE as the primary evaluation
- The smearing hypothesis and the localization ladder (future paper)

These ideas live in `VLM Ideas Developed.md`. They do not reopen this document.

---


---


---

## Research questions

**RQ1 — Measurement.** Can visual grounding be measured directly from internal activations and token probabilities using a real-vs-null counterfactual protocol?

**RQ2 — Utility.** Can intrinsic grounding scores distinguish grounded answers from hallucinated or prior-driven answers?

**RQ3 — Added value.** Does the grounding signal reveal a failure mode that ordinary accuracy and confidence miss?

RQ1 is foundational. RQ2 and RQ3 are independent of each other and both depend on RQ1.

---

## Method

### The object we measure: the real-vs-null counterfactual

The paper measures one quantity per generated token: the **image-attributable change in the model's commitment to that token**. This counterfactual is the methodological core and the basis of the contribution; the specific measures below are operationalizations of it that we are still exploring.

Hold the prompt and token sequence fixed. Replace the real image with a content-free null baseline (the dataset-mean CLIP patch across COCO validation). Measure how internal states and output probabilities change. Any measurable change is attributed to visual content.

The counterfactual subtraction is necessary because raw similarity between hidden states and patch embeddings has a non-zero floor driven by embedding anisotropy. The null-image pass removes this background, isolating the image-specific signal.

### Operationalizing the signal: candidate measures (exploratory)

We are still exploring how best to read the image-attributable change. We currently track three complementary operationalizations of the signal below. These are **candidate measures under active exploration** — not a settled decomposition, and the paper does **not** claim the three-way split itself as a contribution. We expect to narrow toward the most discriminative and causally grounded measure(s) as evidence accumulates; for now the list stays open.

**Track 1 — State grounding.** Did the real image shift the token's Layer-32 hidden state toward specific patch directions?

The measure is the spatial variance of the cosine-delta row: how concentrated (vs. diffuse) is the image-induced shift across patch positions?

**Track 2 — Decision grounding.** Did the real image change what the model chose to generate?

The measure combines the probability shift with a spatial concentration term: `dec_dp_x_cvar = Δp_t × Var_j(concept_profile_j)`. The spatial term penalizes probability shifts that are not attributable to specific patches — filtering out diffuse or prior-driven shifts.

**Track 3 — Causal grounding.** Are the attributed patches actually necessary for the prediction?

The top-k patches ranked by the concept profile are ablated. The measure is the log-probability drop compared to a matched random ablation of the same cardinality. This moves from correlation to causal necessity.

### Design decisions

| Decision | Choice | Why |
|---|---|---|
| Layer | 32 (final) | Grounding suppressed at L32 cannot influence output |
| Null | Dataset-mean CLIP patch (N0) | Removes semantic content; preserves CLIP distribution |
| Concept conditioning | ×cvar product | Filters diffuse probability shifts |
| Space | Raw Layer-32, no whitening | Empirically superior for the primary evaluation target |
| Random controls | K=3 matched random masks | Required for causal specificity |

---

## Experiments

### Experiment A — Benchmark discrimination

**Question:** Can intrinsic grounding scores distinguish hallucinated answers from correct answers?

**Setup:** POPE official adversarial 1K. Primary target: `hallucinated_yes` vs. `correct` responses. Compute three-track metrics under teacher-forced extraction. Evaluate ROC-AUC.

**What makes this interesting:** The champion metric combines a contrastive probability signal with a spatial concentration term. The key comparison is whether this outperforms a simple log-probability ratio — which it does, because the ratio carries no spatial information and cannot distinguish causally necessary patches from diffuse correlational signals.

**Key baseline to address:** `dec_log_p_ratio` achieves strong scalar discrimination. The paper must argue concretely (with worked examples) why the full instrument adds value over this baseline.

### Experiment B — Causal validation

**Question:** Are the patches identified by the instrument causally necessary, or merely correlated with the prediction?

**Setup:** POPE-200 subset. Targeted ablation (top-k concept-profile patches) vs. matched random ablation of the same cardinality. Report mean drop difference with significance test and effect size.

**What this shows:** The instrument does not just identify patches that are statistically associated with the answer — it identifies patches whose removal changes the prediction.

### Experiment C — Beyond-accuracy validation

**Question:** Among correct answers, does the grounding score predict sensitivity to evidence removal?

**Setup:** Take all correct POPE answers. Split into low-grounding (bottom quartile of `dec_dp_x_cvar`) and high-grounding (top quartile). For each, ablate the support patches and measure log-probability drop, answer persistence rate, and answer flip rate.

**Prediction:** Low-grounding correct answers degrade less under evidence removal than high-grounding correct answers, because they were never depending on the image in the first place.

**Why this matters:** This is the paper's most novel claim. It shows the instrument identifies a failure mode invisible to accuracy metrics: correct but visually unsupported answers. A model that gets the right answer for the wrong reason is not reliable.

---

## Paper structure

| Section | Content |
|---|---|
| 1. Introduction | Grounding ≠ correctness. "Right for the wrong reason." Paper claim and contributions. |
| 2. Related work | VCD/M3ID (intervention), EigenScore/HaloScope (detection), attention methods. |
| 3. Method | Null construction, teacher forcing, candidate grounding measures, core metrics, design decisions. Internal validation: token selectivity and convergent validity across measures. |
| 4. Experimental setup | LLaVA-1.5-7B, POPE, evaluation targets, baselines, result-line distinction. |
| 5.1 Benchmark discrimination | Experiment A. ROC curves, AUC table, baseline comparison, worked examples. |
| 5.2 Causal validation | Experiment B. Targeted vs. random ablation, significance, effect sizes. |
| 5.3 Beyond-accuracy validation | Experiment C. Evidence removal on correct cases, degradation analysis. |
| 6. Discussion | What the instrument measures and does not. The ratio-baseline question. Cross-track interpretation. |
| 7. Limitations | Single model, POPE-centric, teacher-forcing, L32 only, region-not-pixel resolution. |
| 8. Conclusion | — |

Target: ~12 pages + references + appendix.

---

## Contributions

1. A training-free, per-token method for measuring visual grounding in VLMs, based on a real-vs-null counterfactual protocol that isolates the image-attributable change in a token's commitment. *(We explore several operationalizations of this signal; the contribution is the counterfactual measurement approach itself, not a specific three-way decomposition.)*

2. Empirical demonstration that the instrument detects hallucination from internal signals alone, with the contrastive component driving the large majority of detection performance over raw model confidence.

3. Causal validation that attributed patches are genuinely necessary for the model's predictions — targeted ablation produces significantly larger probability drops than matched random ablation.

4. Evidence that the instrument identifies a failure mode invisible to accuracy metrics: correct answers with low grounding scores degrade less under evidence removal, indicating they were never visually supported.

*(Contribution 4 is conditional on Experiment C.)*

---

## Internal validation (Method section, not standalone results)

Two checks belong in the Method section as instrument validation:

**Token selectivity:** The instrument should score visual nouns higher than visual attributes, which in turn should score higher than function words. This validates that the instrument is sensitive to semantic content, not just to token position or language-model confidence.

**Convergent validity across measures:** Report Spearman ρ between the candidate measures (state, decision, causal). Strong agreement is convergent-validity evidence that they capture one underlying construct (visual grounding); partial divergence indicates they capture complementary aspects and helps us select among them. Either outcome is informative while the signal is still being narrowed down.

---

## What to set aside (from VLM Ideas)

The ideas developed in `VLM Ideas Developed.md` that are closest to this paper but do not enter it:

**Pipeline information flow (Idea 1)** is important for understanding *why* the instrument measures what it does, but the paper does not need to characterize CLIP encoder or projector behavior. That is a future paper.

**Earlier layers (Idea 2.2)** — the paper measures at L32 only. This is a named limitation. The observation that grounding at earlier layers may be suppressed before reaching L32 is captured in the Discussion.

**Patch logit lens (Idea 3)** — an interpretable patch-selection method that decodes patch embeddings through the LM head. Promising but not needed for the three defined experiments. Mention as future work.

**Semantic direction basis / concept profile (Idea 3, basis variant)** — building a basis of semantic directions from CLIP patch projections and embedding-matrix samples, with a matched **null basis** subtracted, to quantify *what* semantic content a measure picks up (e.g. dog vs. cat) and to define interpretable concept-profile directions. **We are tracking this as a concept of interest and a candidate construction for the concept profile.** It is not in the core method for this submission: it needs validation that it separates known categories above the null basis. Revisit for inclusion in a later revision or as future work.

**Smearing hypothesis and localization ladder (Idea 1)** — directly addresses the H-A cascade question (do bounding box patches correspond to support patches across pipeline stages?). This is a follow-on paper once the core instrument paper is submitted.
