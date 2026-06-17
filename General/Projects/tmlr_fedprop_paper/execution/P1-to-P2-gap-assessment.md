---
type: gap-assessment
status: not-started
project: tmlr_fedprop_paper
tags: [fedprop, p1, p2, claims, evidence]
---

# P1 to P2 Gap Assessment

## Purpose

After P1 is complete, evaluate every major claim using a claim-evidence matrix. This decides what belongs in P2 and what should remain future work or P3.

## Classification

Each gap should be classified as:

- Required for the main claim.
- Helpful but not required.
- Belongs to future work.

## Claim-Evidence Matrix

| Claim | Existing evidence | Current weakness | Required addition | Classification |
|---|---|---|---|---|
| FedProp improves local federated GNN training | Existing GCN/GAT results | Improvement may not be consistently contextualized | Performance-recovery analysis | TBD |
| FedProp adds no graph-data communication | Algorithm and protocol description | L1/L2 assumptions may be unclear | Precise communication accounting | TBD |
| FedProp is competitive with SOTA | Existing comparison tables and literature positioning | Protocols differ across methods | Controlled baseline or explicit positioning | TBD |
| FedProp is model-agnostic | GCN and GAT results | Possibly sufficient already | Better presentation, likely no new experiment | TBD |
| FedProp is robust to heterogeneity | Existing partition/client-count results | Partition effects may be under-explained | Realized graph statistics | TBD |
| FedProp reconstructs useful features | Downstream accuracy | No direct reconstruction evidence | Focused reconstruction diagnostic | TBD |
| Topology determines when FedProp works | Amazon/heterophilic observations | Not systematic | Separate topology-focused study | Likely P3 |

## Output

The filled matrix should produce a short P2 scope decision:

- P2 must include:
- P2 may include:
- P2 should exclude:
- P3 candidates:
