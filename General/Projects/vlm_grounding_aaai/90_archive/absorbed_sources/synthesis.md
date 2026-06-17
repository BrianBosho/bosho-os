---
title: VLM Ideas — Synthesis Against the Vault
type: research-synthesis
created: 2026-06-16
tags: [research, vlm, grounding, ideas, synthesis]
---

# VLM Ideas — Synthesis Against the Vault

This document maps the three idea categories in `unprocessed/VLM Ideas.md` against the existing vault. For each idea, it shows what is already addressed, what is genuinely new, and where the clearest development paths lie.

---

## Overview of the VLM Ideas structure

The unprocessed note has three nested question groups:

1. **Pipeline information flow** — how much visual information exists at each stage (CLIP encoder → projector → LLM)?
2. **LLM dependence on visual input** — how much does the LLM use visual evidence when generating an answer?
3. **Measurement design** — how do you quantify and evaluate the visual information?

These are not three separate research threads. They are three levels of the same question, each operating at a different abstraction: *where does visual information live, how much of it is used, and how do you measure that use?*

---

## Idea 1: Pipeline information flow

### What the note asks

- How much visual information is in the CLIP encoder output?
- How much of that survives the projector?
- How does the LLM process what it receives to generate an answer?

### What the vault already has

The current paper (`PAPER_TRACK_FROZEN_v2.md`) answers a narrower version of this question: it measures image-conditioned behavior at **Layer 32** of the LLM only. Layer 32 is the final LLM layer before the unembedding — the stage where suppression of a grounding signal has no downstream influence on the output. That is the paper's design choice, not a measurement of the full pipeline.

The limitation is explicitly stated: "Grounding at earlier layers that gets suppressed is not captured."

### The key connection: H-A cascade experiment

`OPEN_HYPOTHESES.md` contains a directly relevant proposal under **H-A: Support Patches Do Not Correspond to Bounding Box Patches at Layer 32**. The cascade component of H-A is a precise experimental design for the pipeline-information question:

> Ablate at LLM Layer 32 → ablate at projector output → ablate at CLIP encoder → ablate at pixel level.
> The point where bounding box ablation begins to match support patch ablation is where information dispersion starts.

This is the "localization ladder" that answers Idea 1 empirically. The cascade does not measure information quantity directly, but it identifies *where* visual information becomes non-localized — which is an operationally meaningful version of the pipeline-information question.

### What is genuinely new in Idea 1

The VLM Ideas note frames the question **information-theoretically** rather than causally. Asking "how much information" (rather than "does ablation matter?") implies measuring something like mutual information or entropy at each stage — not just whether removing a stage changes output.

This is a different and harder question than what H-A tests. It connects to:
- CKA-based analysis of representational similarity between CLIP output and LLM hidden states (mentioned in Phase 2 Notes under F5)
- The broader mechanistic interpretability direction (Direction E in the Synthesis doc)

### Development path

For the **AAAI paper**: The pipeline question enters as a limitation and as the framing motivation for H-A (if H-A runs). The cascade result answers "where does localization break down?" which is a partial answer to "how much information survives the pipeline?"

For **follow-up work**: A full information-flow study would require measuring representational alignment (CKA, RDM) between each stage's output and the ground-truth spatial annotation. This is a dissertation-scale contribution.

---

## Idea 2: LLM dependence on visual input

### What the note asks

2.1 Checking representational similarity between hidden states of generated tokens and image patch hidden states at Layer 32.

2.2 Whether earlier layers need to be inspected for representational similarity.

2.3 Counterfactuals: can we identify support patches? Can we change them?

### What the vault already has

**Idea 2.1 is state grounding.** The cosine delta matrix:

```
Δ[t,j] = cos(H^r_t, V_j) − cos(H^0_t, V_j)
```

directly measures representational similarity between the generated token's hidden state and each image patch vector at Layer 32, under a real-vs-null subtraction that removes the anisotropy floor. The key aggregated metric is `state_delta_var` — spatial variance of this delta row. This is already implemented, run on POPE-1K, and included in the paper as Track 1.

**Idea 2.2 (earlier layers)** is the Layer 32 limitation. The paper explicitly does not inspect earlier layers. H-A's cascade partially addresses this by testing ablation effects at earlier pipeline stages.

