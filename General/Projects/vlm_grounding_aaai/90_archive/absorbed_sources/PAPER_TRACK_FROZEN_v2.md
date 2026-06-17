# PAPER TRACK — FROZEN v2  
  
## Measuring Visual Grounding in Vision-Language Models: A Training-Free Per-Token Instrument  
  
**Frozen: March 2026 — Revision 2 (reviewer-proofed)**  
**Rule: Nothing enters this paper that is not in this document.**  
  
---  
  
## WHAT THIS DOCUMENT IS  
  
This is the single authoritative specification of the paper. Everything produced before this — the exploratory notebooks, the V2/V3/V3B/V3C branches, the projection R² formulations, the spectral efficiency framework, the seven-category formulation catalog, the layerwise dispersion analysis — is archived as exploration. None of it enters the paper unless it is listed below.  
  
### Archived as exploration (out of scope)  
  
- Three-station framework / escape velocity / spectral efficiency  
- Projection R² formulation (empirically failed)  
- DeltaV / V2 / V3 / V3A / V3B / V3C frontier branches  
- Concept-anchored grounding reformulation  
- JSD distribution alignment alternatives  
- Layerwise information-dispersion analysis  
- Grid-aware aggregation redesign  
- Training-objective analysis  
- Bounding-box localization as a headline claim  
- Visual Evidence Curves / corruption ladder as a main contribution  
  
### Kept for paper track  
  
- Counterfactual null-vs-real stable baseline  
- Three-track decomposition (state, decision, causal)  
- POPE benchmark results (ablation-line and benchmark-line, distinguished)  
- Causal validation material  
- Technical implementation report (math specification)  
- CHAIR as secondary diagnostic context only (see §IX, point 7)  
  
---  
  
## TERMINOLOGY LOCK  
  
**Primary evaluation target:** `hallucinated_yes` on POPE official adversarial 1K — defined as samples where the model answered "yes" to a ground-truth "no" object-presence question. All headline AUC numbers in this document refer to discrimination of `hallucinated_yes` vs. `correct` responses under this target unless otherwise stated.  
  
**Two result lines exist and must not be conflated:**  
  
- **Ablation-line results:** Produced under the frozen ablation setting (N0 null, raw L32, teacher-forced extraction with the full three-track pipeline). These are the primary numbers reported in the paper. Example: `dec_dp_x_cvar` AUC = 0.885 on `hallucinated_yes`.  
  
- **Benchmark-line results:** Produced under the POPE-1K benchmark-facing evaluation, which uses a different scoring path. The strongest single intrinsic benchmark metric is `causal_delta_logp_random` = 0.7667. `decision_p_real` under the benchmark line is 0.6516, not 0.600.  
  
The 0.600 figure for `dec_p_real` in the ablation line and the 0.6516 for `decision_p_real` in the benchmark line are different numbers from different evaluation paths. The paper must state which line each number comes from. All primary results tables use the ablation line. The benchmark line appears only when comparing to the POPE-1K benchmark-facing evaluation.  
  
---  
  
## I. PROBLEM STATEMENT  
  
Current VLM evaluation measures output correctness: did the model say the right thing? But correctness is not grounding. A model can be correct because it used the image, or correct because language priors happened to agree with the ground truth regardless of the image. Behavioral benchmarks — POPE, CHAIR, DriveBench — cannot distinguish these two cases.  
  
**The scientific problem:**  
  
> How can we measure whether a VLM's generated token is genuinely image-conditioned, rather than a plausible continuation driven mostly by language priors?  
  
That is the paper's problem. Not dispersion. Not training objectives. Not layer analysis. Not spatial segmentation.  
  
---  
  
## II. RESEARCH QUESTIONS  
  
Three questions. No more.  
  
**RQ1 — Measurement.**  
Can visual grounding be measured directly from internal activations and probabilities under a real-vs-null protocol?  
  
**RQ2 — Utility.**  
Can intrinsic grounding scores distinguish grounded outputs from hallucinated or prior-driven outputs?  
  
**RQ3 — Added value.**  
Can intrinsic grounding reveal a failure mode that ordinary accuracy and confidence miss?  
  
**Unifying logic:** All three are about counterfactual dependence — would the output change if the visual information changed?  
  
**Dependency:** RQ1 is foundational. If the instrument cannot produce a meaningful signal, RQ2 and RQ3 are moot. RQ2 and RQ3 are independent of each other.  
  
---  
  
## III. HYPOTHESES  
  
Four hypotheses. Each is falsifiable with a named experiment and a concrete passing criterion.  
  
### H1 — Counterfactual sensitivity  
  
If a token is genuinely grounded, removing image evidence should change its internal representation, decision distribution, or causal dependence. Tokens that are prior-driven should show minimal change.  
  
*Tests:* Does the contrastive signal (real minus null) produce a non-trivial, structured signal? Does it outperform raw confidence?  
  
*Passing criterion:* `dec_dp_x_cvar` AUC > `dec_p_real` AUC by ≥ 10 points on `hallucinated_yes` (ablation line).  
  
*Status:* **✅ PASSED.** `dec_dp_x_cvar` AUC = 0.885 vs. `dec_p_real` AUC = 0.600 (ablation line). Margin = +28.5 points.  
  
### H2 — Token selectivity  
  
A useful grounding signal should separate visually meaningful tokens from punctuation, filler, or structurally weak tokens. If the instrument scores function words as highly as visual nouns, the semantic claims collapse.  
  
*Tests:* Mean grounding score by token class on a fixed sampled subset with a frozen annotation rubric.  
  
*Token-class definitions (frozen rubric):*  
  
| Class | Label | Definition | Examples |  
|-------|-------|------------|----------|  
| V | Visual noun | Object nouns or visually grounded nouns naming entities present (or queried) in the image. Identified via COCO object alias table where applicable. | "dog", "car", "table" |  
| A | Visual attribute | Adjectives or modifiers describing visual properties of an object in the image. | "red", "large", "wooden" |  
| F | Function / structural | Articles, prepositions, conjunctions, punctuation, copulas, and other tokens with no independent visual grounding. | "the", "is", "of", ".", "," |  
  
*Annotation protocol:* Apply rubric to all content tokens in 100 POPE generated answers. Each token receives exactly one label. Ambiguous cases (e.g., "sitting" — action or function?) are resolved by whether the token describes a visually verifiable property. Annotation is performed by one annotator on a fixed subset; inter-annotator reliability is noted as a limitation if a second annotator is not available.  
  
*Passing criterion:* V > A > F at p < 0.01 (Wilcoxon signed-rank) for each adjacent comparison. V/F ratio ≥ 2.0.  
  
*Status:* **⚠️ NOT YET RUN.** No GPU required. ~4 hours manual annotation on existing data. This is method-level internal validation — it belongs in the Method section, not as a standalone results section.  
  
### H3 — Causal faithfulness  
  
Support patches chosen by the instrument should matter more than matched random patches when ablated. The concept-profile attribution is not merely correlational — it identifies causally necessary patches.  
  
*Tests:* Targeted ablation drop vs. matched random ablation drop.  
  
*Passing criterion:* Mean targeted drop significantly > mean random drop (p < 0.001, paired t-test). `cau_rel_drop` AUC > 0.70 on `hallucinated_yes` (ablation line).  
  
*Status:* **⚠️ PARTIALLY PASSED.** Directional evidence is complete: `cau_rel_drop` AUC = 0.762 on `hallucinated_yes`. `cau_specificity_margin` > 0 across POPE-200. `cau_targeted_vs_random` positive. **Formal significance test and effect-size reporting still to finalize.** The paired t-test and Cohen's d must be computed and reported before this status upgrades to fully passed.  
  
### H4 — Beyond accuracy  
  
Grounding should reveal something that plain model accuracy does not. Specifically: among correct answers, those with low grounding should be *less affected* by support-targeted evidence removal than those with high grounding — indicating the low-grounding answers were never depending on the image.  
  
*Tests:* Two complementary approaches (see Experiment C below).  
  
*Passing criterion:* Statistically significant difference (p < 0.01) in degree of answer degradation (log-probability drop, persistence rate, or flip rate) between low-grounding and high-grounding correct answers.  
  
*Status:* **❌ NOT YET RUN.** This is the paper's most novel claim. Highest priority for new work.  
  
---  
  
## IV. METHODOLOGY  
  
### IV.1 Core principle  
  
Hold the prompt, token sequence, and decoding policy fixed. Replace the real image with a content-free null visual baseline. Measure how internal states and output probabilities change. Any measurable change is attributed to visual content.  
  
**Why counterfactual, not absolute:** Raw cosine alignments between hidden states and patch vectors have a non-zero floor driven by anisotropy in the embedding space. Even purely textual tokens have non-trivial inner products with every patch vector. Subtracting a null-image pass removes this background correlation, isolating the image-specific signal.  
  
