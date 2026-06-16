---
project: FedProp
type: research
status: under-review
year: 2025
tags: [federated-learning, GNN, graph-neural-networks, spectral-graph-theory, privacy, communication-efficiency]
---

# FedProp: Communication-Efficient Federated GNNs

## One-Line Summary
A model-agnostic federated GNN framework that achieves 99.6% of centralized performance with zero additional inter-client communication by solving the missing-neighbor problem through local feature propagation.

## Two-Line Summary (for CVs)
Designed and implemented FedProp, a novel algorithm for federated graph neural networks that reconstructs missing neighbor features locally via iterative propagation. Derived mathematical convergence guarantees and error bounds using spectral graph theory; achieved 99.6% of centralized accuracy on Cora without inter-client data exchange.

## Problem
In federated learning for GNNs, each client only has access to a local subgraph. When a node's neighbors reside on different clients, their features are inaccessible — the "missing neighbor problem." This causes degraded model performance without any principled solution that preserves privacy and communication efficiency.

## Brian's Role
- Formulated the missing-neighbor problem mathematically
- Designed the FedProp algorithm (local feature propagation via iterative message passing)
- Derived convergence guarantees and error bounds using spectral graph theory (Laplacian analysis)
- Built training and evaluation pipelines
- Benchmarked against centralized and other federated baselines on standard graph datasets

## Methods and Tools
- Spectral graph theory (Laplacian eigenmaps, propagation operator analysis)
- Graph neural networks (various architectures — model-agnostic)
- Federated learning framework
- PyTorch, graph benchmarks (Cora, etc.)

## Key Results
- 99.6% of centralized model accuracy on Cora with zero additional inter-client communication
- Mathematically proven convergence with derived error bounds
- Submitted to IEEE ICC (also noted as AAAI in some materials — verify actual submission)

## Why It Matters
Privacy-preserving ML over graph-structured data is critical for healthcare records, financial networks, and telecom data — all inherently graph-structured and privacy-sensitive. FedProp provides a principled, mathematically grounded solution that doesn't require trading privacy for performance.

## Variants for Different Applications

### Research framing (PhD apps, fellowships)
"FedProp demonstrates my ability to move from problem formulation to algorithm design to mathematical analysis — I did not just implement federated GNNs, I proved why the propagation operator converges and derived the error bounds. This experience in spectral graph theory directly informs my current interest in applying Laplacian eigenmodes to analyze transformer attention graphs in VLMs."

### Industry framing (ML engineer, research engineer)
"Built a federated learning framework for GNNs that achieves near-centralized performance without sharing raw data — solving a hard constraint problem in privacy-aware distributed ML. Implemented end-to-end training pipelines and benchmarked across datasets."

### Efficiency / low-resource framing
"Federated learning under strict communication limits: designed an algorithm that recovers full performance with zero extra communication rounds, critical for bandwidth-constrained or satellite-connected deployments."

## Links
- Paper: [under review — add link when available]
- Code: [GitHub link — confirm public]
- Preprint: [arXiv — if submitted, add link]

## Supervisor
Prof. João Barros, CMU-Africa
