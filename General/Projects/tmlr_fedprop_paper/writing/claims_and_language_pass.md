---
type: writing-pass
status: draft
project: tmlr_fedprop_paper
tags: [fedprop, writing, claims]
---

# Claims and Language Pass

## Preferred Core Claim

FedProp recovers performance lost through graph partitioning using local feature propagation, with zero additional node-feature, embedding, or reconstruction-model communication beyond standard FedAvg, given the stated neighborhood-structure assumption.

## Replace or Qualify

| Avoid | Use instead |
|---|---|
| communication-free | zero additional node-feature, embedding, or reconstruction-model communication beyond FedAvg |
| privacy-preserving | compatible with privacy mechanisms, unless a formal privacy guarantee is provided |
| no communication | no additional graph-data communication beyond standard model aggregation |
| FedProp solves missing-neighbor information generally | FedProp targets settings where partitioning removes useful smooth cross-client feature signal |
| robust to partitioning | robust across the evaluated partition regimes |
| topology explains all failures | topology and feature smoothness likely influence reconstruction difficulty; P3 studies this directly |

## P1 Framing

- L1 is the primary contribution.
- L2 is an extended-structure or oracle-topology variant unless setup communication is explicitly counted.
- Amazon and heterophilic results are scope diagnostics.
- Recovery is meaningful only when Full outperforms Zero-hop by a real margin.