### IV.2 Protocol  
  
1. Generate a reference answer on the real image via greedy decoding.  
2. Teacher-force the same token sequence under both real and null conditions.  
3. Extract Layer-32 hidden states and logits at each token position under both conditions.  
4. Extract Layer-32 patch representations from the real-image pass.  
5. Compute three families of intrinsic measurements.  
  
### IV.3 Null image construction  
  
The null image is a tensor P⁰ ∈ ℝ^{576×1024} in CLIP space — not a pixel image.  
  
**Canonical null (N0): Dataset-mean patch.** Mean of all CLIP patch vectors across COCO validation. Removes semantic content while preserving statistical distribution of visual features. Layout-preserving: injects the same number of tokens in the same positions.  
  
**Empirical validation:** Under N0, `dec_dp_x_cvar` AUC = 0.885. Under patch-shuffle (N3), AUC = 0.515 (near chance). Under per-image-mean (N1), AUC = 0.735. Under white-noise (N2), AUC = 0.743. N3 and N4 are structurally invalid nulls. N0 is preferred over N2 because it stays within the CLIP learned distribution.  
  
### IV.4 The three-track instrument  
  
**Track 1 — State grounding:** Did the real image shift the token's hidden state toward specific patch directions?  
  
- Cosine delta matrix: Δ[t,j] = cos(H^r_t, V_j) − cos(H^0_t, V_j)  
- Key metric: `state_delta_var` — spatial variance of the delta row  
- High when the image caused a concentrated (not diffuse) state shift  
- Claim strength: weakest — purely representational, correlational  
  
**Track 2 — Decision grounding:** Did the real image change what the model chose to generate?  
  
- Probability shift: Δp_t = p^r_t(y*) − p^0_t(y*)  
- Concept-conditioned metric: `dec_dp_x_cvar` = Δp_t × Var_j(concept_profile_j)  
- The ×cvar term penalizes probability shifts with diffuse spatial attribution  
- Claim strength: medium — the image changed the output distribution  
  
**Track 3 — Causal grounding:** Are the attributed patches actually necessary for the prediction?  
  
- Identify top-k patches by concept profile, ablate them  
- Measure log-probability drop vs. matched random ablations of the same cardinality  
- Key metrics: `cau_rel_drop`, `cau_specificity_margin`  
- Claim strength: strongest — causal necessity, not just correlation  
  
### IV.5 Frozen design decisions  
  
| Decision | Choice | Justification |  
|----------|--------|---------------|  
| Layer | 32 (final) | Grounding suppressed by L32 does not influence output. Measure what actually drives the decision. |  
| Null | N0 (dataset-mean patch) | Empirically validated. Preserves CLIP distribution while removing semantic content. |  
| Concept conditioning | ×cvar product | Filters diffuse probability shifts. Expected to improve V/F separation (pending H2 test). |  
| Space | Raw Layer-32, no whitening | Stage B ablations: raw space dominates for `hallucinated_yes` across all kernels. |  
| Random controls | K=3 matched random masks | Required for causal specificity. Cardinality-matched. |  
  
### IV.6 Method-level internal validation  
  
Two checks belong in the Method section, not as standalone results sections:  
  
**Token selectivity (H2):** Report V/A/F grounding score distributions using the frozen annotation rubric (§III, H2) as evidence that the instrument produces semantically coherent orderings. This validates the instrument's construct.  
  
**Cross-track convergence:** Report Spearman ρ between `state_delta_var`, `dec_dp_x_cvar`, and `cau_rel_drop`. This assesses whether the three tracks provide *compatible* evidence or *complementary* evidence. Strong agreement supports a shared construct; partial divergence suggests grounding is multidimensional. Either outcome is reportable — one supports parsimony, the other supports the value of decomposition. Do not pre-commit to "same underlying construct."  
  
---  
  
## V. EXPERIMENTAL VALIDATION  
  
Three experiment blocks. No more.  
  
### Experiment A — Benchmark Discrimination  
  
**Validates:** RQ2, H1  
  
**Dataset:** POPE official adversarial 1K (balanced yes/no)  
  
**Primary target:** `hallucinated_yes` vs. `correct` responses.  
  
**Protocol:** Compute three-track grounding metrics under teacher-forced extraction (ablation line). Evaluate ROC-AUC for discriminating `hallucinated_yes` from correct responses.  
  
**Results in hand (ablation line):**  
  
