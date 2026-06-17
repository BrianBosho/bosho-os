---
title: "FedProp Literature Synthesis and Borrowing Map"
type: literature-synthesis
source: google-drive
drive-id: 1vu2oaOJMsVEbCy8KCjYKtgMRHUjz1mMSmC8ZdHEl3WI
created: 2026-05-01
tags: [fedprop, literature, synthesis, borrowing-map, two-paper-strategy, tmlr]
project: tmlr_fedprop_paper
---

# FedProp Literature Synthesis and Borrowing Map

*For the main FedProp/TMLR paper and the propagator/operator-analysis paper*

## Purpose

This document consolidates the literature, reviewer feedback, current experimental plans, and emerging theory ideas around FedProp. The goal is to decide what each source gives us, what we can safely borrow, where it belongs, and which ideas should be moved into a second paper.

## Core Decision

We should treat the work as two related but distinct papers.

**Paper 1: FedProp main paper / TMLR revision.** Thesis: FedProp is a communication-free local imputation method for Subgraph-FL. It reconstructs missing cross-client neighbor features through local propagation, with no extra inter-client feature exchange. Its strength is the accuracy/communication tradeoff, not universal SOTA accuracy.

**Paper 2: Propagator/operator-analysis paper.** Thesis: Once FedProp establishes local feature propagation as a useful communication-free mechanism, the next scientific question is how to evaluate and choose propagation operators intrinsically, independent of downstream GNN accuracy. This becomes a systematic study of operators, graph regimes, homophily, non-IID partitions, convergence, and compute.

## Executive Synthesis

The literature should be used in three ways:

1. **To ground FedProp theoretically.** Feature propagation, Dirichlet energy minimization, harmonic extension, heat-equation dynamics, convergence, and spectral-gap language should be used to make the FedProp method mathematically clean.

2. **To position FedProp against prior FGL methods.** FedGCN, FedGAT, FedSage+, FedDEP, FedCog, FedNI, OpenFGL, and related benchmark papers should be used to explain what class of problem FedProp solves and what tradeoffs it makes.

3. **To sharpen the limitation story.** Heterophily, high-frequency graph signals, boundary bias, and imputation discrepancy should not be treated as embarrassing weaknesses. They should be turned into a disciplined theory-backed discussion: FedProp works when smooth harmonic extension is reasonable; it fails or weakens when the graph violates this assumption.

---

## PART I — MAIN FEDPROP PAPER / TMLR REVISION

### 1. Paper Identity

The revised FedProp paper should be framed as follows:

FedProp is a model-agnostic, communication-free federated GNN preprocessing framework for Subgraph-FL. It treats missing cross-client neighbors as a local feature-imputation problem. Each client imputes remote neighbor features using local propagation with fixed known boundary features, then trains a standard GNN under FedAvg.

**The main claim is not:** "FedProp beats every federated GNN baseline."

**The main claim is:** "FedProp recovers a large fraction of the missing-neighbor performance gap while preserving the same inter-client communication profile as FedAvg."

This distinction is essential. Several reviewers judged the paper as an accuracy-only method and therefore compared it unfavorably to FedGCN/FedGAT in settings where those methods communicate neighbor information. The revised paper must lead with the tradeoff: accuracy recovered per byte of extra communication.

### 2. Source Map for Paper 1

#### 2.1 Rossi et al. — Feature Propagation for Missing Node Features

Role: theoretical foundation and conceptual ancestor.

What to borrow: Missing node features can be reconstructed by propagating known features over a graph. Feature propagation corresponds to minimizing Dirichlet energy subject to known-feature constraints. The solution is a harmonic extension of boundary features. Iterative propagation avoids expensive matrix inversion. The method is powerful on homophilic/smooth-feature regimes.