**Idea 2.3 (counterfactuals, support patches)** is split across two tracks:
- *Can we identify support patches?* → The concept profile (top-k patches ranked by Track 2 decision signal) is the instrument's answer. The patches with highest `dec_dp_x_cvar` contribution are the "support patches."
- *Can we change support patches and measure the effect?* → That is **Experiment C** in `PAPER_TRACK_FROZEN_v2.md` — the paper's highest-priority unfinished experiment. Experiment C ablates support patches for *correct* answers and measures how much degradation follows. The key prediction: low-grounding correct answers should degrade less, because they never depended on the image.

### What is genuinely new in Idea 2

The note implicitly asks whether representational similarity at **Layer 32** is sufficient or whether earlier layer analysis is needed. The Phase 2 Notes raise exactly this concern: kernel sensitivity and the difficulty of distinguishing informative from null patches at Layer 32 may indicate that the relevant grounding signal is smeared across layers before reaching Layer 32.

The **new synthesis insight** here is that 2.1 and 2.2 together motivate a layer-traversal version of state grounding: compute `state_delta_var` at multiple LLM layers (e.g., L8, L16, L24, L32) and ask at which layer the signal is strongest. If the signal peaks well before L32, that suggests information is being used earlier and then attenuated. This would directly answer "do we need earlier layers?" — and it does not require the full H-A cascade.

### Development path

For the **AAAI paper**: 2.1 and 2.3 are both in the paper. 2.2 is a limitation. No new work needed to address these as paper content.

For the **open hypotheses**: H-A (cascade) partially answers 2.2. A layer-traversal state grounding analysis (compute `state_delta_var` at L8/L16/L24/L32) could be a low-cost addition to the discussion section if results are available.

---

## Idea 3: Measurement design

### What the note asks

3.1 Can we measure the amount of **semantic information**? For example, can we quantitatively distinguish an image of a dog from an image of a cat?

3.2 A basis was constructed using samples from the embedding matrix or from CLIP projections of a dataset: hidden states and embeddings are projected there to check if basis directions represent semantic information directions.

3.3 What is the best way to determine a basis and null basis?

### What the vault already has

**Idea 3.1 (semantic information measurement)** is addressed by **H2: Token Selectivity**. H2 tests whether the grounding instrument scores visual nouns (V) higher than visual attributes (A), which in turn score higher than function words (F), at p < 0.01. The passing criterion (V/F ratio ≥ 2.0) is a quantitative check that the instrument is sensitive to semantic content direction. H2 has not yet been run — it requires ~4 hours of manual annotation on 100 POPE samples and is blocking the paper.

**Idea 3.2 (basis construction from embedding matrix or CLIP projections)** maps directly to the null baseline design. The N0 null (dataset-mean CLIP patch across COCO validation) is a specific instance of constructing a null basis from a dataset of CLIP projections. The embedding matrix approach was explored in the V3/V3A/V3B branch (using lm_head weights as a semantic basis) but was archived as empirically unstable. N0 won the null ablation (Stage A):

| Null | `dec_dp_x_cvar` AUC |
|------|---|
| N0 (dataset-mean patch) | 0.885 |
| N1 (per-image-mean) | 0.735 |
| N2 (white noise) | 0.743 |
| N3 (patch shuffle) | 0.515 |

N3 and N4 are structurally invalid nulls. N0 is the canonical choice.

**Idea 3.3 (best basis and null basis)** is answered. The empirical answer is N0, and the rationale is that N0 removes semantic content while preserving the statistical distribution of visual features in CLIP space — keeping the null within the learned distribution avoids introducing artifacts from out-of-distribution inputs.

The anisotropy concern that motivated the counterfactual subtraction is also addressed: raw cosine alignments have a non-zero floor even for textual tokens because of embedding anisotropy. Subtracting the null-image pass isolates the image-specific signal by removing this background.

### What is genuinely new in Idea 3

The note's framing of "can we tell quantitatively that one image has dog and another has cat?" is more ambitious than what N0 or H2 test. It implies a **per-image semantic content measure** — not just whether the instrument respects semantic ordering across tokens, but whether it can identify *which* semantic concept is present.

This is adjacent to two things in the vault:
- The concept profile (which identifies *which* patches carry the grounding signal per token) could, in principle, be decoded back to semantic content if the patch embeddings are interpretable. This is essentially the "patch logit lens" idea mentioned in Phase 2 Notes.
- The V3/V3A/V3B branch attempted something like this by projecting into lm_head space to check semantic directions — but this was archived as empirically fragile.

The cleaner path is the **patch logit lens**: project each patch's CLIP embedding through the LM head to see what tokens decode most strongly. Patches that decode to dog-related tokens in an image with a dog would confirm that the basis captures semantic directions. This remains an open idea and is mentioned in Phase 2 Notes ("patches that decode to clearly meaningful words may provide a more surgical evaluation anchor").

