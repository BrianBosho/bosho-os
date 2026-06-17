---
type: section-plan
status: active
project: tmlr_fedprop_paper
section: 6
tags: [fedprop, writing, results, p1]
---

# Section 6 - Experiments and Results P1 Rewrite Plan

## Purpose

Section 6 should prove one central claim:

> Graph partitioning creates a measurable Full-to-Zero-hop performance gap on the core homophilic benchmarks, and FedProp recovers a substantial portion of that gap without additional node-feature, embedding, or reconstruction-model communication beyond FedAvg.

The section should not present every variant as equally important. The main text should establish the recovery story, then use compact follow-up sections for backbone generality, communication positioning, ablations, and scope diagnostics.

## Recommended Section Order

### 6.1 Experimental Protocol and Evaluation Metrics

Purpose: define the setup and the recovery lens before showing results.

Must cover:

- Datasets used in main results: Cora, CiteSeer, PubMed, OGBN-Arxiv.
- Backbones: GCN as the main recovery benchmark; GAT as backbone-generality evidence.
- Partition settings: IID and non-IID, with beta values stated clearly.
- Baselines/reference points:
  - Full graph / centralized or full-neighborhood reference.
  - Zero-hop / local-only reference.
  - FedProp-L1.
  - FedProp-L2 as extended-structure or oracle-topology variant.
- Recovery metrics:

```text
loss = Full - Zero-hop
gain = FedProp - Zero-hop
Recovery% = 100 * gain / loss
```

Reporting rule:

- If Full and Zero-hop are too close, or Zero-hop is better than Full, report Recovery% as `N/A: no recoverable gap`.
- Do not let Recovery% hide raw accuracy; report both raw performance and recovery.

Main output:

- Short metric definition paragraph.
- One compact table or equation block defining loss, gain, and Recovery%.

### 6.2 Main Recovery Results on Homophilic Benchmarks

Purpose: this is the core P1 evidence.

Must cover:

- GCN results on Cora, CiteSeer, PubMed, and OGBN-Arxiv.
- Full vs Zero-hop degradation.
- FedProp-L1 recovery.
- FedProp-L2 recovery, clearly labeled as richer topology / extended structure.
- IID and non-IID settings, because partitioning is central to the paper.

Do not include here:

- Every Adj/Diff variant.
- Every PE/no-PE variant.
- Full GAT detail.
- Amazon or heterophilic diagnostics.

Main table:

| Dataset | Partition | Full | Zero-hop | FedProp-L1 | Rec% L1 | FedProp-L2 | Rec% L2 |
|---|---|---:|---:|---:|---:|---:|---:|

Main figure:

- Recovery plot showing `Zero-hop -> FedProp-L1 -> FedProp-L2 -> Full`.
- Use a bracket or shaded region to show the recoverable Full-to-Zero-hop gap.

Writing point:

- The paragraph should say what the gap is, how much FedProp recovers, and whether L2 adds meaningful benefit over L1.

### 6.3 Backbone Generality: GCN to GAT

Purpose: show that FedProp is not tied only to GCN.

Must cover:

- Compact GAT recovery table on citation datasets.
- Same recovery framing where possible.
- Avoid claiming universal model-agnosticity across all GNNs.

Main table:

| Dataset | Partition | Full GAT | Zero-hop GAT | FedProp-GAT | Recovery% |
|---|---|---:|---:|---:|---:|

Move to appendix:

- Detailed GAT variants.
- Full GAT IID/non-IID/hop/operator tables if too large.

Writing point:

- This subsection should read as "the same missing-neighbor recovery pattern also appears with GAT," not as a second full results section.

### 6.4 Communication-Accuracy Positioning Against Prior Work

Purpose: position FedProp after the reader understands the recovery result.

Move this after the main recovery section. The current order puts SOTA comparison too early.

Must cover:

- FedProp: no additional node-feature, embedding, or reconstruction-model communication beyond FedAvg, given the stated topology assumption.
- FedGCN / FedGAT: one-time setup or pretraining communication.
- FedSage+ / FedDEP / FedCog: different protocols and/or extra communication.
- Same-protocol vs literature-reported values must be separated.

Main table or figure:

| Method | Protocol family | Extra graph-data communication | Same protocol as FedProp? | Accuracy source |
|---|---|---|---|---|

Optional figure:

- Accuracy or recovery on one axis.
- Communication category on the other axis.
- Different markers for "ours / rerun" vs "reported by original paper".

Writing point:

- Do not claim a clean head-to-head win against methods with incompatible protocols.
- The claim is communication-positioning plus competitive performance, not universal SOTA dominance.

