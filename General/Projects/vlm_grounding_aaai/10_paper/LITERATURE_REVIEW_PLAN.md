---
title: Literature Review Plan — Question-Driven Map
type: paper-notes
created: 2026-06-17
tags: [paper, aaai, grounding, vlm, literature, plan]
status: active
---

# Literature Review Plan

A question-driven map for the AAAI grounding paper. The point of this document is **not** to list papers — `60_literature/resources.md` already does that. The point is to turn the outstanding issues into a small set of **core questions**, and for each one say: what the question is, why it matters, which papers bear on it, what a *good answer* looks like, and how the answer feeds the paper.

## How to use this document

Each core question (CQ) carries two tags:

- **[DEVELOP]** — the literature should change what we *do*: method choices, experiment design, dataset choice, what we measure. The paper track is **not confirmed**, so these questions can still move the design.
- **[DEFEND]** — the literature settles how we *position*: novelty, baselines, related work, reviewer rebuttals.

Most questions are both. The tag marks the dominant mode.

A question is **closed** when we can write its answer in 3–5 sentences with citations, and that answer survives a skeptical reviewer. Until then it stays open and blocks the section(s) listed under "Feeds."

---

## The seven core questions at a glance

| # | Core question | Mode | Resolves the issue | Feeds |
|---|---|---|---|---|
| CQ1 | What *is* our signal, and is the real-vs-null counterfactual genuinely different from contrastive decoding? | DEVELOP + DEFEND | "Closest signal looks like contrastive decoding. What's new?" | Method, Related Work, Intro |
| CQ2 | How is VLM/LLM self-evaluation done, and is intrinsic grounding a new axis of it? | DEFEND + DEVELOP | "How is VLM/LLM self-evaluation done?"; VAUQ positioning | Intro, Related Work |
| CQ3 | How do prior methods read an internal hallucination/grounding signal, and what should we borrow? | DEVELOP | "How do we get a signal? Is it unique?" | Method (state/decision tracks) |
| CQ4 | What is the prior art on patch attribution and *causal* visual necessity? | DEVELOP | Strengthen the causal track; reviewer-proof ablation | Method (causal track), Exp B |
| CQ5 | Does our per-token claim actually require free-form generation, and how have others evaluated token-level grounding? | DEVELOP | "POPE gives no free-form generation; we do not do token-level grounding" | Claim, Setup, Limitations |
| CQ6 | Which datasets support grounding/hallucination evaluation without false positives from incomplete labels? | DEVELOP | "Partial labels → we wrongly call 2 of 5 a hallucination" | Setup, Exp A/C |
| CQ7 | What are the closest and foundational papers, and exactly how do we differ from each? | DEFEND | "Closest papers to our methodology?"; per-paper review | Related Work, rebuttals |

CQ1, CQ5, CQ6 are the ones that can still **change the paper**. Prioritize them.

---

## CQ1 — The signal and the contrastive-decoding boundary  [DEVELOP + DEFEND]

**The issue.** Our core object is the real-vs-null counterfactual: hold prompt and tokens fixed, swap the real image for a content-free null, measure the change in the model's commitment. A reviewer will immediately say this *is* contrastive decoding (VCD/M3ID subtract a degraded-image distribution from the real one). We need to know precisely where the line is — both to defend novelty **and** to decide whether the method should change to make the line sharper.

**Sub-questions.**

1. What exactly do VCD and M3ID subtract, at what stage (logits vs. hidden states), and for what purpose (better decoding vs. measurement)?
2. Is "contrastive decoding for *generation control*" categorically different from "contrastive subtraction for *measurement / self-evaluation*"? Is intent enough, or do we need a mechanical difference?
3. Our null is the **dataset-mean CLIP patch**, not a noised or blurred image. Does the choice of null (mean-patch vs. Gaussian-noise vs. blur vs. no-image) materially separate us from VCD? Is there a null-choice ablation in the literature we should match or cite?
4. Do any of our three tracks (state, decision, causal) have **no** contrastive-decoding analogue? The causal-ablation track in particular looks unlike decoding — is that our cleanest novelty?
5. Is the spatial-concentration term (`×cvar`, concept profile) the real differentiator, since plain `dec_log_p_ratio` is essentially a contrastive-decoding scalar and the instrument's claim is that the *spatial* structure adds value?

**Candidate literature (have).** Multi-Modal Hallucination Control by Visual Information Grounding (2403.14003); the VCD/M3ID line (referenced in PAPER_TRACK §2 — confirm exact citations); Curing Semantic Drift (2506.21509, decoding referee); Reducing Hallucinations via Latent Space Steering (2410.15778).