How to integrate: Background — introduce feature propagation as the centralized ancestor. Method — state that FedProp adapts this idea to the Subgraph-FL missing-neighbor setting. Theory — use the Dirichlet minimization and harmonic extension view. Related work — explicitly say FedProp is not claiming novelty for centralized FP; the contribution is the federated, communication-free, missing-cross-client-neighbor deployment.

Language to use: "FedProp adapts the feature propagation principle to Subgraph-FL, where the missing features are not randomly missing entries in a centralized graph but cross-client neighbor features unavailable under federated constraints."

Do not overclaim: Do not imply that FedProp invents feature propagation or Dirichlet energy minimization. The novelty is the federated problem setup, communication-free local deployment, and empirical/theoretical tradeoff analysis.

#### 2.2 Di Giovanni et al. — Understanding Convolution on Graphs via Energies

Role: theoretical support for heterophily/high-frequency limitation.

What to borrow: Graph convolution can be understood through its effect on Dirichlet energy. Message passing and smoothing tend to suppress high-energy/high-frequency components. In heterophilic graphs, useful discriminative information may live in high-frequency components. Smoothing-based methods are therefore structurally limited in heterophilic regimes.

How to integrate: Theory/Discussion — connect the irreducible term in FedProp's error decomposition to high-frequency signal not recoverable by smooth harmonic extension. Limitations — explain why FedProp may weaken on Texas/Wisconsin. Experiments — motivate heterophilic stress tests as a validation of the theory.

Careful wording: Say "The irreducible term captures the portion of the true feature signal that cannot be recovered by a smooth harmonic extension. This is expected to grow in heterophilic or high-frequency regimes." Avoid saying "The irreducible error equals heterophily." That is too strong and may be mathematically attacked.

#### 2.3 Calder et al. / harmonic extension degeneracy literature

Role: limitation and failure-regime support.

What to borrow: Harmonic extension can degenerate when boundary information is too sparse or poorly distributed. If the known boundary set is weak, the solution may become nearly constant or overly dominated by local anchors. This connects naturally to sparse subgraphs and high missing-neighbor fractions.

How to integrate: Discussion — FedProp quality depends on the quality and coverage of local boundary features. Limitations — very sparse graphs, extreme non-IID partitions, and weak boundary coverage may reduce imputation quality. Experimental analysis — report missing-neighbor fraction and boundary coverage per client.

#### 2.4 Spectral-gap / graph diffusion stability literature

Role: convergence-rate support.

What to borrow: The convergence rate of diffusion-like propagation is controlled by spectral gap / contraction of the unknown-node block. Operators may have the same fixed-point goal but different convergence speeds.

How to integrate: Main theory — bring the convergence condition into the main text, not only appendix. Appendix — give a sharper spectral-gap rate statement. Propagator paper — use this as a major axis for operator comparison. Main paper use should be minimal — one or two sentences.

#### 2.5 FedGCN

Role: same-protocol transmission-based competitor.

What to borrow: FedGCN is the closest GCN-family baseline for the same general Subgraph-FL/missing-neighbor issue. It solves missing-neighbor aggregation by communicating encrypted neighbor features in a pre-training/setup phase. It is therefore a strong accuracy baseline but not a zero-extra-communication baseline.

Key narrative: "FedGCN buys accuracy using a neighbor-feature exchange mechanism. FedProp sacrifices some accuracy in hard regimes but removes that extra communication path."

#### 2.6 FedGAT

Role: GAT-family transmission/approximation competitor and model-agnosticity test.

What to borrow: FedGAT inherits centralized GAT hyperparameters and uses polynomial/Chebyshev-style approximations for attention. It is a strong attention-based federated graph baseline.

How to integrate: Add direct FedProp-GAT vs FedGAT table in main paper. Do not compare FedProp-GCN against FedGAT as if backbone differences are irrelevant. Use GAT experiments to support the model-agnosticity claim.

Key narrative: "FedProp is a preprocessing framework. Its claim must be tested with both GCN and GAT backbones."

#### 2.7 FedSage+

Role: generative missing-neighbor baseline.

