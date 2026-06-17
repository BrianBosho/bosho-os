---
title: "Propagator Eval — Anchor-Dataset-First Experiment Reorganization"
type: experiment-strategy
source: google-drive
drive-id: 1HZk8F88SFGrxVsSftUAhTNPGFd7F9zGUNhKcsobdrTM
created: 2026-05-01
tags: [fedprop, propagator, experiments, strategy, phases, cora-anchor]
project: tmlr_fedprop_paper
---

# Propagator Eval — Anchor-Dataset-First Experiment Reorganization

**Date:** 2026-05-01

**Purpose:** Reorganize the propagator evaluation experiments so that we first produce a detailed, paper-quality analysis on one anchor dataset, then scale the same locked protocol across additional datasets.

---

## 0. Core Decision

We will **not** begin by running the full six-dataset matrix.

Instead, we will use a staged strategy:

1. **Cora as the anchor dataset** for detailed analysis, debugging, visualization, and narrative development.
2. **Citeseer and PubMed** as homophilic reproduction datasets.
3. **OGBN-Arxiv** as the scalability dataset.
4. **Texas and Wisconsin** as heterophilic stress-test datasets.

This preserves the full experimental ambition while preventing the project from getting stuck in a large undifferentiated run matrix.

---

## 1. Why Anchor on One Dataset First?

The full reconciled plan is large:

- Layer 1–3 intrinsic core: 317 runs
- Intrinsic ablations: 42 runs
- Layer 4 downstream homophilic block: 540 runs
- Layer 4 heterophilic extension: 40 runs
- Full reconciled total with ablations: 939 runs

Running everything immediately risks: discovering config bugs too late, producing many incomplete result folders, confusing exploratory analysis with final analysis, overfitting the paper narrative to noisy multi-dataset tables, and delaying the first interpretable plots.

Therefore, we should first build the complete analysis loop on a single dataset.

The goal of the first phase is not merely to "get results." The goal is to establish the full empirical language of the paper.

---

## 2. Anchor Dataset Choice

### Use Cora first.

Cora is the best anchor because it is: small enough for fast iteration, standard in GNN and feature propagation literature, homophilic enough for propagation to have a meaningful expected signal, easy to debug, suitable for detailed visualizations and ablations, and likely to expose operator differences clearly without large-scale engineering overhead.

### Do not start with OGBN-Arxiv.

OGBN-Arxiv should be reserved for scalability once the protocol is stable.

### Do not start with Texas/Wisconsin.

Texas and Wisconsin are valuable, but they answer a different question: how propagation behaves when homophily assumptions weaken.

---

## 3. New Experimental Philosophy

The old structure is:

```text
Run all operators × all datasets × all settings.
Then analyze.
```

The new structure is:

```text
Understand deeply on Cora.
Freeze the protocol.
Reproduce on similar datasets.
Stress-test on hard datasets.
Scale to larger graphs.
```

This gives the work a cleaner scientific arc:

```text
Phenomenon → Mechanism → Reproducibility → Scalability → Failure modes
```

---

## 4. Paper-Level Narrative Produced by This Strategy

The experiments should support the following storyline:

> We first conduct a detailed anchor-dataset analysis on Cora to characterize how different propagation operators recover missing features under controlled missingness, propagation depth, and partition conditions. After fixing the metric suite and analysis template, we reproduce the same protocol on additional homophilic datasets, evaluate scalability on OGBN-Arxiv, and finally test heterophilic robustness on Texas and Wisconsin.

This narrative is stronger than immediately showing six datasets because it allows the paper to explain *why* the operators behave differently before showing that the pattern generalizes.

---

## 5. Experimental Phases

## Phase 0 — Protocol Freeze and Repo Cleanup

### Goal

Make the repo execution-ready for the staged plan.

### Tasks

- Confirm the local execution stack is authoritative: `RUNBOOK.md`, `configs/`, intrinsic runner, downstream runner, post-processing scripts.
- Mark the Google Doc as the conceptual/high-level protocol.
- Add a short note in the docs explaining the staged execution plan.
- Confirm the first-pass intrinsic metrics: `mse`, `cosine_sim`, `recovery_ratio`, `boundary_coverage`, `iteration_count`, `residuals`, `convergence_flag`, `wall_clock_time`.
- Defer `spectral_fidelity` unless a later analysis explicitly needs it.
- Confirm the heterophilic downstream extension remains in scope, but not in Phase 1.

