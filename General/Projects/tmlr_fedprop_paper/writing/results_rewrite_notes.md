---
type: writing-notes
status: draft
project: tmlr_fedprop_paper
tags: [fedprop, writing, results]
---

# Results Rewrite Notes

## Results Spine

The results section should answer:

1. Does partitioning create a recoverable loss?
2. How much does FedProp recover?
3. What does that recovery cost in communication?
4. Where does the scope of the method appear to end?

## Main Result Framing

Use Full, Zero-hop, FedProp-L1, FedProp-L2, and RPE variants to show degradation and recovery. Raw accuracy remains useful, but the narrative should foreground the gap from Full to Zero-hop and the fraction of that gap recovered by FedProp.

## Scope Diagnostics

Amazon:

- If the Full-to-Zero-hop gap is small, FedProp has little recoverable loss to repair.
- This is not the same as algorithmic failure.

Heterophilic datasets:

- If Zero-hop is competitive with or better than Full, recovery is not the right metric.
- Frame this as a limitation of smoothness-based propagation under the tested setup.

## Baseline Positioning

- Same-protocol reruns belong in controlled result tables.
- Literature values with different protocols belong in a separate communication-accuracy positioning figure or table with explicit disclaimers.