Key distinction: FedSage+ learns a generator and can require extra training/communication complexity. FedProp uses no additional learnable imputation model.

#### 2.8 FedDEP

Role: stronger recent generative/imputation baseline.

Key distinction: FedDEP tries to generate richer neighbor information; FedProp tries to get useful performance from a smoothness prior without learning an imputer.

#### 2.9 FedCog

Role: novelty threat and required contrast.

What to borrow: FedCog considers coupled graphs and uses border-node information across clients. It can approximate or recover cross-client propagation more directly, but it requires sharing border embeddings / intermediate information between clients. It is not "the same as FedProp" because FedProp performs local imputation without per-round cross-client propagation.

Suggested comparison table:

| Method | Strategy | Extra inter-client communication | Learns imputer? | FedProp distinction |
|:-:|:-:|:-:|:-:|:-:|
| FedCog | Shares border/intermediate embeddings | Yes, per round or repeated | No generator, but cross-client propagation | FedProp avoids cross-client embedding exchange |
| FedGCN/FedGAT | Shares neighbor features/approximations | Yes, setup/pretraining | No | FedProp uses no neighbor-feature exchange |
| FedSage+/FedDEP | Generates missing neighbors/features | Often additional model/communication | Yes | FedProp has no learned imputer |
| FedProp | Local smooth feature imputation | No extra feature communication | No | Lightweight but approximate |

#### 2.10 OpenFGL

Role: benchmark/context source. Use to discipline terminology, align with FGL taxonomy. Do not overuse — OpenFGL is not necessarily a direct baseline unless we run through the benchmark.

#### 2.11 FedNI / network inpainting

Role: related imputation method, especially in medical/population graphs. In related work under "learned imputation / inpainting methods." Contrast with FedProp's non-parametric propagation.

#### 2.12 APPNP / PPR / heat kernel / Chebyshev propagation literature

Role: operator vocabulary and future/operator-paper foundation.

How to integrate in Paper 1: Keep minimal — mention that FedProp currently studies Adj and Diffusion, and other valid operators are future work or appendix. Do not turn Paper 1 into a seven-operator study.

How to integrate in Paper 2: This becomes central — operator families, spectral behavior, intrinsic reconstruction, convergence, compute.

### 3. Concepts to Borrow for Paper 1

#### 3.1 Three-Part Error Decomposition

This should become the central discussion frame.

**Term 1: Propagation/convergence error.** The transient error between the current iterate and the propagation fixed point. Decays with iterations; not the main limitation after convergence.

**Term 2: Boundary bias.** The persistent error caused by the available local boundary features being an imperfect basis for remote features. Borrowed from harmonic extension theory. Use to explain non-IID degradation and sparse boundary failures.

**Term 3: Irreducible heterophily / high-frequency error.** The part of the true feature signal that violates the smoothness assumption and cannot be recovered by harmonic propagation. Use to explain Texas/Wisconsin and heterophily limitation.

This is one of the strongest theoretical assets of the paper. It should not be buried in the appendix.

#### 3.2 Task-Useful Imputation, Not Perfect Reconstruction

Reviewer concern: "How can consistency between imputed and real features be guaranteed?"

Answer: We do not guarantee perfect reconstruction. FedProp aims for task-useful local approximations that improve message passing under communication constraints. The oracle FedProp-Full and intrinsic reconstruction metrics quantify the remaining discrepancy.

Where to add: Method section after imputation definition. Discussion section before limitations. Experimental section with feature reconstruction metrics.

#### 3.3 Information Model / Assumption Table

This is mandatory. Need to specify separately:

- What the client knows under L=1.
- What the client knows under L=2.
- Whether boundary edges are known.
- Whether remote node IDs are known.
- Whether remote features are known.
- Whether remote-remote edges are known.
- What graph is used for propagation.
- What graph is used for GNN training.
- How degrees/normalization are computed.

Suggested table:

| Information item | L=1 strict | L=2 relaxed | Used in propagation? | Used in GNN training? |
|:-:|:-:|:-:|:-:|:-:|
| Local node features | Yes | Yes | Yes | Yes |
| Local-local edges | Yes | Yes | Yes | Yes |
| Boundary incidence | Yes / assumed metadata | Yes | Yes | Yes if augmented training graph used |
| Remote node features | No | No | Imputed | Imputed |
| Remote-remote edges | No | Possibly server-provided | No for strict; yes for L=2 | Clarify |
| Labels of remote nodes | No | No | No | No |

#### 3.4 Communication Language

Replace "strong privacy" with "zero additional inter-client feature communication" and "local-only feature reconstruction."

Use privacy claims carefully: FedProp avoids raw feature exchange; avoids border embedding exchange; is compatible with SecAgg/DP for model updates; does not by itself prove formal differential privacy; L=2 topology assumptions must be discussed as setup metadata leakage.

### 4. Experiments to Integrate into Paper 1

#### 4.1 Main Accuracy Table

Must include: Cora, Citeseer, Pubmed; Amazon Computers and Photos if already run; OGBN-Arxiv if stable; IID and non-IID rows; GCN backbone; Centralised, FedProp-Full, FedProp-Zero, FedProp-Adj, FedProp-Diff, FedGCN.

Narrative: Do not lead with "we beat SOTA." Lead with "we close the gap under zero extra communication."

#### 4.2 GAT Table

Must include: FedProp-GAT variants; FedGAT baseline; same splits and partitions where possible.

Narrative: FedProp is not tied to GCN. It is a preprocessing layer that can feed any message-passing GNN.

#### 4.3 Communication-Efficiency Figure

Plot: X-axis = communication efficiency or extra bytes transferred. Y-axis = accuracy.

Better framing: If plotting raw cost, FedProp sits far left. If plotting efficiency, FedProp can appear in the desirable upper-right quadrant.

Narrative: FedProp may not always dominate accuracy, but it can dominate the Pareto tradeoff.

#### 4.4 Gap-Closed / Recovery Plot

Formula: Gap closed = (FedProp - Zero) / (Full or Centralized - Zero)

#### 4.5 Heterophily Experiment

Datasets: Texas and/or Wisconsin. Synthetic heterophily fallback if integration fails.

Metrics: Accuracy, Feature reconstruction MSE, Cosine similarity, Recovery ratio vs zero imputation, Missing-neighbor fraction, Homophily ratio.

Narrative: This is not just a limitation. It is a theory-validation experiment showing when the smoothness prior breaks.

#### 4.6 Intrinsic Reconstruction Metrics

Add for at least Cora/Citeseer/Pubmed and heterophilic dataset: Reconstruction MSE, Cosine similarity, Recovery ratio, MSE vs accuracy correlation.

Main sentence: "We evaluate imputation directly, not only through downstream accuracy, because downstream GNN training can mask or amplify reconstruction errors."

### 5. Section-by-Section Integration Plan for Paper 1

**Introduction:** Reframe as communication-free missing-neighbor recovery. State that the objective is accuracy/communication tradeoff. Add one sentence that FedProp is approximate and smoothness-dependent.

**Related Work:** Organize into four subsections: (1) Centralized feature propagation and graph diffusion. (2) Transmission-based federated GNNs: FedGCN, FedGAT, FedCog. (3) Generative/inpainting federated GNNs: FedSage+, FedDEP, FedNI. (4) Benchmarks and broader FGL context: OpenFGL and related benchmark papers.

**Problem Setup and Information Model:** Add formal assumption table. Clarify L=1 vs L=2. Clarify boundary edges. Clarify propagation graph and training graph.

**Method:** Define FedProp-Adj and FedProp-Diff precisely. Fix notation issues: do not call I - hL "normalized adjacency." Explain boundary reset. Explain that imputation is task-useful, not perfect.

