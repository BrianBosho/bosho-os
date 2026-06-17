---
project: tmlr_fedprop
title: "TMLR FedProp Paper"
type: project
status: active
domain: General
priority: P1
deadline: null
tags: [project, research, paper, fedprop, tmlr]
---

# TMLR FedProp Paper

> Stable project brief and context. Active execution lives in [[execution]]; weekly tickable actions live in [[To-Do]]. History: [[archive]].

## Objective

Produce a focused, internally consistent TMLR paper built on current evidence first. The contribution is: **FedProp recovers performance lost through graph partitioning using local feature propagation, with zero additional node-feature, embedding, or reconstruction-model communication beyond standard FedAvg, given the stated neighborhood-structure assumption.**

The paper does not need to solve every open question about federated graph learning. It needs to establish its core claims clearly, with consistent evidence and honest scope limits.

## Scope Framework

| Level | Definition | Status |
|---|---|---|
| P1 | Complete manuscript using current evidence. Reorganize, rewrite, fix, and cut. No new experiments. | Active |
| P2 | Improved TMLR paper with bounded additions: realized graph stats, reconstruction diagnostic, controlled FedGCN rerun, and focused robustness if needed. | Parked |
| P3 | Separate follow-up paper on topology, feature smoothness, partitioning, and reconstructability. | Parked |

## Current Target

| Target | Definition |
|---|---|
| P1 minimum | Complete, internally consistent manuscript with all known manuscript issues fixed. |
| P1 strong win | P1 manuscript sent to Carlee / Joao with specific review questions. |
| Not P1 | New experiments, datasets, baselines, reconstruction metrics, or topology theory. |

## Four Core Claims

1. Partitioning harms GNN performance because clients lose cross-client neighbor features.
2. FedProp recovers a substantial portion of that lost performance.
3. This recovery requires no additional node-feature or embedding communication beyond FedAvg.
4. The method works with both GCN and GAT.

If a section, experiment, or analysis does not directly support one of these claims, it should move to the appendix, P2, or P3.

## Execution

Active execution lives in [[execution]]. This project brief should hold context, strategy, milestones, people, and links; live task state belongs in the execution page.

Stage plans:

- [[execution/P1-current-evidence-manuscript]]
- [[execution/P2-tmlr-improvement-plan]]
- [[execution/P3-topology-reconstructability-paper]]
- [[execution/P1-to-P2-gap-assessment]]

## Key Paper Issues to Resolve in P1

- Reframe primary results around full-to-zero-hop degradation and gap recovery, not raw accuracy alone.
- Qualify communication claims and remove broad "communication-free" or privacy-preserving language unless formally supported.
- Clearly distinguish L1 from L2 assumptions; L2 should be treated as extended-structure or oracle-topology unless setup communication is accounted for.
- Redraw Figure 2 as an information-flow diagram: partitioned graph, client-local structural context, constrained propagation, local GNN plus FedAvg.
- Reframe Amazon and heterophilic results as scope diagnostics rather than positive-result failures.
- Separate controlled comparisons from literature positioning.
- Create a weak-claims inventory after P1 edits.

## This-Week Sequence

| Day | Focus | Concrete output |
|---|---|---|
| Tue Jun 16 | Scope lock + revision map | Ordered manuscript fix list; confirm P1 boundary. |
| Wed Jun 17 | Recovery metrics + results rewrite | Add loss/gain/recovery framing to one main results unit. |
| Thu Jun 18 | Manuscript fixes | Resolve placeholders, cross-references, table inconsistencies, and assumption language. |
| Fri Jun 19 | Figure 2 + claims reframe | New Figure 2 spec/draft and qualified communication claim throughout. |
| Sat Jun 20 | Catch-up + packaging | Finish highest-priority missing P1 item; draft review packet if ready. |

## 90-Minute Task Menu

| Task | Output |
|---|---|
| Manuscript audit | Section-level list of weak, missing, or stale material. |
| Recovery metrics pass | Add loss, gain, and Recovery% framing to main results tables. |
| Placeholder sweep | Fix Figure XYX, unresolved references, and inconsistent notation. |
| Figure 2 sketch | Annotated draft of four-stage information-flow diagram. |
| Communication claim edit | Replace broad communication-free language with the qualified claim. |
| Amazon / heterophilic reframe | Move to scope diagnostics or appendix and rewrite framing. |
| Weak-claims inventory | Unsupported claims after P1 edits; input to P1-to-P2 gap assessment. |
| Sendable package | Manuscript, open questions, result status, and requested feedback for Carlee/Joao. |

## Working Notes

| Item | Notes |
|---|---|
| Support | M can help; Carlee can double-check. |
| Venue | TMLR; no page restriction. |
| Standard | Good enough to send for feedback, not perfect. |
| FedGCN rerun | Defer to P2 unless the P1 gap assessment makes it essential. |
| FedGAT rerun | Not a P1 priority; GAT backbone results already support model-agnosticity. |
| FedSage+ | Protocol differs; use literature positioning unless a later controlled comparison is justified. |

## Current Next Action

Create [[writing/revision_map]] from the latest manuscript.

## Background & Research Notes

- [[FedProp Publication Push]] - earlier publication-strategy brain-dump.
- [[Unprocessed/3 Step Approach]] - P1/P2/P3 scope framework.
- [[Unprocessed/Minimal scope]] - four-claim scope boundary.
- [[Unprocessed/Result section Notes]] - results, figure, topology, and baseline notes.
- [[Unprocessed/Review 1]] - reviewer feedback and specific asks.

## Links

- History: [[archive]]
- Planning: [[To-Do]] - [[This Week]]
