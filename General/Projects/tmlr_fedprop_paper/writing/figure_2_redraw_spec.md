---
type: figure-spec
status: draft
project: tmlr_fedprop_paper
tags: [fedprop, writing, figure]
---

# Figure 2 Redraw Spec

## Purpose

Make one fact visually unmistakable: FedProp reconstructs missing remote features locally and does not transmit node features or intermediate node embeddings between clients.

## Four-Stage Layout

1. Partitioned global graph.
   - Clients are colored regions.
   - Cross-client edges are dashed.

2. Client-local structural context.
   - Zoom into one client.
   - Local nodes have known feature icons.
   - Remote boundary nodes are ghosted and marked "feature unavailable".
   - Show L1 normally; show L2 only as optional extended-structure inset.

3. Constrained feature propagation.
   - Diffusion arrows appear over the expanded local graph.
   - Known local features are locked or clamped.
   - Unknown remote features change from "?" to reconstructed feature vectors.

4. Local GNN and FedAvg.
   - Completed local graph enters GCN or GAT.
   - Only model parameters travel between client and server.
   - A crossed-out client-to-client arrow states "no node-feature or embedding exchange".

## Caption Draft

Figure 2: Overview of FedProp. A global graph is partitioned across clients, creating cross-client neighbors whose features are unavailable locally. For each client, FedProp constructs the available neighborhood-structure context, initializes remote-node features as missing, and applies constrained feature propagation while clamping observed local features. The reconstructed feature matrix is then used by a standard GNN backbone for local training. Clients exchange only the model updates required by FedAvg; no node features or intermediate node embeddings are exchanged during reconstruction or training.

## Guardrails

- Do not show FedProp inventing edges unless the method reconstructs topology.
- Do not imply L2 topology is free.
- Do not imply formal privacy guarantees.