**Gaps to search.** Original VCD paper and M3ID paper (get canonical citations + exactly what they subtract); any "contrastive decoding as a diagnostic / detector" rather than a generator; null-image and image-corruption decoding variants; "image-free" or "blind" baseline subtraction.

**What a good answer looks like.** A one-paragraph statement of the form: *"Contrastive decoding subtracts a degraded-image distribution to* steer generation*; we use a single content-free null to* measure*, per token, the image-attributable change, and add two things decoding methods do not have: (a) a spatial concept profile that localizes* where *the image mattered, and (b) a causal ablation test of* whether *those patches are necessary. The scalar log-prob ratio is the part we share with contrastive decoding; we show it is the weakest of our signals."* Plus a decision on whether the null choice needs its own defended ablation (likely yes — the N0–N4 table in the TODO).

**Feeds.** Method §3 (framing of the counterfactual), Related Work §2, Intro contribution statement. **This is the highest-leverage question in the paper.**

---

## CQ2 — VLM / LLM self-evaluation as a field  [DEFEND + DEVELOP]

**The issue.** The project is framed (in resources.md) as "can a VLM evaluate whether its own answer is visually grounded?" We need the map of how self-evaluation / uncertainty / confidence is currently done, so we can say what *kind* of self-evaluation ours is and why it is new. VAUQ is the nearest neighbor and the named primary baseline.

**Sub-questions.**

1. What does VAUQ actually measure — answer correctness, visual dependence, or both — and at what level (output token probabilities, sampled consistency, internal states)?
2. Does VAUQ (or any self-eval method) *localize* visual evidence, or only score image-dependence as a scalar? (If only scalar, our spatial + causal tracks are the gap.)
3. How is LLM self-evaluation done in the text-only world — verbalized confidence, P(True), semantic-entropy / consistency sampling, internal-probe methods (e.g., truthfulness directions)? Which of these have VLM analogues?
4. Is "intrinsic, per-token, image-attributable grounding" a genuinely new axis of self-evaluation, or a re-parameterization of visual-uncertainty?
5. Where can decision-grounding give information that output-level self-eval cannot — specifically the "right for the wrong reason" case where confidence is high and grounding is low?

**Candidate literature (have).** VAUQ (2602.21054) — primary; Uncertainty-Aware Evaluation for VLMs (2402.14418); To See or To Please / visual sycophancy (2603.18373); Hidden in Plain Sight (2506.08008).

**Gaps to search.** LLM self-evaluation canon — verbalized confidence, "Language Models (Mostly) Know What They Know" / P(True), semantic entropy (Kuhn/Farquhar), self-consistency; internal-state truthfulness probes (e.g., representation-engineering / honesty directions); any VLM-specific uncertainty or calibration surveys.

**What a good answer looks like.** A 2×2 placement: axes = {output-level vs. internal} × {scalar score vs. localized + causal}. We show the existing self-eval work clusters in output-level/scalar, and we occupy internal + localized + causal. One crisp sentence on VAUQ: what we reuse, what we challenge (the "what to reuse / what to challenge" note already requested in resources.md immediate tasks).

**Feeds.** Intro (problem framing), Related Work §2.

---

## CQ3 — How others extract an internal signal  [DEVELOP]

**The issue.** "How do we get a signal? Is it unique?" Before defending uniqueness we should harvest the *mechanics* of internal grounding/hallucination signals, because the state and decision tracks are still exploratory (PAPER_TRACK §candidate measures is explicitly open). Borrow good ideas; don't reinvent.

**Sub-questions.**