**Theory:** Separate convergence from optimality. Convergence — affine recursion, contraction on unknown block. Optimality — fixed point equals Dirichlet minimizer only under the right Laplacian/Euler conditions. Add three-part error decomposition.

**Experiments:** Lead with table/figure structure tied to claims. Add reconstruction diagnostics. Add heterophily limitation. Add GAT comparison.

**Discussion:** Build around: (1) When FedProp works. (2) Why non-IID can hurt. (3) Why heterophily can break the smoothness prior. (4) Why communication-free still matters.

**Limitations:** Must include: Homophily dependence, Boundary/topology assumptions, No formal DP guarantee, L=2 setup cost and topology leakage, Potential compute cost on dense client subgraphs, Node classification scope.

### 6. What NOT to Add to Paper 1

Do not add all seven propagation operators to the main FedProp revision unless the current paper needs a major new contribution. This will expand scope and delay submission.

Do not overemphasize APPNP/PPR/Chebyshev in the main paper. Keep them as future work or appendix unless results are already strong and clean.

Do not claim universal privacy. Use precise communication language.

Do not compare across incompatible protocols without a disclaimer. FedSage+/FedDEP results from Louvain + inductive splits should not be placed beside Dirichlet + Planetoid results as if they are apples-to-apples.

---

## PART II — PROPAGATOR / OPERATOR-ANALYSIS PAPER

### 1. Paper Identity

"On the Role of Propagation Operators in Communication-Free Subgraph Federated Learning"

Thesis: FedProp shows that communication-free local propagation can work. However, downstream accuracy alone cannot tell us whether propagation itself is good, and only a small subset of operators has been evaluated. This paper introduces intrinsic propagation evaluation and systematically studies operator choice across graph regimes.

This is not just a FedProp ablation. It is a methods-analysis paper.

### 2. Core Research Gap

Existing FedProp-style evaluation has two problems:

1. Downstream accuracy is confounded. A GNN may compensate for poor imputation, or good imputation may not improve classification if the task does not need the recovered features.

2. Operator coverage is narrow. Adjacency and diffusion are only two choices. PPR/APPNP, random walk, heat kernel, Chebyshev approximations, and exact heat references may behave differently across homophily, sparsity, and non-IID regimes.

### 3. Research Questions for Paper 2

**RQ1:** How well do different propagation operators reconstruct missing neighbor features independently of downstream GNN training? Metrics: MSE, cosine similarity, recovery ratio, spectral fidelity.

**RQ2:** How do operators differ in convergence behavior? Metrics: residual decay, iterations to convergence, feature-change norm, spectral-gap proxy.

**RQ3:** How does graph homophily govern the limits of local propagation? Metrics: reconstruction quality vs homophily; Texas/Wisconsin; synthetic homophily sweep if possible.

**RQ4:** How does partition non-IIDness affect propagation quality, independently of the downstream task? Metrics: beta sweep; missing-neighbor fraction; boundary coverage; per-client variance.

**RQ5:** How do operators compare computationally? Metrics: wall-clock time, iteration count, sparse-matrix cost, memory footprint, scaling to OGBN-Arxiv.

**RQ6:** When does intrinsic propagation quality translate into downstream accuracy? Metrics: correlation between reconstruction MSE/cosine/recovery ratio and final test accuracy across datasets/operators/backbones.

### 4. Literature Integration for Paper 2

| Source | Borrow | Extend |
|:-:|:-:|:-:|
| Rossi et al. FP | Feature propagation as missing-feature reconstruction, harmonic extension view, reconstruction metrics | FedProp's missing features arise from federated partitioning, not random masking |
| Di Giovanni et al. | Energy-based view of graph convolution, high-frequency signal loss under smoothing, heterophily as stress regime | Measure whether intrinsic reconstruction error rises as homophily decreases |
| APPNP / PPR | Personalized propagation with restart, geometric decay, better long-range signal control | APPNP/PPR may reduce oversmoothing in sparse boundary regimes; fixed point is not exactly Dirichlet minimizer |
| Heat kernel | Continuous-time heat equation, spectral attenuation, exact heat kernel as theoretical reference | Heat kernels may produce smoother but possibly over-smoothed imputations |
| Chebyshev | Polynomial approximation to spectral filters, higher-order accuracy, K-tradeoff | Chebyshev may be more efficient on larger/dense graphs; requires K sensitivity analysis |
| Random Walk | Asymmetric diffusion, different stationary behavior | Treat as comparison baseline; does not converge to same Dirichlet minimizer |

### 5. Operator Set for Paper 2

Primary operators: (1) Normalized adjacency, (2) Random walk, (3) Euler/Taylor diffusion, (4) Chebyshev heat approximation, (5) Exact heat kernel reference on small graphs, (6) APPNP/PPR, (7) Personalized PageRank/random-walk variant.

For each operator, document: Formula, Symmetry, Fixed point interpretation, Whether it is a Dirichlet solver, Per-iteration cost, Memory cost, Parameters, Expected failure mode.

### 6. Intrinsic Metrics for Paper 2

- **Feature reconstruction MSE:** Primary error metric against true withheld remote features.
- **Cosine similarity:** Captures directional reconstruction quality; useful for high-dimensional sparse features.
- **Recovery ratio:** (MSE_zero - MSE_operator) / MSE_zero — measures improvement over zero imputation.
- **Spectral fidelity:** Compares covariance/spectral structure of imputed features vs true features.
- **Dirichlet residual:** Measures process convergence: ||L X^(t)||_F².
- **Feature-change norm:** Measures numerical stabilization: ||X^(t+1) - X^(t)||_F.
- **Downstream correlation:** Measures whether intrinsic quality predicts accuracy.

### 7. Dataset Plan for Paper 2

Core datasets: Cora, Citeseer, Pubmed, OGBN-Arxiv, Texas, Wisconsin. Optional appendix datasets: Amazon Computers, Amazon Photos.

### 8. Experimental Layers for Paper 2

**Layer 1 — Intrinsic reconstruction:** No GNN training. Run each operator and measure imputation quality.

**Layer 2 — Process/convergence:** Log residuals, feature changes, iterations, wall-clock time.

**Layer 3 — Computational efficiency:** Compare theoretical cost and empirical wall-clock cost.

**Layer 4 — Downstream accuracy:** Run GCN/GAT only where needed to test whether intrinsic quality translates to task performance.

### 9. Figures and Tables for Paper 2

- Table 1: Operator taxonomy. Columns: operator, formula, symmetry, fixed point, cost, parameter, expected behavior.
- Figure 1: Reconstruction quality by operator and dataset. Metric: MSE or recovery ratio.
- Figure 2: Residual decay curves. Shows convergence differences.
- Figure 3: Homophily vs reconstruction error. Key theory-validation figure.
- Figure 4: Beta / non-IID sweep. Shows partition severity effect independent of training.
- Figure 5: Runtime vs reconstruction quality. Shows efficiency/quality tradeoff.
- Figure 6: Intrinsic quality vs downstream accuracy correlation. Answers whether intrinsic metrics matter.

### 10. What Paper 2 Borrows from Paper 1

From FedProp it inherits: Subgraph-FL problem setting, accessible subgraph construction, boundary reset iteration, Adj and Diff operators, existing training pipeline, FedAvg downstream evaluation, motivation from missing cross-client neighbors.

What Paper 2 adds: Direct feature-level evaluation, larger operator family, convergence/process instrumentation, operator complexity analysis, homophily and non-IID regime characterization, practical operator-selection guidance.

### 11. What Should Stay Separate

Paper 1 should not become an operator benchmark. Paper 2 should not re-argue the entire FedProp method as if it is new.

Paper 1 sells the method. Paper 2 studies the mechanism.

---

## PART III — SHARED BORROWING TABLE

| Source / Concept | Borrow for Paper 1 | Borrow for Paper 2 | Risk / Caution |
|:-:|:-:|:-:|:-:|
| Rossi et al. FP | Dirichlet energy, harmonic extension, FP foundation | Intrinsic reconstruction protocol | Do not claim FP novelty |
| Di Giovanni energy view | Heterophily/high-frequency limitation | Homophily vs error prediction | Avoid saying irreducible error equals heterophily |
| Calder / harmonic degeneracy | Boundary sparsity limitation | Boundary coverage analysis | Use as limitation, not core theorem unless formalized |
| Spectral-gap diffusion work | Convergence-rate language | Operator convergence comparison | Keep main-paper use concise |
| FedGCN | Same-protocol transmission baseline | Communication/accuracy reference | Make communication cost explicit |
| FedGAT | GAT baseline and model-agnosticity test | Attention backbone downstream layer | Do not compare GCN vs GAT unfairly |
| FedSage+ | Generative missing-neighbor positioning | Optional baseline/context | Protocol mismatch unless reproduced |
| FedDEP | Stronger recent neighbor-generation positioning | Optional baseline/context | Same protocol issue |
| FedCog | Novelty threat; contrast table | Communication-heavy alternative | Must be discussed explicitly |
| OpenFGL | Benchmark taxonomy and terminology | Possible benchmark alignment | Do not imply comparison unless run |
| FedNI | Learned inpainting family | Context for imputation methods | Domain/protocol differences |
| APPNP/PPR | Future work/operator note | Core operator family | Fixed point not Dirichlet minimizer |
| Heat kernel | Diffusion interpretation | Core operator/reference | Exact heat is expensive/dense |
| Chebyshev | Approximation note | Core operator family | Parameter K sensitivity required |
| Random walk | Maybe appendix | Baseline operator | Asymmetric; different fixed point |
| Texas/Wisconsin | Heterophily limitation | Homophily-regime test | Small datasets; report variance |
| Amazon datasets | Broader validation | Dense homophilic regime | Appendix or main if results clean |
| OGBN-Arxiv | Scale validation | Scaling/runtime test | Compute stability required |

---

## PART IV — ACTION CHECKLIST

### Immediate Actions for Paper 1

1. Rewrite abstract/introduction around communication-free recovery, not universal SOTA.
2. Add information-model table for L=1 and L=2.
3. Clarify propagation graph, training graph, and normalization.
4. Add FedCog contrast paragraph/table.
5. Add GAT comparison in main paper.
6. Add heterophilic result or synthetic heterophily fallback.
7. Add direct imputation metrics: MSE, cosine similarity, recovery ratio.
8. Rebuild results around communication efficiency and gap closed.
9. Move three-part error decomposition into main discussion.
10. Replace strong privacy claims with precise communication/privacy language.

### Near-Term Actions for Paper 2

1. Implement Chebyshev, APPNP/PPR, random walk, and exact heat reference.
2. Add intrinsic evaluation mode to propagation loop.
3. Log residuals, feature-change norms, MSE over iterations, iterations to convergence, wall-clock time.
4. Run propagation-only matrix before any GNN downstream training.
5. Create operator taxonomy table.
6. Run Texas/Wisconsin to test homophily limitation.
7. Run beta sweep to test non-IID effects.
8. Correlate intrinsic metrics with downstream accuracy.

### Final Strategic Guidance

The literature does not tell us that FedProp is weak. It tells us how to make the contribution more precise.

The revised main paper should say: FedProp is the simplest useful point in the federated GNN design space: no generator, no neighbor-feature exchange, no border-embedding sharing, only local smooth imputation. It works when the graph-feature signal is sufficiently smooth and boundary information is informative. It fails predictably when that assumption breaks.

The second paper should say: If communication-free propagation is a valid design point, then operator choice, intrinsic reconstruction quality, convergence behavior, and graph regime sensitivity deserve their own systematic study.

That split gives us two coherent papers instead of one overloaded paper.
