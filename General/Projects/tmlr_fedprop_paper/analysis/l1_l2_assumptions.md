---
type: analysis-note
status: draft
project: tmlr_fedprop_paper
tags: [fedprop, analysis, assumptions]
---

# L1 and L2 Assumptions

## Purpose

Prevent the contribution from depending on an ambiguous topology assumption.

## L1 Assumption Model

The client knows:

- Local nodes.
- Local node features.
- Local edges.
- Boundary incidence: which local nodes have cross-client neighbors.
- Placeholder identities or structural slots for one-hop remote neighbors, if required by the method.

The client does not know:

- Remote node features.
- Remote labels.
- Remote-remote edges.
- Other clients' full subgraphs.

## L2 Assumption Model

The client receives or otherwise has access to richer two-hop structural context. This can improve performance, but it may imply a setup cost or stronger availability assumption.

P1 wording should treat L2 as:

- Extended-structure.
- Oracle-topology.
- A variant whose setup cost must be accounted for if claimed as practical.

## Paper Implication

The primary FedProp contribution should rest on L1. L2 can demonstrate potential benefit from richer topology, but should not carry the unqualified zero-additional-communication claim.
