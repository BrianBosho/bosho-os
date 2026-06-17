Yes—this is the right way to prevent the project from expanding uncontrollably. Treat the three papers as **three explicit scope levels**, with a freeze point between each one.

## P1 — Complete paper using only current evidence

**Purpose:** Produce a coherent, submission-shaped manuscript that accurately reflects what has already been completed.

P1 should involve:

- Reorganizing the argument.
    
- Rewriting unclear sections.
    
- Redrawing Figure 2.
    
- Consolidating existing tables and figures.
    
- Removing unsupported or overly broad claims.
    
- Clearly distinguishing L1 and L2 assumptions.
    
- Reframing the contribution around communication-free feature reconstruction.
    
- Adding limitations based on what the current results do and do not show.
    
- Moving peripheral material to the appendix.
    

P1 should **not** include:

- New experiments.
    
- New datasets.
    
- New baselines.
    
- New reconstruction metrics.
    
- New topology analysis.
    
- New theoretical results.
    
- New recovery calculations, unless they have already been computed.
    
- Attempts to answer every open reviewer question.
    

The goal is not to make P1 definitive. The goal is to determine:

> What is the strongest complete and internally consistent paper supported by the evidence we already have?

### Likely P1 contribution

The contribution can be framed approximately as:

> FedProp treats inaccessible cross-client node features as missing graph information and reconstructs them locally through feature propagation. Across the evaluated citation and OGBN-Arxiv benchmarks, FedProp improves federated GCN and GAT performance without requiring inter-client feature exchange or an additional learned reconstruction model.

This is narrower than some of the current claims, but likely supportable.

### P1 deliverable

A complete manuscript with:

1. Final narrative and section ordering.
    
2. Revised abstract and introduction.
    
3. Corrected problem formulation.
    
4. Revised methodology section.
    
5. New Figure 2.
    
6. Reorganized existing experimental results.
    
7. Revised related work.
    
8. Limitations and conclusion.
    
9. A list of claims that remain weak or unverified.
    

P1 becomes the **baseline document** from which all later decisions are made.

---

## Gap assessment between P1 and P2

Once P1 is complete, evaluate every major claim using a claim–evidence matrix:

|Claim|Existing evidence|Current weakness|Required addition|
|---|---|---|---|
|FedProp improves local federated GNN training|Existing GCN/GAT results|Improvement is not consistently contextualized|Performance-recovery analysis|
|FedProp adds no communication|Algorithm and protocol description|L1/L2 assumptions may be unclear|Precise communication accounting|
|FedProp is competitive with SOTA|Existing comparison tables|Protocols differ|Controlled baseline or explicit positioning|
|FedProp is model-agnostic|GCN and GAT results|Possibly sufficient already|Better presentation, perhaps no new experiment|
|FedProp is robust to client heterogeneity|Existing partition results|Limited or inconsistent evidence|Partition/client-count analysis|
|FedProp reconstructs useful features|Downstream accuracy|No direct reconstruction evidence|Reconstruction-quality experiment|
|Topology determines when FedProp works|Amazon/heterophilic observations|No systematic evidence|Separate topology-focused study|

This gap assessment should classify additions as:

- **Required for the main claim.**
    
- **Helpful but not required.**
    
- **Belongs to future work.**
    

That classification determines P2 and P3.

---

## P2 — Improved TMLR paper

P2 should be the strongest version of **the same FedProp paper**, not a new research programme.

Its central question should remain:

> Can local feature propagation recover performance lost through graph partitioning without adding graph-data communication?

Only additions that directly strengthen that question belong in P2.

### Recommended P2 additions

#### 1. Performance-recovery analysis

This is probably the highest-value addition.

Compare:

- Full graph.
    
- Zero-hop/local graph.
    
- FedProp-L1.
    
- FedProp-L2.
    
- RPE variants, where available.
    

Report both raw accuracy and the fraction of the full-to-zero-hop degradation recovered by FedProp.

This turns the existing results into a more persuasive argument without changing the algorithm.

#### 2. Precise communication accounting

Clearly distinguish:

- Standard FedAvg model communication.
    
- Additional graph-data communication.
    
- One-time setup communication.
    
- Repeated feature or embedding communication.
    
- Assumed availability of L1 or L2 topology.
    

This is necessary because the primary contribution is communication-related.

#### 3. Communication–accuracy positioning

Compare FedProp with:

- FedGCN.
    
- FedGAT.
    
