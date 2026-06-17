---
type: execution-stage
stage: P3
status: parked
project: tmlr_fedprop_paper
tags: [fedprop, execution, p3, topology, reconstructability]
---

# P3 - Topology and Reconstructability Paper

## Purpose

Park the larger scientific question exposed by FedProp:

> Under what graph, feature, and partition conditions can missing cross-client information be reconstructed effectively?

This is a separate paper, not a P1 or P2 obligation.

## Core Themes

- Graph homophily and heterophily.
- Feature homophily and smoothness.
- Dirichlet energy and graph signal frequency.
- Boundary-node density and cross-client edge structure.
- Distance from observed to missing nodes.
- Partition-induced missingness.
- Reconstruction error bounds.
- Synthetic graphs and controlled topology sweeps.

## Possible Measurements

- Cross-client edge ratio.
- Boundary-node fraction.
- Remote-neighbor ratio per local node.
- Label and feature homophily.
- Feature Dirichlet energy.
- Distance to nearest known node.
- Scalable proxies for boundary anchoring.

## Possible Empirical Scope

- Amazon Computers and Photo.
- Heterophilic datasets.
- OGBN-Products.
- Controlled synthetic graphs.
- Partition sweeps that separate label skew from structural fragmentation.
- Alternative propagation algorithms.

## Guardrail

P3 explains when and why graph-based reconstruction works. P1 and P2 explain whether FedProp works for the TMLR paper's communication-efficient missing-neighbor claim.
