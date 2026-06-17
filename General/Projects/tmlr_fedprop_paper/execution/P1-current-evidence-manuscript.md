---
type: execution-stage
stage: P1
status: active
project: tmlr_fedprop_paper
tags: [fedprop, execution, p1, manuscript]
---

# P1 - Current-Evidence Manuscript

## Purpose

Produce the strongest complete and internally consistent FedProp manuscript supported by the evidence already in hand. P1 is a rewrite, organization, and integrity pass. It is not a new experimental program.

## Boundary

P1 includes:

- Reorganizing the argument.
- Rewriting unclear sections.
- Redrawing Figure 2.
- Consolidating existing tables and figures.
- Removing unsupported or overly broad claims.
- Clearly distinguishing L1 and L2 assumptions.
- Reframing the contribution around local feature reconstruction and zero additional graph-data communication beyond FedAvg.
- Adding limitations based on the current results.
- Moving peripheral material to the appendix.

P1 excludes:

- New experiments.
- New datasets.
- New baselines.
- New reconstruction metrics.
- New topology analysis.
- New theoretical results.
- New recovery calculations unless the numbers already exist.
- Attempts to answer every open reviewer question.

## Four Claims

1. Partitioning harms GNN performance because clients lose cross-client neighbor features.
2. FedProp recovers a substantial portion of that lost performance.
3. This recovery requires no additional node-feature or embedding communication beyond FedAvg.
4. The method works with both GCN and GAT.

## Next P1 Task

The next P1 task is the revision of Section 6, Experiments and Results.

Start from [[../writing/Section 6]] and rewrite the results section around the recovery-first structure:

1. Experimental protocol and recovery metrics.
2. Main GCN recovery results on homophilic benchmarks.
3. Compact GAT backbone-generality results.
4. Communication-accuracy positioning against prior work.
5. Ablations for propagation operator, positional encoding, and convergence.
6. Scope diagnostics for Amazon and heterophilic graphs.

The first concrete output should be the core GCN recovery table and the accompanying narrative explaining Full-to-Zero-hop loss, FedProp-L1 recovery, and FedProp-L2 as an extended-structure variant.

## Required P1 Outputs

| Output | Destination | Status |
|---|---|---|
| Section 6 rewrite | [[../writing/Section 6]] | Active - next task |
| Section-level revision map | [[../writing/revision_map]] | Not started |
| Figure 2 redraw spec | [[../writing/figure_2_redraw_spec]] | Drafted |
| Claims and language pass | [[../writing/claims_and_language_pass]] | Drafted |
| Recovery-metric rewrite notes | [[../analysis/recovery_metrics]] | Drafted |
| L1/L2 assumptions note | [[../analysis/l1_l2_assumptions]] | Drafted |
| Communication accounting note | [[../analysis/communication_accounting]] | Drafted |
| Review packet | [[../writing/review_packet]] | Not started |
| Weak-claims inventory | [[P1-to-P2-gap-assessment]] | Not started |

## Manuscript Checks

- Fix the Figure XYX placeholder.
- Resolve unresolved cross-references.
- Reconcile notation and hyperparameter inconsistencies.
- Complete dataset statistics tables for datasets that remain in the paper.
- Reconcile main and appendix GAT tables.
- Separate same-protocol results from literature-positioning comparisons.
- Mark Amazon and heterophilic results as scope diagnostics where appropriate.

## Exit Criteria

P1 is complete when the manuscript can be sent to Carlee / Joao with:

- A coherent central claim.
- No known placeholders or unresolved references.
- A clear result spine.
- Honest limitations.
- A short list of remaining unsupported or weak claims.