### Output

A committed repo state with:

```text
docs/
  EXPERIMENT_STRATEGY_ANCHOR_FIRST.md
  RUNBOOK.md
  EXPERIMENT_OBJECTIVES.md

configs/
  phase_1_cora_intrinsic.yaml
  phase_2_cora_ablation.yaml
  phase_3_cora_downstream.yaml
  phase_4_homophilic_reproduction.yaml
  phase_5_scalability_ogbn_arxiv.yaml
  phase_6_heterophily_stress.yaml
```

---

# 6. Phase 1 — Cora Intrinsic Core

## Goal

Run the complete intrinsic comparison on Cora only.

This phase answers:

> Which propagation operator best reconstructs missing features on a standard homophilic graph, and under what settings?

## Dataset

```yaml
datasets:
  - Cora
```

## Operators

```yaml
operators:
  - Adj
  - Diffusion
  - Chebyshev
  - APPNP
  - RandomWalk
  - HeatKernelReference
```

## Metrics

```yaml
metrics:
  - mse
  - cosine_sim
  - recovery_ratio
  - boundary_coverage
  - iteration_count
  - residuals
  - convergence_flag
  - wall_clock_time
```

## Settings to Include

```yaml
missing_rates:
  - low
  - medium
  - high

partition_settings:
  - iid_or_balanced
  - non_iid_or_boundary_heavy

propagation_depths:
  - shallow
  - medium
  - deep
```

## Required Outputs

```text
results/
  phase_1_cora_intrinsic/
    raw/
      <run_id>.json
    processed/
      metrics_table.csv
      operator_summary.csv
      depth_sensitivity.csv
      missing_rate_sensitivity.csv
      boundary_coverage_summary.csv
    plots/
      operator_comparison_mse.png
      operator_comparison_cosine.png
      operator_comparison_recovery_ratio.png
      operator_comparison_boundary_coverage.png
      depth_sensitivity.png
      missing_rate_sensitivity.png
      runtime_vs_quality.png
    notes/
      phase_1_findings.md
```

## Acceptance Criteria

Phase 1 is complete only when: all Cora intrinsic runs finish successfully, all output JSON files validate against the schema, post-processing completes without manual patching, every operator has at least one complete result row, the main comparison table can be generated, and the first draft of `phase_1_findings.md` exists.

## Phase 1 Findings Template

Create `results/phase_1_cora_intrinsic/notes/phase_1_findings.md` with this structure:

```markdown
# Phase 1 Findings — Cora Intrinsic Core

## 1. Summary

## 2. Best Overall Operator

## 3. Operator-by-Operator Behavior

### Adj

### Diffusion

### Chebyshev

### APPNP

### Random Walk

### Heat Kernel Reference

## 4. Effect of Missing Rate

## 5. Effect of Propagation Depth

## 6. Boundary Coverage Behavior

## 7. Runtime and Convergence

## 8. Surprising Results

## 9. Bugs or Config Issues Found

## 10. Decision: Ready for Ablations?
```

---

# 7. Phase 2 — Cora Ablations

## Goal

Use Cora to understand which design choices matter.

This phase answers:

> Are the observed operator differences robust, or are they artifacts of particular propagation depths, missingness patterns, or partition choices?

## Dataset

```yaml
datasets:
  - Cora
```

## Ablation Families

```yaml
ablation_families:
  - propagation_depth
  - missing_rate
  - client_partition
  - boundary_density
  - normalization
  - operator_specific_hyperparameters
```

## Required Outputs

```text
results/
  phase_2_cora_ablation/
    raw/
    processed/
      ablation_summary.csv
      ablation_effect_sizes.csv
      robustness_summary.csv
    plots/
      ablation_effects.png
      robustness_by_operator.png
      sensitivity_heatmap.png
    notes/
      phase_2_findings.md
```

## Key Decision After Phase 2

At the end of Phase 2, freeze:

