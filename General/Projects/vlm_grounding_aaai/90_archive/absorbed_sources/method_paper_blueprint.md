# Method Paper Blueprint: Measuring Visual Grounding in VLMs

## Working Title

**"Measuring Visual Grounding in Vision-Language Models: A Training-Free Per-Token Instrument"**

---

## The One-Paragraph Pitch

Current VLM benchmarks evaluate output correctness but cannot distinguish image-grounded answers from lucky guesses driven by language priors. We introduce a training-free, per-token grounding instrument that extracts three complementary signals — state, decision, and causal — from a single model's internal activations under real versus null visual conditions. The instrument detects hallucinations (AUC 0.88), localizes grounding to specific image patches, identifies "accidentally correct" answers that are fragile under perturbation, and tracks grounding degradation as visual evidence is corrupted. Unlike behavioral approaches that compare clean vs. text-only outputs, our method provides a mechanistic account of *where* and *why* grounding fails at the token level.

---

## Five Claims and Their Matched Experiments

### Claim 1: The instrument detects hallucination from internal signals alone

**What we're saying:** Without access to ground truth, the grounding signal separates hallucinated from grounded outputs on clean images, outperforming simple logit-based baselines.

**Experiment — Hallucination Detection (Section 5.1)**

- Dataset: POPE adversarial (1K samples)
- Protocol: Compute three-track grounding metrics under teacher-forced extraction. Evaluate ROC-AUC for distinguishing `hallucinated_yes` (model said "yes" when GT is "no") from correct responses.
- Key result: `dec_dp_x_cvar` achieves AUC 0.885 on hallucinated_yes detection. `cau_rel_drop` achieves AUC 0.762 as independent mechanistic validation.
- Baselines: (a) random (AUC 0.5), (b) logit confidence only (`dec_p_real`), (c) output probability ratio (`dec_p_ratio`, AUC 0.873 — strong but no spatial or causal information).
- Supplementary: CHAIR-200 evaluation showing `decision_jsd_tau0.1` AUC 0.748 on open-ended captioning hallucination.

**Figures:**
- ROC curves comparing champion metrics against baselines
- Distribution histograms of grounding scores split by hallucinated vs. correct
- Table of AUC across all three tracks with top-5 metrics per track

**STATUS: ✅ COMPLETE** — all data exists in POPE-1K and CHAIR-200 runs.

---

### Claim 2: Grounding is causally linked to specific image patches, not diffuse representation shift

**What we're saying:** The causal track confirms that high state-grounding attribution maps point to patches that are genuinely necessary for the model's prediction — ablating them causes probability drops, while ablating random patches of the same size does not.

**Experiment — Causal Validation (Section 5.2)**

- Protocol: For each sample's focal token, construct the concept-profile support mask (top patches by δs_j(y_t)), ablate those patches, measure log-probability drop. Compare against matched random-mask controls.
- Key result: `cau_rel_drop` separates hallucinated from grounded (AUC 0.762). Targeted ablation produces larger drops than random ablation (`cau_specificity_margin > 0`).

**Figures:**
- Scatter: state grounding score vs. causal drop (showing positive correlation)
- Bar chart: targeted vs. random ablation drop sizes
- Example heatmaps: attributed patches overlaid on image for grounded vs. hallucinated token

**STATUS: ✅ COMPLETE** — causal pipeline runs exist, specificity margins computed.

---

### Claim 3: Grounding localizes to semantically correct image regions

**What we're saying:** For tokens naming visible objects, the top-attributed patches overlap with the ground-truth spatial location of that object — not with random image regions.

**Experiment — Spatial Correspondence via Bounding Box IoU (Section 5.3)**

- Dataset: POPE samples whose queried object has a COCO bounding box annotation.
- Protocol: For each visual noun token at the focal generation step, map the top-k attributed patches back to their spatial grid positions (24×24 → image coordinates). Compute IoU between the attributed patch region and the COCO ground-truth bounding box.
- Key comparisons: (a) IoU for grounded-correct cases vs. hallucinated cases, (b) IoU vs. random baseline, (c) IoU for concept-profile attribution vs. raw state-delta attribution.

**STATUS: ⚠️ NOT YET RUN** — all ingredients exist, estimated effort: 1-2 days scripting, zero new forward passes.

---

### Claim 4: Correct but ungrounded answers are fragile under perturbation

**What we're saying:** Among answers the model gets right, those with low grounding scores flip to incorrect under minimal perturbation — revealing a dangerous failure mode invisible to accuracy metrics.

**Experiment — Flip-Rate Fragility (Section 5.4)**