### Development path

For the **AAAI paper**: 3.2 and 3.3 are answered. 3.1 is partially answered by H2 (run it). The patch logit lens idea is a discussion-section note or future work item.

For **follow-up**: The full "how much semantic information?" question would require a more systematic comparison of patch decodings across images, connecting the grounding instrument to interpretability methods (logit lens, direct logit attribution).

---

## Cross-cutting synthesis

### The two framings are complementary

The VLM Ideas note has an implicit framing: **pipeline-theoretic** — what information exists and survives at each stage? The current paper has a different framing: **decision-theoretic** — does the model's decision counterfactually depend on visual evidence?

These are not competing framings. They answer different questions:
- Pipeline-theoretic: *does the information reach the LLM?*
- Decision-theoretic: *does the LLM use the information that reaches it?*

A model could receive visually grounded patch representations but ignore them (prior-driven correct answers). A model could also lack good CLIP representations but still appear grounded by language-prior agreement. The paper captures the second failure mode directly (via the "beyond-accuracy" Experiment C). The pipeline framing would add a diagnosis of the first.

### Where the ideas connect to execution priorities

| VLM Idea | Vault status | Next step |
|---|---|---|
| Visual info at CLIP output | Not in paper (Direction E) | Future work / dissertation chapter |
| Visual info through projector | H-A cascade (open hypothesis, medium priority) | Run H-A cascade after Experiment C |
| How LLM processes visual info | State + decision + causal tracks (paper) | Run H2, cross-track convergence |
| Representational similarity at L32 | State grounding, implemented and run | Confirm with cross-track Spearman ρ |
| Earlier layers needed? | Layer 32 limitation + H-A | Note in limitations; H-A as follow-on |
| Support patch identification | Concept profile / causal track | Finalize H3 significance stats |
| Changing support patches | Experiment C (❌ not yet run) | **Highest priority — blocks paper** |
| Semantic info quantification | H2 token selectivity (not yet run) | Annotate 100 POPE tokens (~4h) |
| Basis from CLIP projections | N0 null (done, validated) | No action needed |
| Best null basis | N0 confirmed by null ablation | No action needed |
| Patch logit lens for semantic directions | Open idea, not in paper | Future work or discussion note |

### One new experiment worth adding

The layer-traversal state grounding analysis (compute `state_delta_var` at L8, L16, L24, L32) is a new idea not explicitly in the vault that directly answers Idea 2.2. It requires no new data — the extraction pipeline would need to output hidden states at multiple layers rather than just L32. If the signal is concentrated at early layers, it strengthens the "information is used early, not late" story. If it is concentrated at L32, it confirms the paper's design choice. Either outcome is informative.

This could be added to the Discussion section as a post-hoc analysis on a small subset (20–50 POPE samples) without threatening the frozen paper track.

### One framing development worth capturing

The VLM Ideas note's core framing — *measuring the amount of visual information* at each stage — is a useful way to position the paper's contributions to a mechanistic interpretability audience. The paper currently positions itself as a hallucination-detection instrument. An alternative positioning is: "a training-free instrument for measuring how much visual evidence a VLM actually uses when generating a token." This reframing (measurement-first rather than detection-first) may be more durable and harder to dismiss as "just another hallucination detector."

This reframing is compatible with the current paper — it does not require new experiments. It connects the detection results (Experiment A), token selectivity (H2), and beyond-accuracy validation (Experiment C) into a measurement story rather than a detection story.

---

## Recommended immediate actions

1. **Run Experiment C (Approach 1)** — this is the highest-priority paper-blocking item and directly addresses the "can we change support patches and measure the effect?" question from Idea 2.3.

2. **Run H2 token selectivity** — 4 hours of annotation. This answers the "can we measure semantic information quantitatively?" question from Idea 3.1 and is a paper requirement.

3. **Add patch logit lens as a discussion note** — check whether top support patches decode to semantically relevant tokens for the target question. This is a 1–2 hour analysis that directly addresses Idea 3.1 in a richer way than H2 alone.

4. **Layer-traversal state grounding on 20–50 samples** — run `state_delta_var` at L8/L16/L24/L32 on a small subset. This answers Idea 2.2 cheaply and either confirms or challenges the Layer 32 design choice.

5. **Keep H-A cascade as a post-AAAI priority** — it answers the full pipeline-information question (Idea 1) and connects to a future paper or dissertation chapter.