1. What internal quantities do detection methods read — hidden-state geometry (EigenScore/HaloScope), contextual embeddings (Beyond Logit Lens, 2411.19187), attention mass (What's in the Image, 2411.17491), logit-lens decodes?
2. Which of these are *image-attributable* vs. just *uncertainty* signals? (Most LLM detectors are uncertainty; our counterfactual is image-attribution — possible differentiator.)
3. Is our **state track** (Layer-32 cosine-delta spatial variance) measuring grounding or an embedding artifact (anisotropy)? What do others do to remove the anisotropy floor, and does that validate our null subtraction?
4. What aggregation do others use from sub-word/token to phrase/object level? (Open issue in the internal report; needed if CQ5 pushes us toward generation.)
5. Token-class selectivity (noun > attribute > function word) — has anyone validated an internal grounding signal this way? Gives us a citation for the H2 internal-validation check.

**Candidate literature (have).** Beyond Logit Lens (2411.19187); What's in the Image (2411.17491); Hidden in Plain Sight (2506.08008); Eyes Wide Shut (2401.06209); EigenScore/HaloScope (named in PAPER_TRACK §2 — confirm citations).

**Gaps to search.** EigenScore and HaloScope canonical papers; INSIDE / internal-state hallucination detection; any VLM logit-lens / patch-logit-lens work (note: our own patch-logit-lens is out of scope per the track, but others' versions are citable); subword→phrase aggregation methods for token-level attribution.

**What a good answer looks like.** A "keep / borrow / differentiate" table over internal-signal methods, and a decision on whether any borrowed mechanic should be added to the state or decision track before freezing. Explicit answer to "is the state track real signal or artifact," with the literature-backed justification for the null subtraction.

**Feeds.** Method §3 (state + decision tracks, internal validation), Discussion (cross-track interpretation).

---

## CQ4 — Patch attribution and causal necessity  [DEVELOP]

**The issue.** The causal track (ablate top-k concept-profile patches vs. matched random) is the part *least* like contrastive decoding and may be our strongest novelty (see CQ1.4). It needs to be reviewer-proof: is targeted-vs-random ablation a sound causal test, and what is the prior art?

**Sub-questions.**

1. How do prior works attribute a VLM prediction to image regions — attention rollout, gradient methods, perturbation/occlusion, F-LMM-style attention-to-mask?
2. What is the accepted control for a causal patch-ablation claim? Is matched-random (K=3) sufficient, or do reviewers expect insertion/deletion curves, comprehensiveness/sufficiency metrics (ERASER-style), or ROAR-style retraining caveats?
3. Does ablating CLIP patches at the input have known confounds (distribution shift from masking) that we must address? How do occlusion-based attribution papers handle the "masking creates OOD inputs" critique?
4. Is there spatial-correspondence validation we can cheaply add — do attributed patches overlap ground-truth object regions (RefCOCO / Panoptic Narrative Grounding boxes)? This addresses the report's "need stronger spatial correspondence" open issue.

**Candidate literature (have).** F-LMM (2406.05821); What's in the Image (2411.17491); Panoptic Narrative Grounding (2109.04988); Modeling Context in Referring Expressions / RefCOCO (1608.00272).

**Gaps to search.** Faithfulness-of-attribution / feature-importance evaluation (comprehensiveness & sufficiency, ERASER; insertion-deletion / ROAR); occlusion-OOD critiques; any VLM-specific causal patch-ablation or causal-tracing (ROME-style) work.

**What a good answer looks like.** A defended sentence that our targeted-vs-random ablation is a recognized necessity test, with named precedent for the control, and an explicit note on the masking-OOD confound and how N0/random matching mitigates it. Optional: a decision on whether a small bbox-overlap check is worth adding (the TODO already lists this as optional/Discussion).

**Feeds.** Method §3 (causal track), Experiment B, Limitations.

---

## CQ5 — The per-token claim vs. the POPE evaluation  [DEVELOP]

**The issue (your sharpest one).** The paper *claims* a "per-token instrument" measuring grounding "for a VLM's generated tokens." But POPE is yes/no VQA — there is no free-form generation, and as you put it, "we do not do token-level grounding" in the POPE setup. There is a gap between the claim's language and the evaluation's reality. The literature should tell us whether to (a) narrow the claim, (b) add a free-form generation evaluation, or (c) reframe what "per-token" means on POPE.

**Sub-questions.**

1. On POPE, the scored token is essentially the yes/no answer token (plus, under teacher forcing, the object token). Is "per-token instrument validated on the answer token" an honest description? Where does the language need to change?
2. How do token-level / generation-time grounding papers (Curing Semantic Drift, M3ID) *evaluate* token-level grounding? What datasets and metrics do they use that we currently lack?
3. If we want a real free-form test, what is the minimum addition — caption generation scored with CHAIR, then run the instrument on each object token? (CHAIR is already in the project as a secondary diagnostic; the audit found only 13/80 flagged mentions were true fabrications — so CHAIR noise is itself a CQ6 problem.)
4. Does teacher-forced extraction (feeding the reference answer) undermine the "generated tokens" claim, since the tokens aren't actually generated? How do others justify teacher forcing for measurement?
5. Can the per-token claim be *demonstrated* (not just validated) with a small qualitative free-form example set, even if POPE remains the quantitative backbone?

**Candidate literature (have).** Curing Semantic Drift (2506.21509); Multi-Modal Hallucination Control (2403.14003, M3ID-style); CHAIR (internal report + audit); Beyond Logit Lens (2411.19187, grounding categories).

**Gaps to search.** CHAIR original (Rohrbach et al.) and modern free-form hallucination benchmarks — AMBER, MMHal-Bench, HallusionBench, FaithScore, GAVIE — specifically which give *token/object-level* labels suitable for per-token grounding; teacher-forcing-for-measurement justifications.

**What a good answer looks like.** A decision, backed by literature, on one of: **(a)** retitle the instrument as "per-answer-token, validated on discriminative VQA, illustrated on generation" and add 2–3 free-form qualitative examples; or **(b)** commit to a free-form quantitative arm (caption + CHAIR/AMBER object tokens). Plus a clean justification of teacher forcing. This question can reshape the Claim, Setup, and Limitations — resolve it early.

**Feeds.** Paper claim, Setup §4, Limitations §7, possibly a new Experiment.

---

## CQ6 — Dataset choice and the partial-labeling trap  [DEVELOP]

**The issue.** "Suppose a dataset has 5 items but only 3 are labeled; if free-form generation describes 2 unlabeled items, we wrongly conclude 2 hallucinations." Incomplete ground truth manufactures false positives. We need datasets (or evaluation protocols) whose labeling is complete enough that "not in the labels" reliably means "not in the image." This directly constrains any free-form arm from CQ5.

**Sub-questions.**

1. Which grounding/hallucination datasets have *exhaustive* object annotation (so absence in labels ≈ absence in image)? Panoptic Narrative Grounding and panoptic COCO are exhaustive by construction — is that our clean substrate?
2. How does CHAIR handle the partial-label problem, and is its synonym/object-list closure the source of the 13/80 false-fabrication rate in our audit?
3. Do newer benchmarks (AMBER, MMHal, etc.) address incomplete labeling, e.g. via closed yes/no probing (which is exactly why POPE exists) or human verification?
4. Is POPE's discriminative design *precisely* the workaround for this problem — it asks "is X present?" for a controlled X, sidestepping open-ended recall? If so, that's a positive argument for POPE as primary, not just a limitation.
5. For Experiment C (evidence removal on *correct* answers) the partial-label issue is moot (we use model-correct cases) — confirm and note this as a reason C is robust.

**Candidate literature (have).** Panoptic Narrative Grounding (2109.04988); RefCOCO (1608.00272); CHAIR (internal); POPE (primary benchmark — confirm citation).

**Gaps to search.** POPE original (Li et al.) for its stated rationale; AMBER / MMHal-Bench / HallusionBench labeling-completeness discussion; panoptic segmentation completeness as a grounding substrate; any paper explicitly naming the "missing-annotation false-hallucination" problem.

**What a good answer looks like.** A short, citable argument that (i) POPE's closed discriminative format is a *deliberate* solution to partial labeling — turning the limitation into a justification for our primary choice; and (ii) if a free-form arm is added (CQ5), it must use an exhaustively annotated substrate (panoptic) or a closed-probe protocol, not raw caption-vs-object-list. Output: a one-paragraph "dataset rationale" for Setup, and a go/no-go on each candidate free-form dataset.

**Feeds.** Setup §4 (dataset justification), Exp A/C, Limitations.

---

## CQ7 — Closest and foundational papers: the differentiation matrix  [DEFEND]

**The issue.** "What are the closest papers to our methodology? Can we review each close or foundational paper?" This is the consolidation question — it consumes the answers to CQ1–CQ6 and turns them into the related-work matrix and per-paper notes.

**Sub-questions.**

1. For each *closest* paper, what one-sentence difference do we assert, and is it mechanical (different thing measured) or framing (same mechanism, different use)? Framing-only differences are weak — flag them.
2. For each *foundational* paper, what exactly do we cite it *for* (one claim per cite)?
3. Are there any papers that, if a reviewer found them, would read as "this is already done"? Identify the scariest neighbor and write its rebuttal now.

**Deliverable: the related-work matrix** (rows = papers; columns already specified in resources.md immediate tasks):

| Paper | Self-eval | Hallucination | Grounding | Internal signal | Causal | Localizes? | Dataset | Intervention vs. Measurement | One-line difference from us |
|---|---|---|---|---|---|---|---|---|---|

Fill one row per paper in resources.md. The "Localizes?" and "Causal" columns are where we expect to be alone — if a row has both, it's a threat; escalate to CQ1/CQ4.

**Tier the closest papers for per-paper review** (use the `paper-summarization` skill; tiers per that skill):

- **Tier 1 (full review — direct neighbors):** VAUQ (2602.21054); Beyond Logit Lens (2411.19187); the VCD/M3ID contrastive-decoding pair; Curing Semantic Drift (2506.21509).
- **Tier 2 (focused notes — mechanism or dataset bridges):** Hidden in Plain Sight (2506.08008); What's in the Image (2411.17491); F-LMM (2406.05821); Multi-Modal Hallucination Control (2403.14003); Uncertainty-Aware Evaluation (2402.14418).
- **Tier 3 (one-line context):** Eyes Wide Shut (2401.06209); MIRAGE (2603.21687); VLind-Bench (2406.08702); To See or To Please (2603.18373); Unveiling LVLM Robustness (2504.16727); Panoptic Narrative Grounding (2109.04988); RefCOCO (1608.00272); EigenScore; HaloScope.

Each Tier-1 review must end with the same two lines: **What to reuse. What to challenge.**

**Feeds.** Related Work §2, every reviewer rebuttal, Intro contributions.

---

## Search agenda (gaps not yet in resources.md)

Run these as a batch once the plan is approved. Grouped by the CQ they serve.

1. **Contrastive decoding canon (CQ1):** VCD original; M3ID original; contrastive/visual-contrastive decoding as a *detector*; null/blur/noise image-corruption decoding variants.
2. **Self-evaluation canon (CQ2):** P(True) / "models know what they know"; semantic entropy; verbalized confidence; internal truthfulness/honesty probes; VLM uncertainty surveys.
3. **Internal-signal detectors (CQ3):** EigenScore; HaloScope; INSIDE; internal-state hallucination detection; subword→object aggregation.
4. **Attribution faithfulness (CQ4):** comprehensiveness/sufficiency (ERASER); insertion-deletion / ROAR; occlusion-OOD critiques; causal tracing (ROME) for VLMs.
5. **Free-form & token-level hallucination eval (CQ5):** CHAIR original; AMBER; MMHal-Bench; HallusionBench; FaithScore; teacher-forcing-for-measurement.
6. **Labeling completeness (CQ6):** POPE original (its rationale); panoptic-completeness as grounding substrate; benchmarks that name the missing-annotation problem.

For each hit, file a note (below) and add a row to the related-work matrix.

---

## Filing scheme (so the review stays disciplined)

All literature lives under `60_literature/`. One note per paper, named `<short-handle>.md`, with frontmatter:

```
---
title: <paper title>
arxiv: <id>
tier: 1 | 2 | 3
serves_CQ: [1, 4]          # which core questions it answers
role: neighbor | foundational | dataset | background
---
```

Body, kept short: **What it does** (2–3 sentences) · **Mechanism** (what it measures/subtracts, at what stage) · **Difference from us** (one sentence, mechanical if possible) · **What to reuse** · **What to challenge** · **Cite for** (the one claim we cite it for).

Two roll-up artifacts, regenerated as notes land:

- `60_literature/related_work_matrix.md` — the CQ7 table.
- `60_literature/open_questions_status.md` — the seven CQs with status (open / closing / closed) and the blocking gap for each.

A CQ flips to **closed** only when its "what a good answer looks like" paragraph can be written with citations and survives the scariest-neighbor test.

---

## Sequencing

**Wave 1 — design-critical, do first (these can still change the paper):**
CQ5 (per-token claim vs. POPE) and CQ6 (dataset partial-labeling) together — they decide whether a free-form arm is added before any writing locks. Then CQ1 (contrastive-decoding boundary), which decides the central novelty framing.

**Wave 2 — method development:**
CQ3 (internal-signal mechanics) and CQ4 (causal necessity) — borrow and reviewer-proof before the method freezes.

**Wave 3 — positioning:**
CQ2 (self-eval landscape) and CQ7 (matrix + per-paper reviews) — consume everything above into Related Work and rebuttals.

Rationale: resolve the questions that can *move the design* before the ones that only *describe* it. CQ5 and CQ6 are first because a "yes, add free-form" answer there cascades into method, datasets, and experiments.

---

## Coverage check — every outstanding issue is mapped

| Your outstanding issue | Core question |
|---|---|
| POPE gives no free-form generation; "we do not do token-level grounding" | CQ5 |
| Problems with other datasets | CQ6 |
| Partial-labeling false hallucinations (5 items, 3 labeled) | CQ6 |
| Contrastive-decoding baseline; null/real ≈ contrastive decoding; "what's new?" | CQ1 |
| VAUQ review — main techniques and evaluation | CQ2, CQ7 (Tier 1) |
| Closest papers to our methodology | CQ7 |
| Review each close / foundational paper | CQ7 (tiered) |
| How do we get a signal? Is it unique? Which lit sources? | CQ1, CQ3 |
| How is VLM/LLM self-evaluation done? | CQ2 |