### 6.5 Ablations: Propagation Operator, Positional Encoding, and Convergence

Purpose: keep useful variants without letting them dominate the results story.

Must cover only if clean and concise:

- Adj vs Diff: present as propagation-operator ablation.
- PE/no-PE: present as an enhancement that can improve task performance and SOTA positioning.
- Propagation convergence / Dirichlet energy: include only as a short sanity check if it supports the method section.

Recommended main-text treatment:

- One compact ablation table.
- One small convergence figure only if it is already clean and interpretable.

Move to appendix:

- Full operator-by-dataset tables.
- Full PE/no-PE tables.
- Long convergence curves or many propagation-step plots.

Writing point:

- Do not make PE or Diff the central contribution. The central contribution is local feature propagation for missing-neighbor recovery.

### 6.6 Scope Diagnostics: Amazon and Heterophilic Graphs

Purpose: explain where the recovery framing is and is not meaningful.

Rename away from "Failure Mode: Heterophilic Graphs." A better title is:

- "Scope Diagnostics"
- "When Recovery Is Not the Right Metric"
- "Recoverable-Gap Diagnostics"

Must cover:

- Amazon datasets: large, non-citation homophilic graphs where FedProp can work, but the Full-to-Zero-hop gap may be small. This limits the recovery story.
- Heterophilic datasets: if Zero-hop matches or beats Full, there is no meaningful degradation to recover under the tested setup.

Main diagnostic table:

| Dataset | Graph type | Full - Zero-hop gap | FedProp behavior | Interpretation |
|---|---|---:|---|---|

Writing point:

- Do not say the missing-neighbor problem does not exist in heterophilic graphs.
- Safer claim: under the tested GCN/GAT setup, these datasets do not show the same recoverable Full-to-Zero-hop degradation as the homophilic core benchmarks.
- The broader topology/reconstructability question belongs in Discussion and P3.

Move to appendix:

- Full Amazon tables.
- Full heterophilic tables.
- Any detailed topology or reconstruction-error analysis.

## Variant Hierarchy for Main Text

| Variant axis | Main-text decision |
|---|---|
| GCN/GAT | GCN is the main recovery story; GAT is compact backbone-generality evidence. |
| IID/non-IID | Keep in main text because partitioning is central. |
| L1/L2 | Keep in main text because assumptions and communication cost are central. |
| Adj/Diff | Ablation, not the main result spine. Pick a default for main recovery tables. |
| PE/no-PE | Ablation or enhanced FedProp row; do not make it the base claim. |
| Amazon | Scope diagnostic, not core recovery evidence. |
| Heterophilic | Scope diagnostic and discussion bridge, not a failure dump. |
| Convergence | Short sanity check or appendix. |

## Required Main-Text Assets

| Asset | Purpose | Status |
|---|---|---|
| Table 6.1: Recovery metric definitions | Defines loss, gain, and Recovery%. | To write |
| Table 6.2: Core GCN recovery | Main evidence for the paper. | To build |
| Figure 6.1: Recovery visualization | Makes the recoverable gap visually clear. | To design |
| Table 6.3: Compact GAT recovery | Shows backbone generality. | To build |
| Table/Figure 6.4: Communication-accuracy positioning | Positions FedProp against SOTA without protocol confusion. | To build |
| Table 6.5: Compact ablation table | Keeps Adj/Diff and PE visible without bloating main results. | To decide |
| Table 6.6: Scope diagnostics | Explains Amazon and heterophilic results. | To build |

## Appendix Moves

Move these out of the main Section 6 unless they are essential to the P1 story:

- Full raw accuracy tables for every dataset, beta, hop, backbone, PE setting, and propagation operator.
- Detailed Adj vs Diff tables.
- Full PE/no-PE tables.
- Detailed GAT results.
- Full Amazon result tables.
- Full heterophilic result tables.
- Long convergence plots.
- Reconstruction-error analysis.
- Broad topology interpretation.
- Expanded SOTA protocol details.

## Immediate Writing Tasks

1. Pick the default FedProp variant for the main recovery tables.
2. Build the core GCN recovery table with IID/non-IID and L1/L2.
3. Draft the recovery-metric paragraph for 6.1.
4. Draft the 6.2 narrative around Full-to-Zero-hop loss and FedProp recovery.
5. Decide whether PE appears in the main ablation table or only in communication positioning.
6. Rename the heterophilic section to "Scope Diagnostics" and rewrite it around recoverable gap.
7. Move detailed variant tables to appendix.