- Dataset: Filter POPE to correct-answer-only subset. Stratify by grounding score into quartiles.
- Perturbations: (a) Prompt paraphrase, (b) Mild Gaussian blur (σ=1), (c) Random crop/shift (±5% spatial jitter).
- Protocol: For each perturbation, re-run generation (free generation). Measure flip rate = fraction that change from correct to incorrect.
- Key result expected: Q1 flip rate 2-3× higher than Q4.

**STATUS: ❌ NOT YET RUN** — requires new forward passes (~2-3 hours on RTX 3090). **Highest-priority missing experiment — most novel claim.**

---

### Claim 5: Grounding degrades monotonically as visual evidence is corrupted

**What we're saying:** The instrument tracks actual visual evidence, not representation noise. As image quality degrades, grounding scores decrease monotonically for genuinely grounded tokens, while remaining flat for hallucinated ones.

**Experiment — Corruption Ladder (Section 5.5)**

- Dataset: 200-image subset (stratified: 50 grounded-correct, 50 hallucinated, 50 ambiguous, 50 diverse).
- Corruption types: Gaussian blur σ ∈ {0, 1, 3, 5, 7}, additive noise σ ∈ {0, 0.1, 0.2, 0.3}.
- Protocol: For each corruption level, run full extraction pipeline (teacher-forced). Plot S(corruption_severity) curves.

**STATUS: ❌ NOT YET RUN** — requires new forward passes (~8-10 hours of compute). Second-highest priority.

---

## Paper Structure (8 pages + supplementary)

| Section | Pages | Content |
|---------|-------|---------|
| 1. Introduction | 1.0 | Problem (grounding ≠ accuracy), the "accidentally correct" gap, contribution summary |
| 2. Related Work | 0.75 | VCD, M3ID, EAZY, ContextualLens, logit lens — position as *measurement* not intervention |
| 3. Method | 2.0 | Three-track framework (state/decision/causal), counterfactual extraction, teacher forcing, metric definitions |
| 4. Experimental Setup | 0.5 | LLaVA-1.5-7B, POPE, CHAIR, null construction, extraction protocol |
| 5. Results | 2.5 | Five subsections matching the five claims above |
| 6. Discussion | 0.75 | Limitations (single model, POPE format), connection to DriveBench, future directions |
| 7. Conclusion | 0.25 | Summary |
| Supplementary | ~4 | Full metric tables, additional heatmaps, ablation details (null choice, whitening, kernel) |

---

## Differentiation from Nearest Competitors

| Aspect | VCD / M3ID | Logit Lens (Jiang+) | ContextualLens | **Ours** |
|--------|-----------|---------------------|----------------|----------|
| Purpose | Intervention (fix decoding) | Detection | Detection + localization | Detection + diagnosis |
| Signal source | Output logit comparison | Patch → vocabulary projection | Middle-layer cosine similarity | Three-track contrastive extraction |
| Granularity | Token-level probability | Patch-level confidence | Answer-level aggregate | Token × patch matrix |
| Causal validation | No | No (correlational) | No | Yes (patch ablation) |
| Fragility detection | No | No | No | Yes (flip-rate experiment) |
| Requires retraining | No | No | No | No |
| Spatial localization | No | Yes (zero-shot segmentation) | Yes (bounding box) | Yes (concept-conditioned) |

The key differentiator is the **three-track design with causal validation**. The second differentiator is **fragility detection** — no existing method explicitly identifies correct-but-ungrounded answers and demonstrates they are unstable.

---

## Execution Priority

| Priority | Experiment | Effort | New Passes? | Claim |
|----------|-----------|--------|-------------|-------|
| **P0** | Flip-rate fragility | 2-3 days | Yes (~3 hrs GPU) | Claim 4 (most novel) |
| **P1** | Bounding box IoU | 1-2 days | No | Claim 3 (external validation) |
| **P2** | Corruption ladder | 2 days | Yes (~10 hrs GPU) | Claim 5 (measurement validity) |
| Done | Hallucination detection | — | — | Claim 1 |
| Done | Causal validation | — | — | Claim 2 |

**Critical path: P0 → P1 → P2 → write**

---

## Venue Fit

| Venue | Fit | Why |
|-------|-----|-----|
| **EMNLP 2026** | Strong | Interpretability + measurement methodology; analysis paper tradition |
| **NeurIPS 2026** | Strong | Mechanistic interpretability track; novel measurement theory |
| **ACL 2026** | Good | Language model analysis; grounding is core NLP concept |
| **ICLR 2027** | Good | Representation analysis; fits the probing/interpretability category |
| **CVPR/ICCV** | Moderate | More application-focused; would want multi-model + downstream task results |

> **Note:** This blueprint is superseded by `PAPER_TRACK_FROZEN_v2.md` for claim structure and method choices. Use this file for pitch/differentiation/venue fit sections only.