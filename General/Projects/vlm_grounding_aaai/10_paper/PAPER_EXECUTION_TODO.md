# Measuring Visual Grounding in Vision-Language Models
## Paper Execution TODO

Based on: `PAPER_TRACK_FROZEN_v2.md`
Status date: March 2026
Purpose: convert the frozen paper track into an execution checklist.

---

# 0. Operating rule

This todo list follows the frozen paper track exactly.
- keep: null-vs-real stable baseline, state/decision/causal tracks, POPE primary, CHAIR secondary diagnostic only
- exclude: DeltaV / V2 / V3 / frontier branches, layerwise dispersion, grid-aware redesign, training-objective ideas, bbox localization as headline claim

---

# 1. Paper-track constants (do not change during execution)

## 1.1 Primary paper target
- Primary benchmark: **POPE official adversarial 1K**
- Primary evaluation target: **`hallucinated_yes` vs `correct`**
- Primary result line for the paper: **ablation-line**
- Context-only result line: **benchmark-line**

## 1.2 Frozen method choices
- Model: **LLaVA-1.5-7B**
- Null: **N0 = dataset-mean patch**
- Space: **raw Layer-32**
- Decomposition: **state / decision / causal**
- Random controls: **K = 3 matched random masks**

## 1.3 Core report-facing metrics
### Decision
- `dec_dp_x_cvar`
- `dec_log_p_ratio`
- `dec_delta_p`
- `dec_p_real`

### Causal
- `cau_rel_drop`
- `cau_specificity_margin`
- `cau_targeted_vs_random`

### State
- `state_delta_var`
- best single state metric from rerun summary

---

# 2. What already exists and must be rerun / regenerated cleanly

## 2.1 Full POPE ablation-line regeneration
- [ ] rerun full POPE ablation-line extraction on official adversarial 1K
- [ ] recompute all report-facing metrics from one consistent artifact path
- [ ] regenerate champion vs baseline AUC table
- [ ] regenerate ROC curves
- [ ] regenerate PR curves
- [ ] regenerate score histograms for `hallucinated_yes` vs `correct`
- [ ] save one clean final artifact folder for paper figures/tables

### Outputs required
- [ ] `pope_ablation_metric_auc_summary.csv`
- [ ] `pope_ablation_threshold_metrics.csv`
- [ ] `pope_ablation_roc_curves.*`
- [ ] `pope_ablation_pr_curves.*`
- [ ] `pope_ablation_score_histograms.*`

## 2.2 Benchmark-line context regeneration
- [ ] rerun / re-export POPE benchmark-line metrics
- [ ] confirm `causal_delta_logp_random = 0.7667` path (or updated rerun value)
- [ ] confirm `decision_p_real` benchmark-line value path
- [ ] confirm direct yes/no accuracy path
- [ ] create one reconciliation table: ablation-line vs benchmark-line

### Outputs required
- [ ] `pope_benchmark_line_summary.csv`
- [ ] `pope_result_line_reconciliation_table.md`

## 2.3 Null-choice regeneration
- [ ] rerun N0 / N1 / N2 / N3 / N4 comparison
- [ ] report the main decision metric under each null
- [ ] verify N0 remains the preferred null

## 2.4 Stage-B / space-choice regeneration
- [ ] rerun raw vs whitening / transformed-space comparison only insofar as needed to justify frozen choice
- [ ] export one final "frozen design decision" table

## 2.5 Causal pipeline regeneration (existing directional result)
- [ ] rerun targeted ablation on POPE-200 subset
- [ ] rerun matched random controls
- [ ] regenerate causal-drop tables
- [ ] regenerate targeted vs random bar chart
- [ ] regenerate state-vs-causal scatter

### Outputs required
- [ ] `causal_targeted_vs_random_summary.csv`
- [ ] `causal_per_sample_results.csv`
- [ ] `causal_validation_figure_bar.*`
- [ ] `causal_validation_scatter.*`

## 2.6 CHAIR secondary diagnostic regeneration
- [ ] rerun top CHAIR-aligned metric summary
- [ ] rerun precision / recall / F1 at best operating point
- [ ] regenerate compact CHAIR diagnostic table

---

# 3. What is genuinely new and must be done

## 3.1 Experiment C — Approach 1 (highest priority)
**Evidence removal on correct cases**

- [ ] identify all correct POPE answers
- [ ] compute `dec_dp_x_cvar` quartiles on correct-only subset
- [ ] define low-grounding group (Q1) and high-grounding group (Q4)
- [ ] check whether existing causal artifacts already include correct-answer samples
- [ ] if not, extend causal pipeline to correct-answer subset
- [ ] ablate support patches for correct-answer subset
- [ ] measure degradation: log-probability drop, answer persistence rate, answer flip rate
- [ ] compare low-grounding vs high-grounding groups
- [ ] compute significance and effect size
- [ ] curate 2–3 worked examples

### Outputs required
- [ ] `correct_only_evidence_removal_results.csv`
- [ ] `correct_only_quartile_degradation_table.csv`
- [ ] `correct_only_effect_sizes.csv`
- [ ] `correct_only_examples/`

## 3.2 H3 finalization (statistics only)
**Formal causal significance reporting**

- [ ] paired t-test: targeted vs random ablation
- [ ] compute Cohen's d
- [ ] bootstrap CI for mean targeted-random difference
- [ ] add significance labels to bar chart

## 3.3 H2 token selectivity
**Visual noun / attribute / function-word validation**

- [ ] sample 100 POPE generated answers
- [ ] freeze the sampled subset
- [ ] annotate tokens using V / A / F rubric
- [ ] compute metric distributions by token class
- [ ] run Wilcoxon comparisons
- [ ] compute V/F ratio

### Outputs required
- [ ] `token_selectivity_annotations.csv`
- [ ] `token_selectivity_tests.csv`
- [ ] `token_selectivity_plot.*`

## 3.4 Cross-track convergence
- [ ] compute Spearman rho between representative state / decision / causal metrics
- [ ] compute overall correlation matrix
- [ ] optionally compute by subset (`hallucinated_yes`, `correct_yes`, `correct_no`)
- [ ] write interpretation note: compatible evidence vs complementary evidence

## 3.5 Worked examples for reviewer-proofing
**Ratio-vs-instrument qualitative divergence examples**

- [ ] identify cases where ratio is high but support is diffuse
- [ ] identify cases where ratio is high and support is concentrated + causally supported
- [ ] generate 2–4 compact worked examples

---

# 4. Reading tasks

## 4.1 Read and extract from your own core docs
- [ ] re-read `PAPER_TRACK_FROZEN_v2.md`
- [ ] re-read canonical methodology document
- [ ] re-read technical implementation report
- [ ] re-read research progress report
- [ ] re-read publication-grade POPE + CHAIR report

## 4.2 Reviewer-question prep reading
Prepare notes for likely reviewer questions:
- [ ] why not just use `dec_log_p_ratio`?
- [ ] why teacher forcing?
- [ ] why only L32?
- [ ] why only one model?
- [ ] why is CHAIR secondary only?
- [ ] why is POPE enough for the main validation?

---

# 5. Writing tasks

## 5.2 Section drafting order (first-pass)
- [ ] Section 3: Method
- [ ] Section 4: Experimental Setup
- [ ] Section 5.1: Benchmark Discrimination
- [ ] Section 5.2: Causal Validation
- [ ] Section 6: Discussion
- [ ] Section 1: Introduction
- [ ] Section 2: Related Work
- [ ] Section 5.3: Beyond-Accuracy Validation (after Experiment C)
- [ ] Section 7: Limitations
- [ ] Section 8: Conclusion

## 5.3 Specific writing deliverables
- [ ] Abstract v1
- [ ] Intro problem statement v1
- [ ] Contributions list v1
- [ ] Method section v1
- [ ] POPE results subsection v1
- [ ] Causal validation subsection v1
- [ ] Beyond-accuracy subsection placeholder
- [ ] Discussion paragraph on ratio baseline
- [ ] Discussion paragraph on CHAIR limits
- [ ] Limitations section v1

---

# 6. Sequencing / dependency order

## Phase 1 — regeneration and cleanup
1. [ ] rerun POPE ablation-line
2. [ ] rerun benchmark-line context
3. [ ] rerun null-ablation summary
4. [ ] rerun space-choice summary
5. [ ] rerun causal validation artifacts

## Phase 2 — paper-blocking new work
6. [ ] Experiment C Approach 1
7. [ ] H3 significance finalization
8. [ ] H2 token selectivity
9. [ ] cross-track convergence
10. [ ] worked examples

## Phase 3 — writing lock-in
11. [ ] draft Method and Setup
12. [ ] draft Results 5.1 and 5.2
13. [ ] draft Discussion and Limitations
14. [ ] integrate Experiment C once complete
15. [ ] write Abstract / Introduction last

## Phase 4 — optional strengthening
16. [ ] Experiment C Approach 2 fragility
17. [ ] exploratory bbox-IoU note for discussion only

---

# 7. Simple project board view

## A. Already run, needs rerun / clean regeneration
- [ ] POPE ablation-line full scorecard
- [ ] benchmark-line context table
- [ ] null-ablation table
- [ ] space/kernel ablation summary
- [ ] causal validation artifact bundle
- [ ] CHAIR secondary summary

## B. New work that blocks the paper
- [ ] Experiment C Approach 1
- [ ] H3 significance stats
- [ ] H2 token selectivity
- [ ] cross-track convergence
- [ ] worked examples

## C. New work that strengthens but does not block
- [ ] Experiment C Approach 2 fragility
- [ ] exploratory spatial-IoU discussion asset

## D. Reading
- [ ] core-doc reread
- [ ] related-work positioning notes
- [ ] reviewer-QA notes

## E. Writing
- [ ] paper skeleton
- [ ] section drafts
- [ ] figure/table caption drafting
- [ ] appendix inventory

---

# 8. Definition of done

The paper-track execution phase is done when:
- [ ] all rerun artifacts exist under one clean paper-results path
- [ ] Experiment C Approach 1 is complete
- [ ] H3 significance is finalized
- [ ] H2 token selectivity is complete
- [ ] cross-track convergence is computed
- [ ] worked examples are curated
- [ ] paper skeleton and first draft of Method / Setup / Results 5.1 / Results 5.2 / Discussion exist
- [ ] contributions list is updated to reflect actual finished evidence