```yaml
frozen_protocol:
  default_depths: ...
  default_missing_rates: ...
  default_partition_settings: ...
  default_operator_hyperparameters: ...
  required_metrics:
    - mse
    - cosine_sim
    - recovery_ratio
    - boundary_coverage
    - iteration_count
    - residuals
    - convergence_flag
    - wall_clock_time
```

This frozen protocol becomes the template for all later datasets.

---

# 8. Phase 3 — Cora Downstream Evaluation

## Goal

Connect intrinsic propagation quality to downstream GNN performance on the same anchor dataset.

This phase answers:

> Do better intrinsic feature recovery metrics correspond to better downstream model performance?

## Dataset

```yaml
datasets:
  - Cora
```

## Models

```yaml
models:
  - GCN
  - GAT
```

## Conditions

```yaml
conditions:
  - zero_hop
  - operator_propagation
  - oracle_or_full_feature_reference
```

## Operators

```yaml
operators:
  - Adj
  - Diffusion
  - Chebyshev
  - APPNP
  - RandomWalk
```

## Required Outputs

```text
results/
  phase_3_cora_downstream/
    raw/
    processed/
      downstream_accuracy.csv
      downstream_operator_summary.csv
      intrinsic_downstream_joined.csv
      gap_closed_summary.csv
    plots/
      downstream_accuracy_by_operator.png
      gap_closed_by_operator.png
      intrinsic_vs_downstream_scatter.png
      runtime_accuracy_tradeoff.png
    notes/
      phase_3_findings.md
```

## Key Analysis

The important object is the joined table `intrinsic_downstream_joined.csv` joining: intrinsic MSE, cosine similarity, recovery ratio, boundary coverage, runtime, downstream accuracy, and gap closed relative to zero-hop and oracle/full-feature reference.

## Acceptance Criteria

Phase 3 is complete only when: downstream Cora runs complete, gap-closed metric is computed, intrinsic and downstream results can be joined, there is at least one plot showing intrinsic score vs downstream performance, and we can decide whether intrinsic metrics are predictive of downstream gains.

---

# 9. Phase 4 — Homophilic Reproduction

## Goal

Test whether the Cora patterns reproduce on other common homophilic citation datasets.

## Datasets

```yaml
datasets:
  - Citeseer
  - PubMed
```

## Protocol

Use the frozen protocol from Phase 2. Do not add new exploratory ablations here unless Cora revealed a necessary fix.

## Required Outputs

```text
results/
  phase_4_homophilic_reproduction/
    Citeseer/
    PubMed/
    processed/
      reproduction_summary.csv
      cross_dataset_operator_summary.csv
      rank_stability.csv
    plots/
      cross_dataset_operator_comparison.png
      operator_rank_stability.png
      dataset_metric_heatmap.png
    notes/
      phase_4_findings.md
```

## Key Questions

- Does the best Cora operator remain strong on Citeseer and PubMed?
- Are operator rankings stable?
- Are failures dataset-specific?
- Does propagation depth sensitivity change with graph size or feature structure?

---

# 10. Phase 5 — Scalability on OGBN-Arxiv

## Goal

Evaluate whether the method scales to a larger graph.

## Dataset

```yaml
datasets:
  - OGBN-Arxiv
```

## Main Question

> Which operators remain computationally practical at larger scale?

## Required Metrics

```yaml
scalability_metrics:
  - wall_clock_time
  - memory_usage_if_available
  - convergence_flag
  - iteration_count
  - residuals
  - quality_per_second
```

## Required Outputs

```text
results/
  phase_5_scalability_ogbn_arxiv/
    raw/
    processed/
      ogbn_arxiv_summary.csv
      scalability_summary.csv
      quality_runtime_tradeoff.csv
    plots/
      ogbn_operator_comparison.png
      runtime_by_operator.png
      quality_per_second.png
      convergence_behavior.png
    notes/
      phase_5_findings.md
```

## Failure Handling

If an operator fails on OGBN-Arxiv due to memory or runtime: keep the failed run record, record the failure mode, do not delete the run, mark the result as `failed_resource_limit` or equivalent, and include the failure in the scalability discussion.

---

# 11. Phase 6 — Heterophily Stress Test

## Goal

Test whether propagation behavior changes when homophily assumptions weaken.

## Datasets

