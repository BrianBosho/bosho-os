---
type: execution-stage
stage: P2
status: parked
project: tmlr_fedprop_paper
tags: [fedprop, execution, p2, tmlr]
---

# P2 - Improved TMLR Paper

## Purpose

Build the strongest version of the same FedProp paper after P1 is complete. P2 should strengthen the central question:

> Can local feature propagation recover performance lost through graph partitioning without adding graph-data communication?

P2 should not become a topology paper or a broad federated graph learning survey.

## Entry Condition

Do not start P2 until:

- P1 manuscript is internally consistent.
- The P1 weak-claims inventory is complete.
- [[P1-to-P2-gap-assessment]] identifies which additions are required, helpful, or future work.

## Likely Additions

| Addition                                       | Priority | Rationale                                                                               |
| ---------------------------------------------- | -------- | --------------------------------------------------------------------------------------- |
| Performance recovery analysis                  | High     | Converts accuracy tables into a direct answer to the paper's main question.             |
| Precise communication accounting               | High     | Required because the contribution is communication-related.                             |
| Communication-accuracy positioning figure      | High     | Separates FedProp from FedGCN, FedGAT, FedSage+, FedDEP, and repeated-exchange methods. |
| Realized graph statistics per partition        | High     | Explains partition effects through structural metrics, not only beta.                   |
| Small reconstruction diagnostic                | Medium   | Addresses reviewer concern without turning reconstruction into the main contribution.   |
| Controlled FedGCN rerun                        | Medium   | Most relevant same-family baseline if technically feasible.                             |
| Client-count robustness on Cora and OGBN-Arxiv | Medium   | Useful if scalability remains a claim.                                                  |

## Non-Goals

- Full topology-dependent reconstruction theory.
- Broad heterophily paper.
- OGBN-Products unless scalability is central.
- Full FedGAT reimplementation unless GAT comparison becomes a central claim.
- FedSage+ head-to-head rerun under incompatible protocols.

## Target P2 Structure

1. Introduction and motivation.
2. Federated missing-neighbor problem.
3. FedProp.
4. Communication model and assumptions.
5. Experimental setup.
6. Performance degradation and recovery.
7. Communication-accuracy tradeoff.
8. Model and partition robustness.
9. Reconstruction diagnostic.
10. Limitations.
11. Conclusion.