- FedSage/FedSage+.
    
- Other relevant approaches already discussed.
    

A controlled rerun of FedGCN would be valuable if it is practical. Methods with incompatible protocols can remain literature-based, provided the distinction is explicit.

#### 4. Small reconstruction diagnostic

A limited experiment could show:

- Whether propagated features become more similar to the true hidden features.
    
- Whether better reconstruction tends to correspond to better node-classification performance.
    
- Whether reconstruction differs between selected IID and non-IID settings.
    

This should be one focused subsection, not a new major theme.

#### 5. Focused robustness evidence

Choose one or two of the following, not all of them:

- Number of clients.
    
- Partition parameter.
    
- L1 versus L2.
    
- RPE.
    
- GCN versus GAT.
    

Since GCN/GAT and L1/L2 results already appear central, those should likely remain the main robustness axes. A client-count experiment could be added if reviewers require scalability across federation size.

### What should not enter P2

P2 should not attempt to fully answer:

- How graph topology determines reconstruction difficulty.
    
- Why heterophilic graphs behave differently.
    
- Whether Dirichlet energy predicts reconstruction performance.
    
- Whether FedProp generalizes to link prediction or graph classification.
    
- How to design optimal partitions for feature propagation.
    
- A comprehensive comparison of propagation algorithms.
    
- Formal topology-dependent reconstruction guarantees.
    

These are substantial research questions and would dilute the TMLR paper.

### P2 target structure

1. Introduction and motivation.
    
2. Federated missing-neighbor problem.
    
3. FedProp.
    
4. Communication model and assumptions.
    
5. Experimental setup.
    
6. Performance degradation and recovery.
    
7. Communication–accuracy tradeoff.
    
8. Model and partition robustness.
    
9. Reconstruction diagnostic.
    
10. Limitations.
    
11. Conclusion.
    

---

## P3 — Follow-up paper on topology and reconstructability

P3 should be a distinct paper with a different central research question:

> Under what graph, feature, and partition conditions can missing cross-client information be reconstructed effectively?

This is not merely “more FedProp experiments.” It is a broader study of **reconstructability in federated graphs**.

### Possible P3 research themes

#### Topology and feature smoothness

Study how reconstruction depends on:

- Graph homophily and heterophily.
    
- Feature homophily.
    
- Dirichlet energy.
    
- Spectral properties.
    
- Graph conductance.
    
- Community structure.
    
- Boundary-node density.
    
- Distance from observed to missing nodes.
    

#### Partition-induced missingness

Characterize what changing the partition regime actually does to the graph:

- Cross-client edge ratio.
    
- Number of boundary nodes.
    
- Size of disconnected local regions.
    
- Distribution of remote-neighbor counts.
    
- Structural differences between IID, label-skewed, random, and topology-aware partitions.
    

#### Reconstruction theory

Develop error bounds relating reconstruction error to:

- Graph Laplacian structure.
    
- Smoothness of the feature signal.
    
- Placement of observed nodes.
    
- Connectivity of unknown regions.
    
- Number of propagation steps.
    

#### Broader empirical evaluation

This is where the following belong:

- Amazon Computers and Photo.
    
- Heterophilic datasets.
    
- OGBN-Products.
    
- More propagation algorithms.
    
- Additional downstream tasks.
    
- Controlled synthetic graphs.
    
- Varying graph homophily independently of label distribution.
    
- Systematic partition sweeps.
    

#### Broader algorithmic extensions

P3 could also consider:

- Adaptive propagation.
    
- Energy-preserving propagation.
    
- Learned propagation coefficients.
    
- Heterophily-aware reconstruction.
    
- Uncertainty estimates for reconstructed features.
    
- Deciding when propagation should not be used.
    

This would give P3 a contribution independent of FedProp’s original communication claim.

---

## Recommended relationship among the three versions

### P1: What do we already have?

A complete, honest manuscript based only on current evidence.

### P2: What is needed to make the FedProp claim convincing?

A bounded set of experiments and analyses directly strengthening performance recovery and communication efficiency.

### P3: What larger scientific question did FedProp expose?

A separate study of graph topology, partitioning, feature smoothness, and missing-information reconstructability.

The important boundary is:

> **P2 explains whether FedProp works and at what communication cost. P3 explains when and why graph-based reconstruction works.**

That separation keeps the TMLR paper focused while preserving the more ambitious topology questions as a legitimate follow-up contribution.