```yaml
datasets:
  - Texas
  - Wisconsin
```

## Operators

```yaml
operators:
  - Adj
  - Diffusion
  - APPNP
  - ZeroHop
```

## Main Question

> Does feature propagation help, hurt, or become unstable on heterophilic graphs?

## Required Outputs

```text
results/
  phase_6_heterophily_stress/
    Texas/
    Wisconsin/
    processed/
      heterophily_summary.csv
      heterophily_downstream_summary.csv
      homophily_vs_heterophily_comparison.csv
    plots/
      heterophily_operator_comparison.png
      propagation_help_vs_hurt.png
      homophilic_vs_heterophilic_rank_shift.png
    notes/
      phase_6_findings.md
```

---

# 12. Suggested Config Reorganization

```text
configs/
  README.md

  phase_1_cora_intrinsic.yaml
  phase_2_cora_ablation.yaml
  phase_3_cora_downstream.yaml
  phase_4_homophilic_reproduction.yaml
  phase_5_scalability_ogbn_arxiv.yaml
  phase_6_heterophily_stress.yaml

  shared/
    operators.yaml
    metrics.yaml
    datasets.yaml
    seeds.yaml
    output_schema.yaml

  archived/
    old_full_matrix_configs/
```

---

# 13. Suggested Results Directory

```text
results/
  phase_0_protocol_freeze/

  phase_1_cora_intrinsic/
    raw/
    processed/
    plots/
    logs/
    notes/

  phase_2_cora_ablation/
    raw/
    processed/
    plots/
    logs/
    notes/

  phase_3_cora_downstream/
    raw/
    processed/
    plots/
    logs/
    notes/

  phase_4_homophilic_reproduction/
    Citeseer/
    PubMed/
    processed/
    plots/
    logs/
    notes/

  phase_5_scalability_ogbn_arxiv/
    raw/
    processed/
    plots/
    logs/
    notes/

  phase_6_heterophily_stress/
    Texas/
    Wisconsin/
    processed/
    plots/
    logs/
    notes/

  final_tables/
  final_figures/
  paper_exports/
```

---

# 14. Run ID Convention

Recommended format:

```text
<phase>__<dataset>__<operator>__<setting>__seed<seed>
```

Example:

```text
phase1__cora__appnp__missing030_depth10_partition_boundary__seed0
phase2__cora__chebyshev__depth20_ablation__seed1
phase5__ogbn_arxiv__diffusion__missing030_depth10__seed0
```

Every raw JSON output should include the run ID.

---

# 15. Required JSON Schema Fields

Each intrinsic run should emit at least:

```json
{
  "run_id": "...",
  "phase": "...",
  "dataset": "...",
  "operator": "...",
  "seed": 0,
  "missing_rate": 0.3,
  "partition_setting": "...",
  "propagation_depth": 10,
  "operator_hyperparameters": {},
  "metrics": {
    "mse": null,
    "cosine_sim": null,
    "recovery_ratio": null,
    "boundary_coverage": null,
    "iteration_count": null,
    "residuals": null,
    "convergence_flag": null,
    "wall_clock_time": null
  },
  "status": "success",
  "failure_reason": null,
  "timestamp": "..."
}
```

Each downstream run should emit at least:

```json
{
  "run_id": "...",
  "phase": "...",
  "dataset": "...",
  "model": "GCN",
  "operator": "...",
  "condition": "...",
  "seed": 0,
  "metrics": {
    "accuracy": null,
    "macro_f1": null,
    "gap_closed": null,
    "train_time": null,
    "wall_clock_time": null
  },
  "status": "success",
  "failure_reason": null,
  "timestamp": "..."
}
```

---

# 16. Post-Processing Workflow

Every phase should use the same post-processing pattern:

```text
raw JSON files
    ↓
schema validation
    ↓
phase-level CSV
    ↓
operator summary
    ↓
plots
    ↓
phase findings note
```

---

# 17. Stop/Go Gates

## Gate 1 — After Phase 1

Proceed to Cora ablations only if: Cora intrinsic results are complete, all operators run successfully or failures are understood, the post-processing works, and the plots are interpretable.

## Gate 2 — After Phase 2

Proceed to downstream only if: default settings are frozen, ablations identify stable hyperparameter choices, and no unresolved schema or metric bugs remain.