| Metric | AUC | Role |  
|--------|-----|------|  
| `dec_dp_x_cvar` | **0.885** | Champion — contrastive + spatial |  
| `dec_log_p_ratio` | 0.873 | Strong baseline — contrastive, no spatial |  
| `dec_delta_p` | 0.877 | Contrastive, no concept conditioning |  
| `cau_rel_drop` | 0.762 | Independent causal validation |  
| `dec_p_real` | 0.600 | Raw confidence (ablation line) — near chance |  
| Random | 0.500 | Floor |  
  
**For reference (benchmark line, different evaluation path):**  
  
| Metric | AUC | Notes |  
|--------|-----|-------|  
| `causal_delta_logp_random` | 0.7667 | Strongest single benchmark-facing intrinsic metric |  
| `decision_p_real` | 0.6516 | Benchmark-line confidence (not same as ablation-line 0.600) |  
| Direct task accuracy | 0.8300 | Model yes/no correctness on POPE |  
  
The ablation-line numbers (top table) are the paper's primary results. The benchmark-line numbers provide context and must not be mixed with ablation-line numbers in the same table.  
  
**The ratio baseline — addressed head-on:**  
  
`dec_log_p_ratio` achieves AUC 0.873 — within 1.2 points of the champion on scalar detection.  
  
The instrument's value over the ratio is not improved scalar detection. It is decomposition into three distinct questions about the image's role:  
  
1. **Where** the image matters (spatial localization via the concept profile — the ratio is a scalar with no spatial information)  
2. **Whether** the image matters (decision-level probability shift — shared with the ratio, but concept-conditioned by ×cvar to filter diffuse shifts)  
3. **Whether necessarily** the image matters (causal track — the ratio cannot distinguish causal from correlational evidence)  
  
This must be argued concretely with worked examples, not just asserted.  
  
**Status: ✅ COMPLETE** — all data exists.  
  
### Experiment B — Causal Validation  
  
**Validates:** H3  
  
**Dataset:** POPE-200 subset  
  
**Results in hand:**  
- `cau_rel_drop` AUC = 0.762 on `hallucinated_yes` (ablation line)  
- `cau_specificity_margin` > 0 across POPE-200  
- `cau_targeted_vs_random` positive (targeted ablation produces larger drops)  
  
**What remains:** Formal paired t-test (targeted vs. random) and effect-size reporting (Cohen's d).  
  
**Status: ⚠️ PARTIALLY COMPLETE** — directional evidence exists; formal significance reporting to finalize.  
  
### Experiment C — Beyond-Accuracy Validation  
  
**Validates:** RQ3, H4  
  
**This is the paper's most important unfinished experiment.**  
  
Core claim: among *correct* answers, low-grounding cases should be *less affected* by support-targeted evidence removal than high-grounding cases — because the low-grounding answers were never depending on the image in the first place.  
  
**Approach 1 (primary): Evidence removal on correct cases**  
1. Take all correct POPE answers.  
2. Split into low-grounding (bottom quartile of `dec_dp_x_cvar`) and high-grounding (top quartile).  
3. For each sample, ablate the support patches.  
4. Measure log-probability drop on the answer token.  
5. Compare: degree of degradation in low-grounding vs. high-grounding correct answers.  
  
**Approach 2 (robustness check): Perturbation fragility**  
1. Same low/high grounding split on correct answers.  
2. Apply minimal perturbations: slight crop (5%), Gaussian blur (σ=1), JPEG compression (quality=50).  
3. Re-run the model on perturbed images.  
4. Measure flip rate.  
  
**Status: ❌ NOT YET RUN.** Highest priority for new work.  
  
---  
  
## VI. PAPER STRUCTURE  
  
| Section | Content | Length |  
|---------|---------|--------|  
| 1. Introduction | Grounding ≠ correctness. "Right for the wrong reason." Contributions. | 1.5 pp |  
| 2. Related Work | VCD/M3ID (intervention), EigenScore/HaloScope (detection), attention methods. | 1 pp |  
| 3. Method | Null construction, teacher forcing, three tracks, core metrics, design decisions. Internal validation: token selectivity (H2) and cross-track analysis. | 2.5 pp |  
| 4. Experimental Setup | LLaVA-1.5-7B, POPE, evaluation targets, baselines, ablation-line vs. benchmark-line distinction. | 0.5 pp |  
| 5.1 Benchmark Discrimination | Experiment A. ROC curves, AUC table, baseline comparison, worked examples. | 1.5 pp |  
| 5.2 Causal Validation | Experiment B. Targeted vs. random ablation, effect sizes, significance. | 1 pp |  
| 5.3 Beyond-Accuracy Validation | Experiment C. Evidence removal on correct cases, degradation analysis. | 1.5 pp |  
| 6. Discussion | What the instrument measures and does not. The ratio baseline question. Cross-track interpretation. Spatial localization as open question. | 1 pp |  
| 7. Limitations | Single model, POPE-centric, teacher-forcing, L32 only, region-not-pixel, CHAIR noise. | 0.5 pp |  
| 8. Conclusion | — | 0.5 pp |  
  
**Target: ~12 pages + references + appendix**  
  
---  
  
## VII. CONTRIBUTIONS  
  
1. We introduce a training-free, per-token grounding instrument for VLMs based on a real-vs-null counterfactual protocol, decomposed into state, decision, and causal tracks.  
  
2. We demonstrate that the instrument detects hallucination from internal signals alone (AUC 0.885 on POPE adversarial, ablation line), with the counterfactual component responsible for the large majority of detection performance over raw confidence.  
  
3. We provide causal validation that attributed patches are genuinely necessary for the model's predictions — targeted ablation produces significantly larger probability drops than matched random ablation.  
  
4. **[CONDITIONAL on Experiment C]** We show that the instrument identifies a failure mode invisible to accuracy metrics: correct answers with low grounding scores degrade less under evidence removal, indicating they were never visually supported.  
  
---  
  
## VIII. EXECUTION PLAN  
  
### What is done  
  
| Item | Status |  
|------|--------|  
| Full three-track extraction on POPE-1K | ✅ |  
| Experiment A: All AUC numbers (ablation line) | ✅ |  
| Experiment B: Causal ablation on POPE-200 (directional) | ✅ |  
| Null ablation (Stage A, N0–N4) | ✅ |  
| Space/kernel ablation (Stage B) | ✅ |  
| CHAIR-200 extraction (secondary only) | ✅ |  
  
### Blocking the paper (must complete)  
  
| Priority | Task | Effort | GPU? |  
|----------|------|--------|------|  
| **1** | **Experiment C, Approach 1:** Evidence removal on correct cases | Medium | Possibly from existing data |  
| **2** | **H3 significance finalization:** Paired t-test + Cohen's d on targeted vs. random ablation | ~1 hour | No |  
| **3** | **H2: Token-class annotation** using frozen rubric on 100 POPE samples | ~4 hours | No |  
| **4** | **Cross-track convergence:** Spearman ρ computation | ~1 hour | No |  
| **5** | **Worked examples** for ratio-vs-instrument distinction (Experiment A) | ~2 hours | No |  
| **6** | **Ablation-line vs. benchmark-line reconciliation** table for the paper | ~1 hour | No |  
  
---  
  
## IX. HONEST LIMITATIONS  
  
1. **Single model.** All results are on LLaVA-1.5-7B. Generalization to other architectures is future work.  
2. **POPE-centric.** POPE is binary yes/no. Generalization to open-ended generation is not demonstrated.  
3. **The ratio baseline.** `dec_log_p_ratio` at AUC 0.873 nearly matches the champion for scalar detection. The instrument's added value is spatial, causal, and semantic — not raw detection performance.  
4. **Teacher-forcing.** The protocol requires the token sequence in advance. The instrument operates post-hoc, not during live generation.  
5. **Layer 32 only.** Grounding at earlier layers that gets suppressed is not captured.  
6. **Region, not pixel.** Localization is at patch resolution (~14×14 pixels), not pixel-level.  
7. **CHAIR is not a primary validation target.** No primary claims rest on CHAIR evidence.  
8. **Single annotator for H2.** Token-class annotation is performed by one annotator.  
  
---  
  
## X. THE FREEZE  
  
This document is frozen. The following are locked:  
  
- **1** problem statement  
- **3** research questions  
- **4** hypotheses (H3 status to be upgraded after significance test; H4 conditional on Experiment C)  
- **1** stable baseline method (no frontier branches)  
- **3** validation experiments (no more)  
- **1** primary benchmark (POPE adversarial 1K)  
- **1** primary evaluation target (`hallucinated_yes` vs. `correct`)  
- **1** model (LLaVA-1.5-7B)  
- **2** result lines distinguished (ablation-line primary, benchmark-line contextual)  
- **4** contributions (Contribution 4 conditional)  
  
Anything not listed here does not enter the paper. New ideas go into a separate "future work notes" file. They do not reopen this document.