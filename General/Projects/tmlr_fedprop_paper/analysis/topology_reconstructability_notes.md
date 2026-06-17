---
type: analysis-note
status: parked
project: tmlr_fedprop_paper
tags: [fedprop, analysis, topology, p3]
---

# Topology and Reconstructability Notes

## Purpose

Parking lot for the larger P3 question. Do not use this note to expand P1.

## Core Question

Under what graph, feature, and partition conditions can missing cross-client information be reconstructed effectively?

## Hypothesis

Feature propagation works best when:

- Features are smooth over the relevant graph edges.
- Missing nodes are well anchored to known local nodes.
- Partitioning removes useful cross-client signal that the local graph cannot otherwise replace.

## Candidate Variables

- Feature Dirichlet energy.
- Label and feature homophily.
- Cross-client edge ratio.
- Boundary-node fraction.
- Distance from missing nodes to known nodes.
- Partition-induced structural fragmentation.

## Stage

This belongs to P3 unless the P1-to-P2 gap assessment proves that a small version is required for the TMLR paper.