## Gate 3 — After Phase 3

Proceed to other datasets only if: intrinsic and downstream results can be joined, gap-closed metric works, and there is a clear Cora narrative.

## Gate 4 — After Phase 4

Proceed to OGBN-Arxiv only if: the protocol reproduces on Citeseer/PubMed, cross-dataset tables are generated, and operator ranking is reasonably interpretable.

## Gate 5 — After Phase 5

Proceed to final paper integration only if: OGBN-Arxiv scalability is summarized, failures are documented, and practical runtime tradeoffs are clear.

---

# 18. Minimal Viable Paper Results

If time becomes tight, the minimum publishable package is:

1. Cora detailed intrinsic analysis
2. Cora downstream connection
3. Citeseer/PubMed reproduction summary
4. OGBN-Arxiv scalability table
5. Texas/Wisconsin heterophily stress summary

If time becomes very tight, the absolute minimum is:

1. Cora detailed intrinsic analysis
2. Cora downstream connection
3. One reproduction dataset
4. One scalability or heterophily stress test

---

# 19. Recommended Paper Figure Plan

**Figure 1 — Experimental Design:** Schematic showing `Missing features → Propagation operator → Recovered features → Intrinsic metrics → Downstream evaluation`.

**Figure 2 — Cora Operator Comparison:** Main bar plot/table with MSE, cosine similarity, recovery ratio, boundary coverage.

**Figure 3 — Cora Sensitivity Analysis:** How performance changes with propagation depth, missing rate, and boundary-heavy partitions.

**Figure 4 — Intrinsic vs Downstream Link:** Scatter plot with x-axis = intrinsic recovery quality, y-axis = downstream gap closed or accuracy.

**Figure 5 — Cross-Dataset Reproduction:** Operator ranking or metric heatmap across Cora, Citeseer, PubMed.

**Figure 6 — Scalability:** Runtime-quality tradeoff on OGBN-Arxiv.

**Figure 7 — Heterophily Stress Test:** Homophilic vs heterophilic behavior comparison.

---

# 20. Recommended Tables

**Table 1 — Operator Definitions:** Columns: Operator, Mechanism, Hyperparameters, Expected Strength, Expected Weakness.

**Table 2 — Cora Intrinsic Results:** Columns: Operator, MSE ↓, Cosine ↑, Recovery Ratio ↑, Boundary Coverage ↑, Runtime ↓.

**Table 3 — Cora Downstream Results:** Columns: Model, Operator, Accuracy ↑, Gap Closed ↑, Runtime ↓.

**Table 4 — Cross-Dataset Summary:** Columns: Dataset, Best Operator, MSE Rank, Recovery Rank, Boundary Coverage Rank, Runtime Rank.

**Table 5 — Scalability Results:** Columns: Dataset, Operator, Runtime, Converged?, Quality Score, Quality per Second.

**Table 6 — Heterophily Results:** Columns: Dataset, Operator, Helps/Hurts, Accuracy Change, Intrinsic Recovery, Interpretation.

---

# 21. Recommended Immediate Next Steps

**Today:**

1. Add this strategy document to the repo.
2. Create `phase_1_cora_intrinsic.yaml`.
3. Run a tiny dry run on Cora with one or two operators.
4. Validate output schema.
5. Confirm post-processing works.

**Next Work Session:**

1. Run full Phase 1 Cora intrinsic core.
2. Generate the first operator comparison table.
3. Write `phase_1_findings.md`.
4. Decide whether to proceed to Cora ablations.

**After Phase 1:**

Do not jump to all datasets. Proceed in this order:

```text
Cora ablations → Cora downstream → Citeseer/PubMed → OGBN-Arxiv → Texas/Wisconsin
```

---

# 22. Final Recommendation

Yes, reorganize the experiments around a single detailed anchor dataset.

The best structure is:

```text
Cora = deep understanding
Citeseer/PubMed = reproduction
OGBN-Arxiv = scalability
Texas/Wisconsin = heterophily stress test
```

This makes the work easier to execute, easier to debug, and easier to write as a coherent paper.

The project should avoid a premature full-matrix run. The full matrix should be the final confirmation step, not the first step.
