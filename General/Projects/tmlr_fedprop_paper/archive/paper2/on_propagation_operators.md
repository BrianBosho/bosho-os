---
title: "On the Role of Propagation Operators in Communication-Free Subgraph Federated Learning"
type: proto-paper
source: google-drive
drive-id: 1hMwK78oTa_5M9PhBJ8-i5Ax05aaACJLIRAkTuyFjKOI
created: 2026-04-29
tags: [fedprop, propagator, operators, paper2, proto-paper, intrinsic-evaluation, tmlr]
project: tmlr_fedprop_paper
---

# On the Role of Propagation Operators in Communication-Free Subgraph Federated Learning

*Proto-Paper — Research Questions, Theory, and Experimental Protocol*

*Draft — April 29, 2026*

---

## Abstract

In subgraph federated graph learning, clients train GNNs on locally observable subgraphs without access to the features of remote neighbors. Communication-free local feature propagation has emerged as a practical solution: each client iteratively propagates known boundary features into unknown neighbor positions before GNN training, incurring zero inter-client communication. While prior work — specifically FedProp — demonstrates that this approach recovers substantial accuracy under both IID and non-IID partitions, two fundamental questions remain open.

First, existing evaluations measure propagation quality only through downstream classification accuracy, which is a confounded and indirect signal. Second, only two propagation operators (normalized adjacency and a Taylor-approximated diffusion kernel) have been studied; the broader family of valid operators — including Chebyshev approximations, APPNP-style personalized propagation, random walk, and exact heat kernels — remains unevaluated.

This paper addresses both gaps. We establish a rigorous intrinsic evaluation protocol that measures feature reconstruction quality directly, independent of any downstream GNN. We then conduct a systematic empirical and theoretical study of seven propagation operators across eight datasets spanning small-to-large scale, homophilic-to-heterophilic regimes, and IID-to-non-IID partitions. Our analysis reveals how operator choice, graph homophily, partition non-IIDness, and subgraph size jointly determine propagation quality, convergence speed, and computational cost. We derive per-operator theoretical complexity bounds and provide practical guidance on operator selection for practitioners deploying federated GNNs under communication constraints.

---

## 1. Introduction

Federated learning over graph-structured data poses a fundamental challenge absent from standard federated learning: in the subgraph setting, nodes on one client may have edges to nodes held by other clients. When GNN message-passing is applied locally, these cross-client edges are broken, and remote neighbor features are simply missing. This missing-neighbor problem degrades GNN performance relative to centralized training, and the severity of degradation grows with the degree of non-IID partitioning — precisely the condition that federated learning is designed for.

Communication-free feature propagation, as introduced in FedProp, resolves this by having each client locally impute missing neighbor features through iterative propagation before training. The key insight is Dirichlet energy minimization: under a smoothness assumption, the optimal imputation is the harmonic extension of known boundary features into unknown positions, and this can be approximated efficiently by iterating a propagation operator. The result is zero additional inter-client communication beyond standard FedAvg parameter aggregation.

Despite promising empirical results, the approach leaves two gaps unaddressed. The first is measurement: all existing evaluations of propagation quality are downstream. The second gap is operator coverage: FedProp studies two operators, but the theoretical framework supports any operator whose spectral radius is bounded by one and that is a spectral function of the Laplacian. This family includes Chebyshev polynomial approximations, APPNP-style personalized propagation, random walk operators, and the exact heat kernel.

**Contributions:**

- **Intrinsic evaluation protocol**: We define and implement a feature-level evaluation framework measuring propagation quality directly: feature reconstruction MSE, cosine similarity, recovery ratio, spectral fidelity, and convergence diagnostics — all independent of downstream GNN training.
- **Unified operator study**: We systematically compare seven propagation operators under matched conditions across eight datasets.
- **Theoretical complexity analysis**: We derive per-operator bounds on iteration cost, iterations-to-convergence, and total propagation cost, showing how the spectral gap governs the efficiency-accuracy tradeoff.
- **Empirical regime analysis**: We characterize how propagation quality varies with graph homophily, partition non-IIDness, subgraph size, and missing-neighbor fraction.
- **Practical guidance**: We synthesize findings into operator selection recommendations across a range of deployment scenarios.

