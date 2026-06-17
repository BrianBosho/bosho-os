---
type: analysis-note
status: draft
project: tmlr_fedprop_paper
tags: [fedprop, analysis, communication]
---

# Communication Accounting

## Purpose

The paper's main contribution is communication-related, so the communication model must be precise.

## Distinctions to Keep Clear

- Standard FedAvg model-parameter communication.
- Additional node-feature communication.
- Additional node-embedding communication.
- Additional generated-feature or reconstruction-model communication.
- One-time topology setup communication.
- Repeated per-round graph-data communication.

## Preferred Claim

FedProp requires zero additional node-feature, embedding, or reconstruction-model communication beyond standard FedAvg, given the stated neighborhood-structure assumption.

## L1

L1 can carry the primary claim if the paper clearly states that the client already knows:

- Its own nodes and features.
- Its local edges.
- The existence or identity of incident cross-client edges.
- No remote features.
- No remote labels.

## L2

L2 should not be presented as free unless the topology is genuinely available before training. Safer labels:

- Extended-structure variant.
- Oracle-topology variant.
- One-time topology-setup variant.
