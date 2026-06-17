# Research Progress Report  
  
> Status: Collaborator-facing draft.  
> Scope: Research progress, experimental history, major findings, and open questions for the `vlm_grounding` codebase.  
  
## Table Of Contents  
  
- [1. Executive Summary](#1-executive-summary)  
- [2. Project Goal](#2-project-goal)  
- [3. Main Research Questions](#3-main-research-questions)  
- [4. High-Level Method](#4-high-level-method)  
- [5. Evolution Of The Research Program](#5-evolution-of-the-research-program)  
- [5.1 Phase I: Core Method Formulation](#51-phase-i-core-method-formulation)  
- [5.2 Phase II: Notebook-Led Signal Inspection](#52-phase-ii-notebook-led-signal-inspection)  
- [5.3 Phase III: Systematic Ablation Program](#53-phase-iii-systematic-ablation-program)  
- [5.4 Phase IV: Benchmark Evaluation](#54-phase-iv-benchmark-evaluation)  
- [5.5 Phase V: CHAIR Audit And Interpretation Correction](#55-phase-v-chair-audit-and-interpretation-correction)  
- [5.6 Phase VI: GT-Free Judge And Metric Reduction](#56-phase-vi-gt-free-judge-and-metric-reduction)  
- [5.7 Phase VII: Frontier V2 / V3 / V3A / V3B Line](#57-phase-vii-frontier-v2--v3--v3a--v3b-line)  
- [5.8 Phase VIII: Current Validation Agenda](#58-phase-viii-current-validation-agenda)  
- [6. Progress Snapshot Across Workstreams](#6-progress-snapshot-across-workstreams)  
- [7. Main Findings And Observations](#7-main-findings-and-observations)  
- [8. Figure Plan](#8-figure-plan)  
- [9. Open Questions](#9-open-questions)  
- [9.1 Baselines And Comparative Value](#91-baselines-and-comparative-value)  
- [9.2 Interpretation And Aggregation](#92-interpretation-and-aggregation)  
- [9.3 Spatial And Mechanistic Questions](#93-spatial-and-mechanistic-questions)  
- [9.4 Frontier-Branch Questions](#94-frontier-branch-questions)  
- [9.5 Specific Unresolved Analytical Issues From The Current Codebase](#95-specific-unresolved-analytical-issues-from-the-current-codebase)  
- [10. Next Work](#10-next-work)  
- [11. Appendix: Repository Source Map (Optional)](#11-appendix-repository-source-map-optional)  
- [12. Recommended Finalization Options](#12-recommended-finalization-options)  
  
## 1. Executive Summary  
  
This project studies how to measure visual grounding inside a vision-language model (VLM), specifically the `llava-hf/llava-1.5-7b-hf` stack, rather than inferring grounding only from output correctness. The core idea is to compare the model's behavior under a real image versus a content-free null visual condition while holding the prompt and generated token sequence fixed. From this counterfactual setup, the codebase defines three complementary intrinsic views of grounding:  
  
- **State grounding**: whether the token representation moves with image evidence  
- **Decision grounding**: whether the model's next-token decision depends on the image  
- **Causal grounding**: whether specific visual support is necessary under targeted patch ablation  
  
The strongest completed line of evidence in the codebase is the benchmark-and-ablation story around Polling-based Object Probing Evaluation (POPE) official adversarial 1K, Caption Hallucination Assessment with Image Relevance (CHAIR)-200, and the Stage A/B/C/D ablation suite. That line supports a narrow but real claim: intrinsic signals derived from real-vs-null comparisons can separate grounded from hallucination-like behavior better than chance, and causal metrics are especially strong on the primary POPE benchmark. At the same time, the codebase has accumulated evidence that benchmark interpretation matters a lot. In particular, the CHAIR audit shows that raw CHAIR flags are too noisy to be treated as direct hallucination truth without correction.  
  
Alongside the stable baseline line, the repo contains two major exploratory extensions. The first is a **ground-truth-free (GT-free) judge / metric-reduction** branch that aligns intrinsic signals to claim-level labels from a multimodal judge instead of depending only on benchmark annotations. The second is a **V2 / V3 / V3A / V3B** frontier line that tries to improve the patch-evidence object itself, especially the projection and calibration logic behind image-side support.  
  
The current project position is therefore mixed but productive:  
  
- the original intrinsic grounding stack is implemented, benchmarked, and reasonably well documented  
- the Stage A/B/C/D ablation program has frozen key methodological choices for the baseline line  
- the CHAIR audit significantly improved the interpretation of earlier benchmark claims  
- the GT-free branch is implemented and promising, but still secondary in evidentiary maturity  
- the V2/V3 frontier branch has generated strong implementation and acceptance evidence, but it is not yet benchmark-promoted or fully closed  
- the next big step is a more formal validation program around evidence monotonicity, token selectivity, fragility, spatial correspondence, and transfer  
  
### Progress At A Glance  
  
| Workstream | Status | Current position |  
|---|---|---|  
| Core intrinsic method | Complete baseline | Implemented, documented, and benchmarked |  
| Notebook-led signal inspection | Complete exploratory line | Strong source of qualitative and mechanistic insight |  
| Stage A/B/C/D ablations | Complete | Main baseline decisions frozen |  
| POPE / CHAIR benchmark line | Complete, with interpretation caveats | Strongest current empirical evidence |  
| CHAIR audit | Complete | Major correction to earlier benchmark interpretation |  
| GT-free judge / metric reduction | Complete secondary line | Promising but less mature than the benchmark line |  
| V2 / V3 / V3A / V3B frontier line | Active | Strong implementation progress, not yet fully benchmark-closed |  
| Property-matched validation agenda | Planned / partially scaffolded | Most important next research stage |  
  
### Reader Orientation  
  
The report is written to be readable without prior repo context. The most important background assumptions are:  
  
| Item | Meaning in this report |  
|---|---|  
| VLM studied | `llava-hf/llava-1.5-7b-hf`, a LLaVA-family model with a CLIP vision encoder, a two-layer multimodal projector, and a Vicuna-family language model |  
| Patch | One of 576 image-grid tokens produced by the visual pathway; these patch positions are the spatial units used by the state, decision, and causal analyses |  
| Layer-32 space | The final transformer hidden-state layer used for most baseline intrinsic comparisons |  
| Metric families | The three intrinsic families are **state**, **decision**, and **causal** grounding |  
| Teacher forcing | Replaying the model on the same fixed generated answer tokens rather than letting it decode a new answer under the null image |  
| Calibrated grounding confidence | A sample-level composite of the three grounding families that is Platt-calibrated and evaluated out-of-fold; it summarizes ranking and calibration, not direct task accuracy |  
  
### Key Acronyms  
  
| Term | Expansion / meaning |  
|---|---|  
| VLM | Vision-Language Model |  
| GT | Ground Truth |  
| GT-free | Ground-truth-free evaluation path that does not rely directly on benchmark object lists or reference captions |  
| OOF | Out-of-fold; calibration or scoring evaluated on held-out folds rather than the same data used to fit the calibrator |  
| JSD | Jensen-Shannon divergence |  
| CHAIR_i | Mention-level CHAIR score: fraction of object mentions judged hallucinated |  
| CHAIR_s | Sentence-level CHAIR score: fraction of sentences containing at least one hallucinated mention |  
  
### Benchmarks And Targets Used Repeatedly  
  
| Name | What it means here | Structure in this report |  
|---|---|---|  
| POPE | Polling-based Object Probing Evaluation | Standardized yes/no object-presence benchmark |  
| POPE official adversarial 1K | Main binary benchmark for controlled groundedness discrimination | 1000 samples, 500 yes / 500 no, 73 queried objects, 167 unique images, one canonical question template; the adversarial negatives are absent-object queries meant to expose unsupported `Yes` answers |  
| `hallucinated_yes` | Model answered `Yes` on a ground-truth `No` POPE case | Primary hallucination-style target in the ablation program |  
| CHAIR | Caption Hallucination Assessment with Image Relevance | Free-form caption benchmark scored against COCO-style object annotations |  
| CHAIR-200 | The 200-image CHAIR slice used in the current repo | Main caption-style benchmark; hallucination flags come from object mentions that fail to match the COCO-style ground-truth object list, which is why annotation gaps later matter so much |  
  
## 2. Project Goal  
  
The codebase is trying to answer a central research problem:  
  
> How can we measure whether a VLM's generated token is genuinely image-conditioned, rather than a plausible continuation driven mostly by language priors?  
  
The working philosophy of the repo is that **output correctness is not enough**. A model can be correct for the wrong reason, and a model can hallucinate while still being strongly influenced by the image. The project therefore focuses on intrinsic measurement rather than only task accuracy.  
  
At a high level, the codebase has been exploring the following hypothesis:  
  
> A token's visual grounding can be estimated from the model's counterfactual sensitivity to removing or altering image evidence, and this sensitivity can be decomposed into state, decision, and causal components.  
  
## 3. Main Research Questions  
  
### 3.1 Primary Questions  
  
- Can visual grounding be measured directly from internal activations and probabilities under a real-vs-null protocol?  
- Can intrinsic grounding scores distinguish grounded outputs from hallucinated or prior-driven outputs?  
- Can grounding be separated into representational, decision-level, and causal notions rather than collapsed into one score too early?  
- Can intrinsic grounding reveal failure modes that ordinary accuracy misses?  
  
### 3.2 Micro-Questions Explored In The Codebase  
  
- What is the right **null baseline** for removing image evidence?  
- Should comparisons be made in **raw Layer-32 space**, whitened space, projection space, or some other basis?  
- Which comparison operator is most useful: cosine, dot, l2-derived, divergence-based, or something else?  
- Should signals be treated as **raw values** or **distributions**?  
- Which aggregation functions are meaningful: `max`, `var`, `entropy`, `range`, top-k summaries, or cross-track products?  
- Can a signal be judged by how well it separates meaningful tokens from filler tokens or punctuation?  
- Can grounding metrics predict hallucinations on benchmark datasets such as POPE and CHAIR?  
- Can patch support be localized to meaningful image regions?  
- Can a stronger patch-evidence object improve the original pipeline?  
  
### 3.3 Working Hypotheses Across The Project  
  
The codebase has not been exploring a single hypothesis in isolation. Instead, several working hypotheses recur across the notebooks, ablations, and reporting docs:  
  
- **H1:** A genuinely grounded token should change measurably when visual evidence is removed.  
- **H2:** A useful grounding signal should separate visually meaningful tokens from punctuation, filler tokens, or structurally weak tokens.  
- **H3:** A causal support mask derived from the intrinsic signal should matter more than a matched random intervention.  
- **H4:** Methodological choices such as null baseline, vector space, kernel, and aggregation strongly affect whether the signal is useful.  
- **H5:** Intrinsic grounding should reveal something that plain model accuracy does not, especially on hallucination-like or accidentally-correct cases.  
- **H6:** A better patch-evidence object may improve the interpretability and reliability of the overall grounding story.  
  
### 3.4 Concrete Micro-Questions In Working Form  
  
The project often progressed by repeatedly asking a smaller set of concrete engineering-research questions. Those micro-questions were usually what drove new notebooks, ablations, or redesigns:  
  
| Micro-question | Why it mattered | Main places it was explored |  
|---|---|---|  
| What should the null condition be? | The real-vs-null interpretation is only as good as the "no evidence" baseline | Stage A ablations, technical reports, `experimental_protocol.md` |  
| Should the signal live in raw or transformed space? | Space choice can either preserve or wash out discriminative structure | Stage B/C/D ablations, state notebooks, V2/V3 line |  
| Are we comparing vectors, distributions, or both? | Different comparison objects encode different notions of grounding | notebook deep dives, benchmark reports, GT-free branch |  
| Which kernels and reductions are meaningful? | Aggregation determines whether patch-level structure survives into a useful token/sample score | Stage C/D ablations, metric sweeps, report docs |  
| Which benchmark target should be treated as primary? | Target choice changes what "good grounding" means empirically | POPE docs, CHAIR docs, ablation reports |  
| Should `hallucinated_yes` be the main absent-object target? | It best matches the codebase's core hallucination-style question | Stage B/C/D results, POPE-facing reporting |  
| Can CHAIR be trusted as hallucination truth? | Many earlier conclusions depended on this assumption | CHAIR report, audit doc, case-study notebooks |  
| How should subword scores be merged into semantic units? | Many interpretations need word- or mention-level support rather than subword fragments | protocol docs, notebook analyses, GT-free branch |  
| How should nearby function words be treated? | Visual support can spill into articles or neighboring tokens | notebook reviews, token-selectivity planning |  
| Can a better patch-evidence object improve the entire pipeline? | The original signal may be limited by a weak image-side support definition | V2/V3/V3A/V3B/V3C docs and notebooks |  
  
## 4. High-Level Method  
  
The stable baseline method in this repo is the intrinsic grounding stack documented in `docs/GROUNDING_METHODOLOGY.md`, `docs/TECHNICAL_IMPLEMENTATION_REPORT_ALIGNED.md`, and the legacy snapshot `archive/docs/TECHNICAL_IMPLEMENTATION_REPORT.md`.  
  
The method uses one shared pipeline and one shared run structure:  
  
1\. Generate a reference answer on the real image.  
2\. Re-run the model under teacher forcing on the same answer sequence with:  
 - the real image  
 - a null visual baseline  
3\. Extract token states, patch states, logits, and intervention artifacts.  
4\. Compute three families of intrinsic measurements:  
 - **State grounding** from hidden-state / patch-profile changes  
 - **Decision grounding** from probability, rank, and concept-footprint changes  
 - **Causal grounding** from targeted patch ablation effects  
  
This framework is built around a counterfactual principle:  
  
> if a token is genuinely grounded in visual content, removing or degrading image evidence should change its internal representation, its decision distribution, or the causal effect of ablating the relevant support.  
  
The current protocol-facing metric set is summarized below. These five metrics are the reduced, report-facing set, although the codebase contains a broader implementation-native metric inventory.  
  
| Metric | Short definition | Reader intuition |  
|---|---|---|  
| `state_delta_var` | Variance across patches of the token's real-vs-null state-difference profile | Higher means the hidden-state change is spatially concentrated rather than flat |  
| `decision_delta_p` | Probability lift of the generated token under the real image relative to the null image | Higher means the image makes the chosen token more likely |  
| `dec_dp_x_cvar` | `decision_delta_p` multiplied by the spatial variance of the token's concept footprint | High only when the image both boosts the token and localizes concept support |  
| `causal_rel_drop` | Targeted-ablation log-probability drop normalized by the token's real-image log-probability magnitude | Higher means removing the support patches explains a larger share of the model's confidence |  
| `specificity_margin` | Targeted-ablation drop minus the mean matched random-control drop | Higher means the chosen support patches matter more than a generic patch removal of the same size |  
  
The most common shorthand used later in the report is:  
  
| Shorthand | Meaning |  
|---|---|  
| `N0` | `dataset_mean_patch`, the frozen global null baseline from Stage A |  
| `B2_S0_raw` | Stage-B raw Layer-32 condition with no whitening |  
| `B2_S1_all` | Whitening fit on all available vector families |  
| `B2_S1_bal` | Whitening fit on a balanced sample from each vector family |  
  
\![Three-track intrinsic grounding pipeline](figures/report_three_track_pipeline.png)  
  
*Current generated figure: This schematic compresses the core method into one view. A reference answer is generated on the real image, then replayed under paired real and null conditions with teacher forcing. The resulting shared extractions feed the three complementary tracks: state grounding for representational sensitivity, decision grounding for token-choice dependence, and causal grounding for necessity under targeted ablation.*  
  
\![Run artifact flow](figures/report_artifact_flow.png)  
  
*Current generated figure: This artifact-flow view makes the implementation contract concrete. Each run stores local evidence under `samples/\<sample_id>/`, run-wide scoring tables under `results/`, and shared tensors under `references/`. That structure is what allows the same run to support benchmark scoring, GT-free judge alignment, notebook inspection, and later reporting without redefining the metrics each time.*  
  
## 5. Evolution Of The Research Program  
  
### Chronology At A Glance  
  
| Date / phase | Representative documents | What changed |  
|---|---|---|  
| Late Feb 2026 | early POC notebooks, initial repo docs, GT-free planning seed | The repo establishes the intrinsic grounding idea and the first notebook-led proof-of-concept workflow |  
| 2026-02-27 | technical reports, methodology docs, early Typst sources | The project becomes more formal, with explicit mathematical and implementation framing |  
| 2026-03-02 | CHAIR experiment docs, CHAIR results, CHAIR audit materials | Benchmark evaluation expands and starts exposing problems with naive hallucination labels |  
| 2026-03-05 | POPE/CHAIR publication-grade report, metric-reduction report, deeper review notebooks | The benchmark line and GT-free line both become substantially more mature |  
| 2026-03-09 | Stage A/B/C/D reviews, Level 2 protocol materials | The baseline ablation program freezes key methodological choices |  
| 2026-03-10 | documentation audit and project-record materials | The repo adopts a clearer evidence hierarchy and documentation structure |  
| 2026-03-16 | V2/V3 docs and sample-review notebooks | A distinct frontier branch emerges around projection and patch-evidence reformulation |  
| 2026-03-19 | experimental protocol, implementation plan, V3A/V3B/V3C docs | The project becomes more paper-oriented and explicit about validation claims |  
| 2026-03-20 | reproducibility, setup, and data docs | The codebase becomes easier for others to run and interpret |  
| 2026-03-25 | method paper blueprint and interactive single-sample notebook | The focus shifts toward consolidation, presentation, and interactive analysis |  
  
\![Research evolution timeline](figures/report_research_timeline.png)  
  
*Current generated figure: This timeline emphasizes the main turning points in the repo: formulation of the intrinsic-grounding stack, benchmark maturation and ablation freeze, emergence of the V2/V3 frontier branch, and the later shift toward validation design, reproducibility, and collaborator-facing consolidation.*  
  
## 5.1 Phase I: Core Method Formulation  
  
The project begins with the intrinsic grounding formulation itself. The initial goal was to define grounding as **counterfactual real-vs-null sensitivity** inside the model rather than only as output correctness. This produced the three-track stack:  
  
- state grounding  
- decision grounding  
- causal grounding  
  
The early technical documents focus on making this mathematically precise and implementation-faithful. The canonical method view lives in `docs/GROUNDING_METHODOLOGY.md`, while the deeper derivations and implementation contracts live in the technical reports.  
  
### What This Phase Was Testing  
  
- Is there a coherent mathematical formulation of intrinsic grounding?  
- Can grounding be expressed as a shared pipeline rather than unrelated scripts?  
- Can token-level grounding be linked to patch-level evidence in a tractable way?  
  
### Main Outcome  
  
This phase produced the stable baseline architecture of the project and the artifact contracts that later notebooks and experiments depend on.  
  
## 5.2 Phase II: Notebook-Led Signal Inspection  
  
After the initial formulation, a large part of the work moved into notebook-driven inspection. These notebooks were used to understand what the signal actually looked like before committing to large benchmark claims.  
  
Representative notebooks include:  
  
- `archive/notebooks/notebooks/state_grounding_deep_review.ipynb`  
- `archive/notebooks/notebooks/stage4_critical_review.ipynb`  
- `archive/notebooks/notebooks/stage4B_hidden_state_drift.ipynb`  
- `archive/notebooks/notebooks/stage4_man_vs_period_deep_dive.ipynb`  
- early proof-of-concept notebooks for decision and causal grounding  
  
These `stage4` / `stage4B` notebook names belong to an earlier exploratory notebook naming scheme. They are not the same staging system as the later Stage A/B/C/D ablation program in Section 5.3.  
  
### What This Phase Was Testing  
  
- whether the stored tensors and formulas matched the intended math  
- whether patch heatmaps looked semantically plausible  
- whether content-bearing tokens behaved differently from punctuation or filler tokens  
- whether token-patch support could be made visually interpretable  
- whether specific token comparisons such as `"man"` vs `"."` exposed discriminative structure  
  
### Main Observations  
  
- The notebooks were crucial for tracing the full pipeline from raw tensors to summary metrics.  
- The project repeatedly used **mechanistic contrasts** such as content token vs punctuation to judge whether a metric was meaningful.  
- The notebooks surfaced non-trivial artifacts, including high early-token norms and unexpectedly strong values on some non-content tokens.  
- The "man vs period" style analyses appear to have been especially useful as a development-time sanity check for whether a signal was actually discriminative.  
  
### Why This Phase Matters  
  
Much of the codebase's later intuition about what counts as a good signal comes from these notebooks, not only from benchmark tables.  
  
### Notebook Figure Notation  
  
| Symbol | Meaning in the notebook figures |  
|---|---|  
| `S_real` | Token-by-patch similarity matrix under the real image condition |  
| `S_null` | Token-by-patch similarity matrix under the null image condition |  
| `P_real` | Patch-support distribution for a token under the real image condition |  
| `P_null` | Patch-support distribution for a token under the null image condition |  
| `A_pos` | Positive part of `P_real - P_null`; highlights patch support gained under the real image |  
  
\![State-grounding full-sequence heatmap](figures/report_state_grounding_heatmap.png)  
  
*Current extracted notebook figure: This full-sequence state-grounding view shows `S_real`, `S_null`, and their difference across all generated tokens and all image patches. The marked focus tokens make it easier to see where token-level image sensitivity becomes concentrated or diffuse across the sequence.*  
  
\![Man-vs-period patch overlays](figures/report_man_vs_period_overlays.png)  
  
*Current extracted notebook figure: This `▁man` vs `.` comparison shows how the visually meaningful noun and sentence-final punctuation differ under `P_real`, `P_null`, and `A_pos` overlays. It captures one of the notebook line's core development heuristics: a useful signal should assign more structured patch support to content-bearing tokens than to punctuation.*  
  
\![Hidden-state drift position correction](figures/report_hidden_state_drift_position.png)  
  
*Current extracted notebook figure: This hidden-state drift panel makes the sequence-position issue concrete by showing drift magnitude by token-position decile before and after correction. It supports one of the report's recurring observations: some early-token effects are real confounds that must be separated from genuine grounding behavior.*  
  
## 5.3 Phase III: Systematic Ablation Program  
  
Once the project had a viable baseline pipeline, the next step was to test which methodological choices actually mattered.  
  
This became the Stage A/B/C/D ablation program documented in:  
  
- `archive/docs/experiments/STAGE_A_ABLATIONS_COMPREHENSIVE_REVIEW.md`  
- `archive/docs/experiments/STAGE_B_ABLATIONS_COMPREHENSIVE_REVIEW.md`  
- `archive/docs/experiments/STAGE_BCD_ABLATIONS_RIGOROUS_RESULTS_ANALYSIS.md`  
  
### Stage A: Null Baseline Selection  
  
The question here was: **what should count as the "no image evidence" condition?**  
  
Tested null strategies included:  
  
- dataset mean patch  
- per-image mean  
- white noise  
- patch shuffle  
- random-image replacement  
  
In the Stage A reports these are abbreviated `N0` through `N4`, with `N0 = dataset_mean_patch`.  
  
### Main Finding  
  
`dataset_mean_patch` (`N0`) emerged as the best baseline. In the Stage A review it achieved:  
  
- decision AUC `0.877`  
- causal AUC `0.669`  
  
The broad conclusion was that `dataset_mean_patch` removes image-specific evidence while preserving a stable reference geometry better than the alternatives.  
  
### Stage B: Space Treatment  
  
The next question was whether the signal should be computed in:  
  
- raw Layer-32 space  
- whitening built from all families  
- family-balanced whitening  
  
### Main Finding  
  
Raw space (`B2_S0_raw`, the Stage-B raw Layer-32 condition with no whitening) became the frozen baseline for the primary hallucination-style target. Whitening sometimes helped secondary targets, but not the main one.  
  
### Stage C/D: Kernel And Aggregation Sweeps  
  
The project then swept:  
  
- `cosine`  
- `dot`  
- `l2neg`  
- `bilinear_drift`  
  
along with many aggregation and metric families.  
  
### Main Finding  
  
Across the full kernel-space matrix, the strongest `hallucinated_yes` result was:  
  
- `dot + B2_S0_raw + dec_dp_x_cvar = 0.8871` AUC  
  
Here `hallucinated_yes` means a POPE example where the model answered `Yes` on a ground-truth `No` question, and `dec_dp_x_cvar` is the product of token probability lift and concept spatial variance.  
  
This is one of the most important freeze decisions in the repo. The ablation docs support a stable conclusion:  
  
- **raw remains the robust primary winner**  
- **decision interactions dominate the best hallucination detectors**  
- **causal metrics dominate many correctness-oriented targets**  
  
### Figures In This Draft  
  
\![Stage A null-baseline comparison](figures/report_stage_a_nulls.png)  
  
*Current generated figure: Stage A shows why `dataset_mean_patch` (`N0`) became the frozen baseline. It is the strongest decision-track null, remains competitive on the causal track, and preserves high null sanity at the same time.*  
  
\![Stage B/C/D primary-target winners](figures/report_stage_bcd_primary_winners.png)  
  
*Current generated figure: Across all four kernels, the primary `hallucinated_yes` winner stays in raw space (`B2_S0_raw`). The overall winner is `dot + dec_dp_x_cvar`, reinforcing the report's main freeze decision.*  
  
## 5.4 Phase IV: Benchmark Evaluation  
  
With a candidate baseline in place, the project moved to benchmark-oriented evaluation, especially on:  
  
- **Polling-based Object Probing Evaluation (POPE)** official adversarial 1K  
- **Caption Hallucination Assessment with Image Relevance (CHAIR)**-200  
  
The strongest benchmark narrative is in `archive/docs/experiments/reports/POPE_CHAIR_PUBLICATION_GRADE_RESULTS_ANALYSIS.md`.  
  
### Benchmark Guide  
  
| Benchmark or term | Meaning here | Why it matters |  
|---|---|---|  
| POPE official adversarial 1K | 1000 balanced yes/no object-presence questions with a fixed template; absent-object negatives are the adversarial half of the split | Clean controlled benchmark for direct task accuracy, ranking quality, and calibration |  
| `is_correct` | Model answer matches the POPE ground-truth label | General task-correctness target |  
| `hallucinated_yes` | Model answered `Yes` on a ground-truth `No` POPE case | Main hallucination-style ablation target |  
| CHAIR-200 | 200-image captioning sample evaluated against COCO-style object annotations; a mention is flagged when it does not match the ground-truth object list | Caption-style benchmark that later required audit correction |  
| CHAIR_i | Fraction of mentioned objects marked hallucinated | Mention-level caption hallucination summary |  
| CHAIR_s | Fraction of sentences containing at least one hallucinated mention | Sentence-level caption hallucination summary |  
  
### What This Phase Was Testing  
  
- Can intrinsic metrics discriminate hallucination-like failures on a standard benchmark?  
- How do intrinsic scores compare to model accuracy and calibration?  
- Are the signals practically useful, or only mechanistically interesting?  
  
### Main Findings On POPE  
  
- Direct task accuracy is `0.8300`.  
- The best single intrinsic POPE score is `causal_delta_logp_random` with ROC-AUC `0.7667`; here `random` means the targeted ablation effect is interpreted against matched random-control ablations.  
- The calibrated grounding score reaches out-of-fold (OOF) ROC-AUC `0.7658`; this score is a Platt-calibrated sample-level composite built from the three intrinsic families rather than a single raw metric.  
  
The practical conclusion is not that intrinsic grounding replaces task accuracy. Rather, the repo's conclusion is that intrinsic signals contain meaningful additional information, especially for ranking and triage.  
  
### Main Findings On CHAIR  
  
- CHAIR can produce decent ROC-AUC-style numbers for some intrinsic metrics.  
- The best CHAIR detector reported in the main benchmark doc is `decision_jsd_tau0.1` with ROC-AUC `0.7482`; this is the Jensen-Shannon divergence between real and null concept-footprint distributions at temperature `tau = 0.1`.  
- But this benchmark story changed dramatically after audit.  
  
### Current Limitation Of This Phase  
  
The benchmark story is informative but not sufficient on its own. POPE is narrow and template-heavy, while CHAIR turns out to be noisy enough that it cannot serve as a clean hallucination truth source without manual correction or an alternative judging strategy.  
  
### Figures In This Draft  
  
\![POPE-1K summary figure](figures/report_pope_summary.png)  
  
*Current generated figure: The direct yes/no baseline remains stronger than any single intrinsic score on POPE, but the strongest causal metric and the calibrated grounding composite both retain substantial discriminative value. This supports the report's narrower claim that grounding adds useful signal rather than replacing task performance.*  
  
## 5.5 Phase V: CHAIR Audit And Interpretation Correction  
  
One of the most important corrections in the entire project came from the manual CHAIR audit:  
  
- `archive/docs/experiments/audits/HALLUCINATION_AUDIT_200.md`  
  
### What This Phase Was Testing  
  
- Are CHAIR-flagged mentions actually true hallucinations?  
- How much of the benchmark signal is real model failure versus annotation noise or category mismatch?  
  
### Main Finding  
  
Only `13 / 80` CHAIR-flagged mentions, or `16.3%`, were classified as true fabrications.  
  
The rest were mostly:  
  
- GT annotation gaps  
- reasonable inference  
- misidentification of a real referent  
- category synonym or taxonomy mismatch  
  
### Why This Matters  
  
This forced a major reinterpretation:  
  
- CHAIR is useful as **diagnostic context**  
- CHAIR is **not** a clean standalone hallucination ground truth  
- image dependence and factual correctness must be treated as related but separate questions  
  
This is also consistent with the notebook case-study line, which repeatedly argues that many apparent hallucinations are better described as **image-driven perceptual errors** than as pure language-prior completions.  
  
### Figures In This Draft  
  
\![CHAIR audit taxonomy](figures/report_chair_audit_taxonomy.png)  
  
*Current generated figure: The CHAIR audit is dominated by GT gaps, plausible inference, and misidentification cases. Only `13 / 80` flagged mentions survive as true hallucinations, which is why CHAIR is treated as diagnostic context rather than clean ground truth.*  
  
\![Hallucination case study: shower in bathroom](figures/report_hallucination_case_shower.png)  
  
*Current extracted notebook figure: This case-study panel illustrates the report's broader audit interpretation. The model's mention is not well described as a pure language-prior fabrication; instead, it appears to be an image-driven perceptual error triggered by bathroom tile and fixture cues.*  
  
## 5.6 Phase VI: GT-Free Judge And Metric Reduction  
  
Another major branch in the repo tries to reduce dependence on benchmark annotations by introducing a multimodal judge.  
  
The key docs are:  
  
- `archive/docs/plans/GT_FREE_MULTIMODAL_JUDGE_PLAN.md`  
- `archive/docs/experiments/reports/METRIC_REDUCTION_200_RUN_REPORT.md`  
  
### What This Phase Was Testing  
  
- Can intrinsic metrics be aligned to claim-level present/absent labels produced from `image + generated answer` rather than only GT benchmark labels?  
- Can a smaller, better-organized metric set be identified?  
- Can a composite grounding index be learned from judged token labels?  
  
### Main Findings  
  
The 200-image metric-reduction run is a completed experiment. Its main outputs suggest:  
  
- a usable but still modest GT-free signal exists  
- family reduction and composite models can improve over single metrics from any one of the three intrinsic families: state, decision, and causal  
- the best grouped-CV logistic family combination in that report reaches ROC-AUC `0.6060`  
- the strongest non-linear models perform better, with Random Forest grouped-CV AUC around `0.6636`  
  
### Interpretation  
  
This line is meaningful and implemented, but it is not yet as strong or mature as the baseline POPE/ablation evidence. It should currently be treated as a promising secondary evaluation track.  
  
### Current Limitation Of This Phase  
  
This workstream reduces dependence on external benchmark labels, but the current evidence still shows moderate performance and incomplete maturity relative to the main benchmark line. It is best described as a strong supporting branch rather than the core evidentiary spine.  
  
### Figures In This Draft  
  
\![GT-free metric-reduction summary](figures/report_gtfree_metric_reduction.png)  
  
*Current generated figure: The GT-free line improves when it moves from single-family representatives to a three-family composite, with the grouped-CV logistic model reaching `0.6060` ROC-AUC. The stronger Random Forest and Gradient Boosting results suggest there is additional structure in the signals, but the report still treats the logistic family-combination result as the most stable report-facing summary.*  
  
## 5.7 Phase VII: Frontier V2 / V3 / V3A / V3B Line  
  
A later branch of the project shifts attention from the original intrinsic stack to the **patch-evidence object itself**.  
  
Representative docs:  
  
- `archive/docs/GroundingV2.md`  
- `archive/docs/GROUNDING_V3A_IMPLEMENTATION_REVIEW.md`  
- `archive/docs/GROUNDING_V3B_IMPLEMENTATION.md`  
- `archive/docs/groundingv3c.md`  
- `archive/docs/EXPERIMENT_RESULTS_REPORT.md`  
  
### V2  
  
V2 explores an orthogonal-projection replay view:  
  
- token-side change: `DeltaH`, the real-minus-null change in the focal token state  
- patch-side change: `DeltaV`, the real-minus-null change in patch states  
- grounding as how much token change lies in an image-specific patch-difference subspace  
  
This is conceptually cleaner than the older state formulation, but still global.  
  
### V3 / V3A  
  
V3 and V3A try to localize the signal by building a better image-side patch-evidence field. The main question becomes:  
  
> can we construct a calibrated patch-evidence object that reflects structured non-null visual information better than raw patch-difference magnitude?  
  
### V3A Main Observation  
  
The V3A review identifies several root problems:  
  
- heterogeneous null family  
- full-dimensional real whitening  
- under-selected null rank  
- missing per-position null normalization  
  
### V3B Main Observation  
  
V3B is explicitly a repair of those failures. The current acceptance-backed snapshot reports:  
  
- `gamma_b1`, the main B1 null-rejection calibration scale, reduced from about `1011` to `6.87`  
- null explained variance at selected rank increased from `7.2%` to `95.1%`  
- `gamma_a2`, an auxiliary residual-ratio calibration term, recovered from near-degenerate values to about `0.386`  
- current acceptance suite: `8/8` checks passing  
  
### Interpretation  
  
This branch has produced a serious improvement in calibration behavior, but it is still frontier-status because:  
  
- the null holdout is small  
- the current evidence is centered on `chair_200`  
- it has not yet replaced the benchmark-backed baseline stack  
  
### Figures In This Draft  
  
\![V3A to V3B calibration repair summary](figures/report_v3a_v3b_comparison.png)  
  
*Current generated figure: This comparison makes the frontier-branch improvement concrete. V3B sharply increases null variance capture, rejects far more null modes, collapses the inflated `gamma_B1` scale, and recovers `gamma_A2` from degeneracy. At the same time, the report keeps the branch in frontier status because these gains are still centered on `chair_200` and a small null holdout rather than broad benchmark closure.*  
  
## 5.8 Phase VIII: Current Validation Agenda  
  
The most formal expression of current future work is in:  
  
- `experimental_protocol.md`  
- `EXPERIMENTAL_IMPLEMENTATION.md`  
- `method_paper_blueprint.md`  
  
These docs move the project toward a more explicit validation program built around:  
  
- evidence monotonicity  
- token selectivity  
- causal faithfulness  
- fragility under perturbation  
- external correspondence  
- spatial correspondence / localization  
- transfer to another model  
  
This is effectively the next research stage: moving from "we have a promising instrument and ablation-backed configuration" to "we have property-matched validation of what the instrument measures."  
  
Additional validation-roadmap figures are tracked in Section 8 rather than embedded here, because the underlying experiments are mostly still planned or only partially scaffolded.  
  
## 6. Progress Snapshot Across Workstreams  
  
| Workstream | Main question | Current status | Main takeaway |  
|---|---|---|---|  
| Core intrinsic method | Can grounding be measured by real-vs-null sensitivity? | Complete baseline | Three-track stack is implemented and documented |  
| Notebook deep dives | Does the signal behave mechanistically as expected? | Complete exploratory line | Helped debug formulas, patch support, and token behavior |  
| Stage A ablations | What null baseline should be used? | Complete | `dataset_mean_patch` frozen as baseline |  
| Stage B/C/D ablations | Which space/kernel/aggregation choices work best? | Complete | `B2_S0_raw` frozen for primary hallucination target; `dec_dp_x_cvar` is top raw detector |  
| POPE 1K | Can intrinsic signals discriminate hallucination-like failures? | Complete | Causal signals are strongest single-family performers |  
| CHAIR-200 | Do intrinsic signals align with caption hallucination labels? | Complete but reinterpreted | Useful only with audit-aware caution |  
| CHAIR audit | Are CHAIR flags actually true hallucinations? | Complete | Most CHAIR flags are not true fabrications |  
| GT-free judge | Can intrinsic metrics align with judge-derived labels? | Complete secondary line | Promising but less mature than baseline benchmark line |  
| V2/V3/V3B frontier | Can the patch-evidence object itself be improved? | Active | V3B materially improves calibration behavior but is not yet fully closed |  
| Formal validation protocol | Can the method satisfy stronger measurement claims? | Planned / partially scaffolded | High-priority next stage |  
  
## 7. Main Findings And Observations  
  
## 7.1 Strongest Supported Findings  
  
- The three-track intrinsic grounding pipeline is real, implemented, and methodologically coherent.  
- `dataset_mean_patch` is the strongest tested null baseline in the main ablation line.  
- Raw Layer-32 space remains the best primary choice for the main hallucination-style target.  
- Decision-family interaction metrics are strongest for the main hallucination target under the frozen raw configuration.  
- Causal metrics are the strongest single-family benchmark performers on POPE official 1K.  
- CHAIR cannot be interpreted naively as a hallucination prevalence metric.  
  
## 7.2 Important Notebook-Driven Observations  
  
- Heatmaps and token-patch traces were central to the project's development, not just presentation.  
- The "man vs period" style comparison reflects a deeper recurring idea in the codebase: a useful signal should separate visually meaningful tokens from structurally weak or non-content tokens.  
- Some generation-position artifacts remain unresolved, especially unusually high values or norms near the start of the generated answer.  
- The notebooks support a recurring interpretation that some so-called hallucinations are actually **perceptual misreadings** of real image content.  
  
## 7.3 Findings That Changed The Project's Direction  
  
- The CHAIR audit changed the interpretation of the benchmark line.  
- The ablation program froze the baseline methodology rather than leaving it open-ended.  
- The V3A review revealed that a visually appealing patch-evidence idea could still fail for calibration reasons.  
- The V3B repair line emerged because notebook and calibration inspection exposed structural, not merely cosmetic, issues.  
  
## 8. Figure Plan  
  
Only figures that are actually embedded in the body of the report appear in Sections 4 and 5 above. This figure plan tracks both the generated assets already in the draft and additional optional figures that remain unmade.  
  
### 8.1 Conceptual Figures  
  
- **Figure 1 [generated]:** Three-track grounding pipeline schematic  
 - File: `docs/figures/report_three_track_pipeline.png`  
 - Source: `docs/GROUNDING_METHODOLOGY.md` and `docs/TECHNICAL_IMPLEMENTATION_REPORT_ALIGNED.md`  
- **Figure 2 [generated]:** Timeline of research phases and workstreams  
 - File: `docs/figures/report_research_timeline.png`  
 - Source: this report plus `archive/docs/PROJECT_RECORD.md`  
- **Figure 3 [generated]:** Run artifact flow through `samples/`, `results/`, and `references/`  
 - File: `docs/figures/report_artifact_flow.png`  
 - Source: `docs/GROUNDING_METHODOLOGY.md`  
  
### 8.2 Existing Or Easily Recoverable Experimental Figures  
  
- **Figure 4 [generated]:** POPE summary of strongest metrics and calibrated score  
 - File: `docs/figures/report_pope_summary.png`  
 - Source: `archive/docs/experiments/reports/POPE_CHAIR_PUBLICATION_GRADE_RESULTS_ANALYSIS.md`  
- **Figure 5 [generated]:** CHAIR audit taxonomy panel  
 - File: `docs/figures/report_chair_audit_taxonomy.png`  
 - Source: `archive/docs/experiments/reports/POPE_CHAIR_PUBLICATION_GRADE_RESULTS_ANALYSIS.md` and `archive/docs/experiments/audits/HALLUCINATION_AUDIT_200.md`  
- **Figure 6 [generated]:** Stage A null-ablation comparison  
 - File: `docs/figures/report_stage_a_nulls.png`  
 - Source: `archive/docs/experiments/STAGE_A_ABLATIONS_COMPREHENSIVE_REVIEW.md`  
- **Figure 7 [generated]:** Stage B/C/D primary-target winner summary  
 - File: `docs/figures/report_stage_bcd_primary_winners.png`  
 - Source: `archive/docs/experiments/STAGE_BCD_ABLATIONS_RIGOROUS_RESULTS_ANALYSIS.md`  
- **Figure 8 [generated]:** GT-free metric-reduction summary  
 - File: `docs/figures/report_gtfree_metric_reduction.png`  
 - Source: `archive/docs/experiments/reports/METRIC_REDUCTION_200_RUN_REPORT.md`  
- **Figure 9 [generated]:** V3A -> V3B calibration repair summary  
 - File: `docs/figures/report_v3a_v3b_comparison.png`  
 - Source: `archive/docs/EXPERIMENT_RESULTS_REPORT.md`  
  
### 8.3 Notebook-Driven Qualitative Figures  
  
- **Figure 10 [generated]:** Full-sequence state-grounding heatmap  
 - File: `docs/figures/report_state_grounding_heatmap.png`  
 - Source: `archive/notebooks/notebooks/state_grounding_deep_review.ipynb`  
- **Figure 11 [generated]:** `▁man` vs `.` patch-overlay comparison  
 - File: `docs/figures/report_man_vs_period_overlays.png`  
 - Source: `archive/notebooks/notebooks/stage4_man_vs_period_deep_dive.ipynb`  
- **Figure 12 [generated]:** Hidden-state drift position-correction view  
 - File: `docs/figures/report_hidden_state_drift_position.png`  
 - Source: `archive/notebooks/notebooks/stage4B_hidden_state_drift.ipynb`  
- **Figure 13 [generated]:** Hallucination case study panel  
 - File: `docs/figures/report_hallucination_case_shower.png`  
 - Source: `archive/notebooks/notebooks/hallucination_case_studies.ipynb`  
- **Figure 14:** V3A versus V3B qualitative calibration comparison  
 - Source: `archive/notebooks/notebooks/grounding_v3a_sample_review.ipynb` and `archive/notebooks/notebooks/grounding_v3b_acceptance_tests.ipynb`  
- **Figure 15:** Current interactive single-sample object / patch tracking example  
 - Source: `notebooks/single_sample_grounding_interactive.ipynb`  
  
### 8.4 Figures That Are Still Better Treated As Planned  
  
- **Planned figure:** Bounding-box overlap / spatial correspondence summary  
 - Source target: `method_paper_blueprint.md`  
- **Planned figure:** Corruption ladder plots  
 - Source target: `experimental_protocol.md`  
- **Planned figure:** Fragility-under-perturbation quartile plots  
 - Source target: `experimental_protocol.md`  
- **Planned figure:** Transfer-model comparison plots  
 - Source target: `experimental_protocol.md`  
  
## 9. Open Questions  
  
## 9.1 Baselines And Comparative Value  
  
- How much better is the full grounding framework than simple logit-difference or confidence baselines?  
- When is the extra complexity of the full three-track method justified?  
- What is the right baseline notion of "good" AUC for grounding, as opposed to task performance?  
  
## 9.2 Interpretation And Aggregation  
  
- How should subword-level scores be merged into word-level or mention-level decisions?  
- How should function words near visually meaningful spans be treated?  
- Do high early-sequence values indicate true grounding, generic generation artifacts, or something else?  
- Can content-vs-function discrimination be done robustly at scale?  
  
## 9.3 Spatial And Mechanistic Questions  
  
- Do high-support patches align with semantically correct object regions?  
- How should occlusion and corruption be used to validate the signal?  
- Is the causal support mask specifically meaningful, or only one useful approximation?  
  
## 9.4 Frontier-Branch Questions  
  
- Will V3B hold up under larger holdouts and more datasets?  
- Will improved patch-evidence calibration translate into stronger benchmark behavior?  
- What exactly should V3C become, and how should it connect back to token-level grounding?  
  
## 9.5 Specific Unresolved Analytical Issues From The Current Codebase  
  
These are recurring issues that show up across the notebooks, benchmark reports, and planned-work docs. They are better treated as live analytical problems than as minor cleanup tasks.  
  
| Issue | Why it remains unresolved | Why it matters |  
|---|---|---|  
| Baseline comparison against simple logit-difference methods | The need is recognized, but the comparison is not yet standardized across the main reports | Without it, the framework can look more complex than necessary |  
| Relationship between model accuracy and grounding AUC | The repo conceptually separates them, but the operational relationship is still incomplete | This is central to arguing that grounding adds information beyond correctness |  
| Token-class analysis at scale | Content-vs-function discrimination is attractive, but hard to do robustly on free-form outputs | This affects claims about semantic selectivity |  
| Subword aggregation and phrase-level grounding | Many outputs are naturally phrase-level, while many current signals are token- or subword-level | This affects both interpretability and evaluation |  
| Support spillover onto nearby function words | Articles and adjacent tokens can inherit strong signal from visually meaningful nouns | This complicates naive content-vs-noncontent interpretations |  
| Early-token norm / sequence-position artifacts | Several notebooks surface unusually strong values near the start of generation | These may be real signal, generic generation artifacts, or a mixture |  
| Spatial alignment and occlusion validation | The repo is moving toward localization and corruption tests, but the story is not yet closed | This matters for showing the signal is genuinely visual rather than only predictive |  
| Whether V3B should replace or supplement the baseline stack | V3B looks much better in calibration terms, but is not yet benchmark-closed | This affects the future architecture of the project itself |  
  
## 10. Next Work  
  
The most important near-term work appears to be:  
  
1\. Run property-matched validation experiments from `experimental_protocol.md`, especially:  
 - fragility under perturbation  
 - evidence monotonicity under corruption  
 - token selectivity  
 - spatial correspondence  
2\. Strengthen the baseline story with explicit comparisons against simpler logit-based baselines.  
3\. Turn the strongest notebook observations into reproducible scripts or report-quality figures.  
4\. Decide whether V3B should remain a frontier branch or become part of the main benchmarked story.  
5\. Clarify the role of the GT-free line: supporting evaluation branch versus central project pillar.  
  
## 11. Appendix: Repository Source Map (Optional)  
  
The report above is intended to stand on its own. This appendix is only useful for internal readers who already have access to the repository and want to trace claims back to source files; it can be omitted in an external-facing export.  
  
### Canonical Method Docs  
  
- `docs/GROUNDING_METHODOLOGY.md`  
- `docs/TECHNICAL_IMPLEMENTATION_REPORT_ALIGNED.md`  
- `archive/docs/TECHNICAL_IMPLEMENTATION_REPORT.md`  
  
### Main Evidence Docs  
  
- `archive/docs/PROJECT_RECORD.md`  
- `archive/docs/experiments/reports/POPE_CHAIR_PUBLICATION_GRADE_RESULTS_ANALYSIS.md`  
- `archive/docs/experiments/STAGE_A_ABLATIONS_COMPREHENSIVE_REVIEW.md`  
- `archive/docs/experiments/STAGE_B_ABLATIONS_COMPREHENSIVE_REVIEW.md`  
- `archive/docs/experiments/STAGE_BCD_ABLATIONS_RIGOROUS_RESULTS_ANALYSIS.md`  
- `archive/docs/experiments/audits/HALLUCINATION_AUDIT_200.md`  
  
### GT-Free And Secondary Evidence  
  
- `archive/docs/plans/GT_FREE_MULTIMODAL_JUDGE_PLAN.md`  
- `archive/docs/experiments/reports/METRIC_REDUCTION_200_RUN_REPORT.md`  
  
### Frontier V2/V3 Line  
  
- `archive/docs/EXPERIMENT_RESULTS_REPORT.md`  
- `archive/docs/GroundingV2.md`  
- `archive/docs/GROUNDING_V3A_IMPLEMENTATION_REVIEW.md`  
- `archive/docs/GROUNDING_V3B_IMPLEMENTATION.md`  
- `archive/docs/groundingv3c.md`  
  
### Validation And Future-Work Docs  
  
- `experimental_protocol.md`  
- `EXPERIMENTAL_IMPLEMENTATION.md`  
- `method_paper_blueprint.md`  
  
### Representative Notebooks  
  
- `archive/notebooks/notebooks/state_grounding_deep_review.ipynb`  
- `archive/notebooks/notebooks/stage4_critical_review.ipynb`  
- `archive/notebooks/notebooks/stage4B_hidden_state_drift.ipynb`  
- `archive/notebooks/notebooks/stage4_man_vs_period_deep_dive.ipynb`  
- `archive/notebooks/notebooks/metric_reduction_200_results.ipynb`  
- `archive/notebooks/notebooks/hallucination_case_studies.ipynb`  
- `archive/notebooks/notebooks/grounding_v2_sample_review.ipynb`  
- `archive/notebooks/notebooks/grounding_v3a_sample_review.ipynb`  
- `archive/notebooks/notebooks/grounding_v3b_acceptance_tests.ipynb`  
- `notebooks/single_sample_grounding_interactive.ipynb`  
  
## 12. Recommended Finalization Options  
  
The next editorial pass should focus less on coverage and more on packaging:  
  
- decide whether this version should remain an internal research memo or be tightened into an external-facing narrative  
- trim or keep the optional repository appendix depending on whether the audience has repo access  
- move some metric-shorthand detail into an appendix if a shorter collaborator memo is preferred  
- add a final prose-only polish pass so the figure captions and section transitions sound more uniform  