---

## 2. Research Questions

| | |
|:-:|:-:|
| **RQ1** | **How well do different propagation operators reconstruct missing neighbor features, independently of any downstream GNN?** |
| **RQ2** | **How do operators differ in their convergence behavior and process-level quality?** |
| **RQ3** | **How does graph homophily govern the limits of local feature propagation?** |
| **RQ4** | **How does partition non-IIDness affect propagation quality, independently of the downstream task?** |
| **RQ5** | **How do operators compare in computational efficiency, and how does this scale from small to large graphs?** |
| **RQ6** | **When does good intrinsic propagation quality translate to downstream accuracy gains, and when does it not?** |

RQ2 governs the spectral gap and per-iteration residual decay. RQ3 tests the irreducible error prediction — Term 3 of the error decomposition grows monotonically with heterophily. RQ4 measures how reconstruction MSE and recovery ratio degrade as the Dirichlet concentration parameter β decreases from 10,000 (IID) to 1 (highly non-IID). RQ5 measures empirical wall-clock time from Cora (~5K edges) to OGBN-Arxiv (~1.2M edges) and compares to theoretical predictions.

---

## 3. Background and Problem Setting

### 3.1 Subgraph Federated GNN Learning

In the subgraph federated setting, a graph G = (V, E, X) is distributed across K clients without explicit edge sharing. Client k observes a local subgraph G_k = (V_k, E_k^local, X_Vk), where V_k is its node set, E_k^local contains only edges between nodes in V_k, and X_Vk are the known local features. Nodes in other clients that share an edge with a node in V_k are remote neighbors — their features X_Uk are unknown to client k.

### 3.2 The Accessible Subgraph and L-hop Construction

FedProp introduces the accessible subgraph G_k^(L) = (V_k ∪ U_k, E_k'), where U_k is the set of remote nodes reachable within L hops from V_k, and E_k' includes the boundary edges between V_k and U_k. Under the L=1 (Strict Privacy) model, U_k nodes appear as isolated leaves whose interconnections are unknown. Under the L=2 model, the server provides the 2-hop topology.

The accessible subgraph separates the node set into V_k (known features, boundary nodes) and U_k (unknown features, interior nodes to be imputed). This partition is the foundation of the Dirichlet imputation problem.

### 3.3 Propagation Operators

A propagation operator P is a matrix applied iteratively to the feature matrix X to propagate information across the graph. For use in FedProp, an operator must satisfy: ρ(P) ≤ 1 (guaranteeing convergence), and it must be a spectral function of the graph Laplacian L.

**Table 1: Propagation Operators Under Study**

| **ID** | **Operator** | **Formula** | **Symmetric?** | **Notes** |
|:-:|:-:|:-:|:-:|:-:|
| **O1** | **Norm. Adjacency** | D̃⁻¹/²ÃD̃⁻¹/² (with self-loops) | Yes | Current FedProp baseline |
| **O2** | **Random Walk** | D⁻¹A | No | Asymmetric variant; different fixed point |
| **O3** | **Diffusion / Taylor** | I − hL (truncated Taylor, K terms) | Yes | FedProp-Diff; heat kernel approx. |
| **O4** | **Chebyshev** | Cheby. approx. of heat kernel | Yes | Better for dense graphs (O(K|E|d)) |
| **O5** | **Heat Kernel (exact)** | exp(−tL) | Yes | Theoretical reference; O(n³) |
| **O6** | **APPNP / PPR** | (1−α)Â + αI or PPR closed-form | Yes | Personalized; residual connection |
| **O7** | **Random Walk / PageRank** | Personalized PageRank | No | Graph-global random walk interpretation |

---

## 4. Theoretical Framework

### 4.1 Dirichlet Energy Minimization

The goal of feature propagation is to find the smoothest feature matrix X_Uk that is consistent with the known boundary features X_Vk. Formally, we minimize the local Dirichlet energy:

    E_k(X_k) = (1/2) tr(X_k^T L_k X_k)

subject to the constraint that X_Vk remains fixed at its observed values.

**Proposition 1 (Analytical Solution).** For a connected accessible subgraph G_k^(L), the unique feature matrix X*_Uk that minimizes the Dirichlet energy subject to fixed boundary features X_Vk is given by:

    X*_Uk = − L_UkUk⁻¹ L_UkVk X_Vk

This solution is the discrete harmonic extension of the boundary features into the interior. Direct computation of this inverse is O(|U_k|³) and thus impractical for large subgraphs — motivating the iterative propagation approach.

### 4.2 Convergence of Iterative Propagation

The iterative algorithm applies a propagation operator P_k to the feature matrix at each step, then resets boundary nodes to their true values:

    X_k^(t+1) ← P_k X_k^(t),   then   X_k^(t+1)(v) ← X_Vk^0(v) for all v ∈ V_k

Applying this to the interior block U_k yields the affine recursion:

    X_Uk^(t+1) = P_UkUk X_Uk^(t) + P_UkVk X_Vk^0

**Theorem 1 (Convergence).** For any connected accessible subgraph G_k^(L), if P_k is a spectral function of the Laplacian with ρ(P_k) ≤ 1, then the boundary-reset iteration converges linearly to the unique Dirichlet minimizer X*_Uk. The interior block P_UkUk is a strict contraction (ρ(P_UkUk) < 1) because anchoring the boundary removes the non-contracting λ=1 eigenvector from the interior dynamics.

The rate of convergence is governed by the spectral gap of P_UkUk: operators with a larger spectral gap (faster eigenvalue decay below 1) converge in fewer iterations.

### 4.3 Three-Part Error Decomposition

The total reconstruction error at iteration t decomposes into three independent terms:

    ‖X_Uk^(t) − X_true,Uk‖_F  ≤  Term 1 + Term 2 + Term 3

- **Term 1 — Propagation Convergence Error**: ‖X_Uk^(t) − X*_Uk‖_F ≤ (λ_gap^(U))^t ‖X_Uk^(0) − X*_Uk‖_F. This transient error decays exponentially in t and reaches zero at convergence. In practice, 30–50 iterations suffice. This term depends only on the spectral gap of the operator.

- **Term 2 — Initial Boundary Bias**: ‖(I−P_UU)⁻¹ P_UV (X_Vk^(0) − X_true,Vk)‖_F. This persistent error arises from mismatch between the initial guess and the true remote features. It is irreducible for a given propagation run but could be mitigated by better initialization.

- **Term 3 — Irreducible Heterophily Error**: ‖(I−P_UU)⁻¹ P_UV X_true,Vk − X_true,Uk‖_F. This fundamental error measures the high-frequency signal in the true features that no smooth, harmonic model can recover. It is proportional to the graph's heterophily — the degree to which connected nodes have dissimilar features. This term sets a hard floor on reconstruction quality that no operator can overcome.

Term 3 directly predicts that propagation will fail on heterophilic graphs — not because of operator choice or implementation, but because the smoothness assumption is violated. This prediction is testable and forms the basis of RQ3.

### 4.4 Per-Operator Complexity Analysis

**Table 2: Theoretical Complexity Per Operator**

| **Operator** | **Cost/Iteration** | **Iterations (theory)** | **Total Cost** | **Memory** |
|:-:|:-:|:-:|:-:|:-:|
| **Norm. Adj (O1)** | O(|E|·d) | O(1/λ_gap · log(1/ε)) | O(|E|·d/λ_gap) | O(|V|·d) |
| **Random Walk (O2)** | O(|E|·d) | O(1/λ_gap · log(1/ε)) | O(|E|·d/λ_gap) | O(|V|·d) |
| **Diffusion/Taylor (O3)** | O(K·|E|·d) | Fewer (faster decay) | O(K·|E|·d·T*) | O(|V|·d) |
| **Chebyshev (O4)** | O(K·|E|·d) | Fewer than Taylor | O(K·|E|·d·T*) | O(K·|V|·d) |
| **Heat Kernel exact (O5)** | O(n³) — one-shot | 1 (closed-form) | O(n³) | O(n²) |
| **APPNP/PPR (O6)** | O(|E|·d) | O(1/α · log(1/ε)) | O(|E|·d/α) | O(|V|·d) |

### 4.5 Theoretical Predictions

- **P1 (Homophily threshold)**: Reconstruction MSE scales with Term 3, which grows with heterophily. On graphs with homophily ratio h < 0.3 (Texas, Wisconsin), propagation should provide minimal benefit over zero-hop imputation.
- **P2 (Non-IID degradation)**: More non-IID partitions (lower β) increase the fraction of missing neighbors, weakening the boundary condition. This amplifies Term 2 and worsens reconstruction quality, independently of operator choice.
- **P3 (Operator convergence ordering)**: Operators with larger spectral gaps should converge in fewer iterations. The ordering is theoretically predictable and should be confirmed empirically.
- **P4 (Decoupling of intrinsic and downstream quality)**: On heterophilic graphs, intrinsic reconstruction quality will be poor (high MSE) but downstream accuracy may not degrade proportionally if the GNN's attention mechanism (GAT) can compensate.

---

## 5. Datasets

**Table 3: Dataset Summary**

| **Dataset** | **|V|** | **|E|** | **C** | **d** | **Homophily** | **Type** | **Scale** |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| **Cora** | 2,708 | 5,429 | 7 | 1,433 | 0.81 | Homophilic | Small |
| **Citeseer** | 3,327 | 4,732 | 6 | 3,703 | 0.74 | Homophilic | Small |
| **Pubmed** | 19,717 | 44,338 | 3 | 500 | 0.80 | Homophilic | Medium |
| **Amazon Computers** | 13,752 | 245,861 | 10 | 767 | 0.78 | Homophilic | Medium |
| **Amazon Photos** | 7,650 | 119,081 | 8 | 745 | 0.83 | Homophilic | Medium |
| **OGBN-Arxiv** | 169,343 | 1,166,243 | 40 | 128 | 0.66 | Homophilic | Large |
| **Texas** | 183 | 295 | 5 | 1,703 | 0.11 | Heterophilic | Small |
| **Wisconsin** | 251 | 466 | 5 | 1,703 | 0.20 | Heterophilic | Small |

---

## 6. Experimental Protocol

### 6.1 Partitioning

All datasets are partitioned into K=10 client subgraphs using the label-Dirichlet scheme with β ∈ {10,000 (IID), 10 (mild non-IID), 1 (strong non-IID)}.

### 6.2 Evaluation Layers

**Layer 1 — Intrinsic Feature Reconstruction Quality:** For each client k and each partition β, designate the boundary nodes U_k as the evaluation targets. Their true features X_true,Uk are withheld. Propagation is run to convergence, producing the imputed matrix X*_Uk. This layer answers RQ1 directly.

**Layer 2 — Propagation Process Quality:** Instrument the propagation loop to log at each iteration t: (1) the Dirichlet energy residual ‖LX^(t)‖²_F, (2) the feature change norm ‖X^(t+1) − X^(t)‖_F, and (3) the reconstruction MSE against X_true,Uk. This layer answers RQ2.

**Layer 3 — Computational Efficiency:** Wrap the propagation loop with wall-clock timing. Record time per iteration, total propagation time to convergence, and relative overhead as (propagation time / GNN training time). This layer answers RQ5.

**Layer 4 — Downstream Task Validation:** Train a two-layer GCN and a two-layer GAT on the imputed features from each operator across all datasets and partition regimes. This layer answers RQ6.

### 6.3 Metrics

**Table 4: Evaluation Metrics by Layer**

| **Layer** | **Metric** | **Definition** | **What it measures** |
|:-:|:-:|:-:|:-:|
| **Intrinsic** | **Feature MSE** | ‖X* − X_true‖²_F / |U_k| | How close imputed features are to ground truth |
| **Intrinsic** | **Cosine Similarity** | avg cosine(x*_i, x_true_i) over unknown nodes | Feature direction alignment, scale-invariant |
| **Intrinsic** | **Recovery Ratio** | (MSE_zero − MSE_op) / MSE_zero | How much of the zero-hop→oracle gap is closed |
| **Intrinsic** | **Spectral Fidelity** | ‖cov(X*) − cov(X_true)‖_F | Preservation of feature covariance structure |
| **Process** | **Residual Decay** | ‖LX^(t)‖²_F per iteration t | Rate of Dirichlet energy minimization |
| **Process** | **Feature Change Norm** | ‖X^(t+1) − X^(t)‖_F per iteration | Convergence speed in feature space |
| **Process** | **Iterations to Conv.** | t* s.t. ‖X^(t+1)−X^(t)‖_F < ε | Empirical iterations under fixed tolerance |
| **Efficiency** | **Time/Iteration** | Wall-clock seconds per propagation step | Raw computational cost |
| **Efficiency** | **Total Prop. Time** | Time × iterations to convergence | End-to-end preprocessing cost |
| **Efficiency** | **Relative Overhead** | Prop. time / GNN training time | Practical cost relative to downstream task |
| **Downstream** | **Node Class. Acc.** | Test accuracy on standard splits | Downstream task benefit |
| **Downstream** | **Accuracy Gap Closed** | (acc_op − acc_zero)/(acc_oracle − acc_zero) | How much downstream benefit is recovered |

### 6.4 Full Experiment Matrix

**Table 5: Experimental Factor Matrix**

| **Factor** | **Levels** | **Datasets** | **Metric** | **Layer** |
|:-:|:-:|:-:|:-:|:-:|
| **Operator choice** | 7 operators | All datasets | MSE, cosine sim, iter. to conv. | Intrinsic + Process |
| **IID vs Non-IID** | β=10000, β=10, β=1 | Cora, Citeseer, Pubmed, OGBN | Recovery ratio per β level | Intrinsic |
| **Graph homophily** | h: 0.11 → 0.83 | All + Texas/Wisconsin | MSE vs homophily ratio h | Intrinsic + Downstream |
| **Graph/subgraph size** | Small → Large | Cora → OGBN-Arxiv | Runtime scaling curve | Efficiency |
| **Missing neighbor fraction** | Varies with partition | All datasets | Recovery ratio vs % missing | Intrinsic |
| **Backbone (GNN)** | GCN, GAT | Cora, Citeseer, Pubmed | Downstream accuracy | Downstream |
| **Hop depth (L)** | L=1, L=2 | Cora, Pubmed | MSE + downstream accuracy | Intrinsic + Downstream |
| **Convergence tolerance ε** | 10⁻², 10⁻³, 10⁻⁴ | Cora, OGBN-Arxiv | Iterations + MSE tradeoff | Process |

### 6.5 Operator Configuration

- **Convergence tolerance**: ε = 10⁻⁴ (Frobenius norm of feature change).
- **Maximum iterations**: T_max = 100 for all operators.
- **Step size (h) for Diffusion/Taylor**: h = 0.5/λ_max(L_k), computed per client subgraph.
- **Polynomial order (K) for Taylor/Chebyshev**: K ∈ {3, 5, 10}. K=5 is the default.
- **Personalization parameter (α) for APPNP/PPR**: α = 0.1 (default), ablation at α ∈ {0.05, 0.1, 0.2}.
- **Random seeds**: 5 seeds for all runs. Results reported as mean ± std.

### 6.6 GNN Backbone Configuration (Layer 4)

- **GCN**: Two layers, 16 hidden units, ReLU, dropout 0.5. SGD (lr=0.5, weight decay 5×10⁻⁴) for Cora/Citeseer; Adam (lr=0.01) for Pubmed/Amazon/OGBN.
- **GAT**: Two attention layers, 8 heads × 8 features (hidden 64), ELU, dropout 0.6.
- **Training**: Up to 600 epochs with early stopping (patience=10) on validation loss. FedAvg with synchronous aggregation. K=10 clients, R=100 federation rounds.

---

## 7. Analysis Plan

### 7.1 Primary Operator Comparison (RQ1)

Main Table A: Recovery ratio per operator × dataset × partition regime. Figure 1: Heatmap of recovery ratio across the full operator × dataset matrix. Figure 2: Cosine similarity distributions per operator on Cora and OGBN-Arxiv.

### 7.2 Convergence Analysis (RQ2)

Figure 3: Residual decay curves (log scale) per operator on Cora, Pubmed, and OGBN-Arxiv. Table B: Empirical iterations-to-convergence per operator × dataset. Figure 4: Convergence speed vs reconstruction quality at convergence.

### 7.3 Homophily Sensitivity (RQ3)

Figure 5: Scatter plot of recovery ratio vs homophily ratio h across all datasets and operators. The theoretical prediction is a monotone positive relationship (higher h → better recovery). Detailed analysis of Texas and Wisconsin.

### 7.4 Non-IID Sensitivity (RQ4)

Figure 6: Recovery ratio vs β (log scale) per operator, showing how each operator degrades under increasing non-IIDness. Per-client analysis: recovery ratio vs client's missing-neighbor fraction.

### 7.5 Efficiency and Scaling (RQ5)

Figure 7: Log-log plot of total propagation time vs graph size (|E|) per operator. Table C: Relative overhead (propagation time / GNN training time). Figure 8: Efficiency frontier — recovery ratio vs total propagation time.

### 7.6 Intrinsic vs Downstream Correlation (RQ6)

Figure 9: Scatter plot of recovery ratio (Layer 1) vs accuracy gap closed (Layer 4) across all operator × dataset × partition combinations. Heterophilic case: on Texas and Wisconsin, does low recovery ratio predict low accuracy gain? Or does GAT's attention mechanism compensate?

---

## 8. Open Questions and Discussion Topics

- **Why can propagation sometimes outperform the oracle?** The oracle provides true remote features, which may be noisy or out-of-distribution relative to the local client. Propagation imposes a smoothness prior that may regularize these features beneficially.
- **Is the L=1 vs L=2 topology distinction meaningful for operator quality?** Under L=2, the interconnections of remote nodes are known and included, which may advantage operators exploiting higher-order neighborhood structure.
- **How should operators be selected in practice?** The answer likely depends on graph size (Adj/RW for large sparse; Chebyshev for medium dense), homophily (any for high h; APPNP-style for low h), and compute budget.
- **What are the limits of the smoothness assumption?** Understanding how gracefully propagation degrades as homophily decreases — and whether there is a sharp threshold or a gradual decline — is an important empirical question.
- **Learnable propagation operators**: The current study establishes the baseline against which learnable operators should be evaluated.

---

## 9. Planned Figures and Tables

| **Item** | **Name** | **Content** |
|:-:|:-:|:-:|
| **Table A** | **Operator Recovery Matrix** | Recovery ratio per operator × dataset × partition. Primary result table. |
| **Table B** | **Convergence Summary** | Empirical iterations-to-convergence vs theoretical prediction per operator × dataset. |
| **Table C** | **Efficiency Overhead** | Propagation time / GNN training time per operator × dataset. |
| **Table D** | **Downstream Accuracy** | Node classification accuracy (mean ± std) per operator × dataset × backbone. |
| **Figure 1** | **Recovery Ratio Heatmap** | Full operator × dataset heatmap of recovery ratio. Datasets ordered by homophily. |
| **Figure 2** | **Cosine Similarity Distributions** | Box plots of per-node cosine similarity on Cora and OGBN-Arxiv. |
| **Figure 3** | **Residual Decay Curves** | Log-scale Dirichlet energy residual per iteration for all operators on 3 datasets. |
| **Figure 4** | **Convergence vs Quality Frontier** | Scatter: iterations-to-convergence vs MSE at convergence per operator. |
| **Figure 5** | **Homophily Sensitivity** | Recovery ratio vs homophily ratio h across all datasets and operators. |
| **Figure 6** | **Non-IID Sensitivity** | Recovery ratio vs β (IID→non-IID) per operator on representative datasets. |
| **Figure 7** | **Efficiency Scaling** | Log-log: propagation time vs |E| per operator. Shows theoretical slope. |
| **Figure 8** | **Efficiency Frontier** | Pareto: recovery ratio vs total propagation time per operator. |
| **Figure 9** | **Intrinsic vs Downstream Correlation** | Scatter: recovery ratio (Layer 1) vs accuracy gap closed (Layer 4). |

---

## 10. Instrumentation Checklist

- **[NEW] Feature reconstruction logging**: At convergence, save X*_Uk and compute MSE, cosine similarity, and recovery ratio against X_true,Uk.
- **[NEW] Per-iteration diagnostics**: Inside the propagation loop, log ‖LX^(t)‖²_F and ‖X^(t+1) − X^(t)‖_F at each iteration t.
- **[NEW] Wall-clock timing**: Wrap propagation loop with time.perf_counter() calls.
- **[NEW] Chebyshev operator**: Implement Chebyshev polynomial approximation of the heat kernel. Parameterize by order K.
- **[NEW] APPNP/PPR operator**: Implement personalized propagation: P = (1−α)Â + αI style. Parameterize by α.
- **[NEW] Random Walk operator**: Implement asymmetric D⁻¹A propagation. Treat as comparison baseline (does not converge to Dirichlet minimizer).
- **[DONE] Normalized Adjacency (O1)**: Already implemented as FedProp-Adj.
- **[DONE] Diffusion / Taylor (O3)**: Already implemented as FedProp-Diff.
- **[DONE] IID / non-IID partitioning**: β ∈ {10000, 10, 1} already implemented.
- **[DONE] GCN and GAT backbones**: Both already implemented and producing results.
- **[DONE] All eight datasets**: All datasets are partitioned and accessible.
- **[DONE] Downstream accuracy logging**: Per-client and aggregate test accuracy already saved.

---

## 11. Submission Strategy

- **Primary target**: CIKM 2026 Short / Resource Track — submission deadline June 8, 2026. The intrinsic evaluation protocol and the systematic operator benchmark are resource-track contributions.
- **Secondary target**: MLG 2026 or WAFL 2026 at ECML-PKDD — estimated deadline mid-June 2026.
- **Tertiary target**: ICDM 2026 Workshop — August 2026 deadline.
- **arXiv strategy**: Upload the main FedProp paper to arXiv first (for job visibility). Cite it in this paper as '[FedProp, arXiv:XXXX]'. This positions both papers as a research program.
- **Scope discipline**: The experiment matrix is fixed as defined in Section 6.4. No additional datasets, operators, or analysis axes should be added after June 1 (CIKM abstract deadline). Emergency submission rule: if experiments are 90% complete by June 5, submit with the available results and note pending ablations in the limitations.

---

*End of Proto-Paper — To be expanded with experimental results and full literature review.*
